import requests
import psycopg2
import time
import os
from typing import List, Dict, Set
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Muat variabel lingkungan dari file .env
load_dotenv()

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "DB_HOST_PLACEHOLDER")
DB_NAME = os.getenv("DB_NAME", "tanya_quran_hadist")
DB_USER = os.getenv("DB_USER", "DB_USER_PLACEHOLDER")
DB_PASS = os.getenv("DB_PASS", "DB_PASS_PLACEHOLDER")

# Global Session for Connection Pooling
http = requests.get("https://equran.id/api/v2/surat").json()["data"] # Pre-warm cache for meta
http_session = requests.Session()

def get_connection(autocommit=False):
    conn = psycopg2.connect(
        host=DB_HOST, 
        user=DB_USER, 
        password=DB_PASS, 
        dbname=DB_NAME, 
        connect_timeout=10,
        options="-c lock_timeout=5000" # Timeout 5 detik jika tabel terkunci
    )
    conn.autocommit = autocommit
    return conn

def optimize_database_performance():
    """Trik Optimasi: Membersihkan Bloat dan mempercepat pembuatan index."""
    print("🧹 PERFORMING DB MAINTENANCE (Vacuum & Analyze)...")
    conn = get_connection(autocommit=True)
    cur = conn.cursor()
    try:
        # Meningkatkan memori untuk pembuatan index (Maintenance Work Mem)
        cur.execute("SET maintenance_work_mem = '64MB';")
        
        # Membersihkan dead tuples dari proses gagal sebelumnya
        pbar = tqdm(total=2, desc="DB Optimization")
        
        pbar.set_description("Cleaning Table Bloat (VACUUM)")
        cur.execute("VACUUM sumber_quran;")
        pbar.update(1)
        
        pbar.set_description("Updating Statistics (ANALYZE)")
        cur.execute("ANALYZE sumber_quran;")
        pbar.update(1)
        pbar.close()
        
        print("✅ Database maintenance complete.")
    except Exception as e:
        print(f"⚠️ Maintenance skipped: {e} (Mungkin tabel belum ada)")
    finally:
        cur.close()
        conn.close()

def create_table_and_indexes():
    print(f"🛠️  Ensuring Schema & High-Speed Indexes...")
    conn = get_connection(autocommit=True)
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sumber_quran (
                id SERIAL PRIMARY KEY,
                nomor_juz INTEGER,
                nomor_surah INTEGER,
                nama_surah VARCHAR(255),
                nomor_ayat INTEGER,
                text_arab TEXT,
                terjemah_indonesia TEXT,
                tafsir_idonesia TEXT
            );
        """)
        
        # Buat index satu per satu agar lebih terpantau
        index_tasks = [
            ("idx_nomor_surah", "nomor_surah"),
            ("idx_nomor_ayat", "nomor_ayat")
        ]
        
        for idx_name, column in tqdm(index_tasks, desc="Indexing Columns"):
            cur.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON sumber_quran ({column});")
            
    finally:
        cur.close()
        conn.close()

def resequence_ids():
    print("\n🚀 FINALIZING: Resequencing IDs...")
    conn = get_connection(autocommit=True)
    cur = conn.cursor()
    try:
        cur.execute("""
            BEGIN;
            CREATE TEMP TABLE temp_quran AS SELECT * FROM sumber_quran ORDER BY nomor_surah, nomor_ayat;
            TRUNCATE TABLE sumber_quran RESTART IDENTITY;
            INSERT INTO sumber_quran (nomor_juz, nomor_surah, nama_surah, nomor_ayat, text_arab, terjemah_indonesia, tafsir_idonesia)
            SELECT nomor_juz, nomor_surah, nama_surah, nomor_ayat, text_arab, terjemah_indonesia, tafsir_idonesia FROM temp_quran;
            COMMIT;
        """)
        print("✅ Database is now perfectly ordered and indexed.")
    except Exception as e:
        print(f"❌ Resequencing failed: {e}")
    finally:
        cur.close()
        conn.close()

def get_juz_mapping():
    r = http_session.get("https://api.alquran.cloud/v1/meta", timeout=15)
    return [(d["surah"], d["ayah"]) for d in r.json()["data"]["juzs"]["references"]]

def ingest_surah_worker(surah_info, juz_mapping):
    surah_no, nama_surah = surah_info
    conn = get_connection()
    cur = conn.cursor()
    try:
        s_resp = http_session.get(f"https://equran.id/api/v2/surat/{surah_no}", timeout=15).json()["data"]
        t_resp = http_session.get(f"https://equran.id/api/v2/tafsir/{surah_no}", timeout=15).json()["data"]
        t_map = {t["ayat"]: t["teks"] for t in t_resp["tafsir"]}
        
        def get_j(s, a, m):
            for j_n in range(30, 0, -1):
                ss, sa = m[j_n-1]
                if s > ss or (s == ss and a >= sa): return j_n
            return 1

        batch = [(get_j(surah_no, a["nomorAyat"], juz_mapping), surah_no, nama_surah, a["nomorAyat"], a["teksArab"], a["teksIndonesia"], t_map.get(a["nomorAyat"], "")) for a in s_resp["ayat"]]
        
        cur.execute("DELETE FROM sumber_quran WHERE nomor_surah = %s", (surah_no,))
        execute_values(cur, "INSERT INTO sumber_quran (nomor_juz, nomor_surah, nama_surah, nomor_ayat, text_arab, terjemah_indonesia, tafsir_idonesia) VALUES %s", batch)
        conn.commit()
        return f"✅ {nama_surah}"
    except Exception as e:
        conn.rollback()
        return f"❌ {nama_surah}: {e}"
    finally:
        cur.close()
        conn.close()

def run_ultra_ingestion():
    print("🔥 STARTING ULTRA-OPTIMIZED INGESTION\n")
    
    # Step 1: Schema
    create_table_and_indexes()
    
    # Step 2: Maintenance (Penting jika ada data lama/bloat)
    optimize_database_performance()
    
    juz_mapping = get_juz_mapping()
    
    # Step 3: Fast Scan
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nomor_surah, COUNT(*) FROM sumber_quran GROUP BY nomor_surah")
    db_status = {row[0]: row[1] for row in cur.fetchall()}
    cur.close()
    conn.close()
    
    api_meta = http # Using pre-warmed meta
    to_process = [(m["nomor"], m["namaLatin"]) for m in api_meta if db_status.get(m["nomor"]) != m["jumlahAyat"]]
    
    if not to_process:
        print("\n✨ Data already synced.")
        resequence_ids()
        return

    print(f"🚀 Syncing {len(to_process)} surahs (Parallel Workers: 4)\n")
    
    main_pbar = tqdm(total=len(to_process), desc="Total Progress")
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(ingest_surah_worker, s, juz_mapping): s for s in to_process}
        for f in as_completed(futures):
            main_pbar.write(f.result())
            main_pbar.update(1)
    
    main_pbar.close()
    resequence_ids()
    print("\n🏁 DONE!")

if __name__ == "__main__":
    run_ultra_ingestion()
