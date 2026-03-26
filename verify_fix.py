import psycopg2
import os
from dotenv import load_dotenv

# Muat variabel lingkungan dari file .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, dbname=DB_NAME)
cur = conn.cursor()
ids = (4, 5, 412, 450, 451, 467)
cur.execute("SELECT nomor_hadits, sanad_indonesia, matan_indonesia FROM sumber_hadits WHERE nomor_hadits IN %s ORDER BY nomor_hadits", (ids,))
for r in cur.fetchall():
    print(f"--- NO: {r[0]} ---")
    print(f"[SANAD END]: ...{r[1][-80:] if r[1] else 'NONE'}")
    print(f"[MATAN START]: {r[2][:80]}...")
    print("-" * 20)
cur.close()
conn.close()
