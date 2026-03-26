import psycopg2
import os
from dotenv import load_dotenv

# Muat variabel lingkungan dari file .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

try:
    conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, dbname=DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT name, default_version, installed_version FROM pg_available_extensions WHERE name = 'vector'")
    res = cur.fetchone()
    if res:
        print(f"✅ Ekstensi 'pgvector' TERSEDIA di server.")
        print(f"   - Versi default: {res[1]}")
        print(f"   - Versi terinstal: {res[2] if res[2] else 'Belum diaktifkan di database ini'}")
    else:
        print("❌ Ekstensi 'pgvector' TIDAK DITEMUKAN di server ini.")
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Gagal memeriksa ekstensi: {e}")
