import psycopg2
try:
    conn = psycopg2.connect(host='DB_HOST_PLACEHOLDER', user='DB_USER_PLACEHOLDER', password='DB_PASS_PLACEHOLDER', dbname='postgres')
    conn.autocommit = True
    cur = conn.cursor()
    # Menghentikan semua koneksi yang bukan koneksi saat ini ke DB tujuan
    cur.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'tanya_quran_hadist' AND pid != pg_backend_pid()")
    print("✅ Berhasil memutus semua koneksi liar yang mengunci database.")
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Gagal membersihkan lock: {e}")
