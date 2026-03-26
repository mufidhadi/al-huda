import requests
import psycopg2
import time
import os
from typing import List, Dict, Set, Tuple
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
http_session = requests.Session()

def get_connection(autocommit=False):
    conn = psycopg2.connect(
        host=DB_HOST, 
        user=DB_USER, 
        password=DB_PASS, 
        dbname=DB_NAME, 
        connect_timeout=15,
        options="-c lock_timeout=10000"
    )
    conn.autocommit = autocommit
    return conn

def split_sanad_matan(text: str) -> Tuple[str, str]:
    """
    Logika V3: Rightmost Search Optimization.
    Memisahkan sanad dan matan berdasarkan titik transisi terakhir (perawi terakhir).
    """
    # 1. Prioritas Utama: Sabda Nabi (Gunakan split pertama untuk menangkap awal sabda)
    for d in ["bersabda:", "bersabda;", "bersabda \""]:
        if d in text:
            parts = text.split(d, 1)
            return (parts[0] + d).strip(), parts[1].strip()

    # 2. Prioritas Kedua: Transisi Kutipan Terakhir (Rightmost search)
    indicators = [
        "berkata, \"", "berkata, '", "berkata: \"", "berkata; \"", 
        "berkata, bahwa", "mengatakan, \"", "mengatakan, '"
    ]
    
    best_pos = -1
    best_delimiter = None
    
    for d in indicators:
        pos = text.rfind(d) # Cari posisi TERAKHIR dari delimiter
        if pos > best_pos:
            best_pos = pos
            best_delimiter = d
            
    if best_delimiter:
        parts = text.rsplit(best_delimiter, 1)
        return (parts[0] + best_delimiter).strip(), parts[1].strip()

    # 3. Prioritas Ketiga: Koma terakhir setelah verb berkata
    if "berkata," in text:
        parts = text.rsplit("berkata,", 1)
        return (parts[0] + "berkata,").strip(), parts[1].strip()

    # Fallback: Anggap semuanya Matan
    return "", text.strip()

def optimize_database_performance():
    print("🧹 DB MAINTENANCE: VACUUM & ANALYZE...")
    conn = get_connection(autocommit=True)
    cur = conn.cursor()
    try:
        cur.execute("SET maintenance_work_mem = '64MB';")
        cur.execute("VACUUM sumber_hadits;")
        cur.execute("ANALYZE sumber_hadits;")
        print("✅ Maintenance complete.")
    except Exception as e:
        print(f"⚠️ Maintenance failed: {e}")
    finally:
        cur.close()
        conn.close()

def resequence_ids():
    print("\n🚀 FINALIZING: Resequencing Hadith IDs...")
    conn = get_connection(autocommit=True)
    cur = conn.cursor()
    try:
        cur.execute("""
            BEGIN;
            CREATE TEMP TABLE temp_hadits AS SELECT * FROM sumber_hadits ORDER BY id_kitab, nomor_hadits;
            TRUNCATE TABLE sumber_hadits RESTART IDENTITY;
            INSERT INTO sumber_hadits (id_kitab, id_derajat, nomor_hadits, teks_arab_full, sanad_indonesia, matan_indonesia, terjemah_full)
            SELECT id_kitab, id_derajat, nomor_hadits, teks_arab_full, sanad_indonesia, matan_indonesia, terjemah_full FROM temp_hadits;
            COMMIT;
        """)
        print("✅ IDs perfectly re-sequenced.")
    except Exception as e:
        print(f"❌ Resequencing failed: {e}")
    finally:
        cur.close()
        conn.close()

def ingest_hadist_range_worker(range_info: Tuple[int, int], kitab_id: int, derajat_id: int):
    start, end = range_info
    conn = get_connection(autocommit=False)
    cur = conn.cursor()
    try:
        url = f"https://api.hadith.gading.dev/books/bukhari?range={start}-{end}"
        resp = http_session.get(url, timeout=25).json()
        hadist_list = resp["data"]["hadiths"]
        
        batch_data = []
        for h in hadist_list:
            sanad, matan = split_sanad_matan(h["id"])
            batch_data.append((kitab_id, derajat_id, h["number"], h["arab"], sanad, matan, h["id"]))
        
        cur.execute("DELETE FROM sumber_hadits WHERE id_kitab = %s AND nomor_hadits BETWEEN %s AND %s", (kitab_id, start, end))
        execute_values(cur, """
            INSERT INTO sumber_hadits 
            (id_kitab, id_derajat, nomor_hadits, teks_arab_full, sanad_indonesia, matan_indonesia, terjemah_full)
            VALUES %s
        """, batch_data)
        
        conn.commit()
        return f"✅ Range {start}-{end} synced."
    except Exception as e:
        conn.rollback()
        return f"❌ Range {start}-{end} failed: {e}"
    finally:
        cur.close()
        conn.close()

def run_smart_hadist_ingestion():
    print("🔥 STARTING ATOMIC TURBO HADITH SYNC (Logic V3)\n")
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM master_kitab WHERE slug = 'bukhari'")
    kitab_id = cur.fetchone()[0]
    cur.execute("SELECT id FROM master_derajat WHERE label = 'Shahih'")
    derajat_id = cur.fetchone()[0]
    cur.close()
    conn.close()
    
    total_hadits = http_session.get("https://api.hadith.gading.dev/books/bukhari/1").json()["data"]["available"]
    
    # Re-process ALL to ensure Logic V3 applied correctly
    ranges = []
    chunk_size = 300
    for i in range(1, total_hadits + 1, chunk_size):
        end = min(i + chunk_size - 1, total_hadits)
        ranges.append((i, end))
            
    print(f"📦 Re-processing {len(ranges)} chunks using 4 parallel workers...\n")
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(ingest_hadist_range_worker, r, kitab_id, derajat_id): r for r in ranges}
        for f in tqdm(as_completed(futures), total=len(ranges), desc="Global Sync Progress"):
            msg = f.result()
            if "❌" in msg: print(f"\n{msg}")

    optimize_database_performance()
    resequence_ids()
    print("\n🏁 SYNC COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    run_smart_hadist_ingestion()
