import psycopg2
import os
from dotenv import load_dotenv

# Muat variabel lingkungan dari file .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME_TARGET = os.getenv("DB_NAME")

try:
    conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, dbname='postgres')
    conn.autocommit = True
    cur = conn.cursor()
    # Menghentikan semua koneksi yang bukan koneksi saat ini ke DB tujuan
    cur.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = %s AND pid != pg_backend_pid()", (DB_NAME_TARGET,))
    print(f"✅ Berhasil memutus semua koneksi liar yang mengunci database {DB_NAME_TARGET}.")
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Gagal membersihkan lock: {e}")
