import psycopg2
try:
    conn = psycopg2.connect(host='DB_HOST_PLACEHOLDER', user='DB_USER_PLACEHOLDER', password='DB_PASS_PLACEHOLDER', dbname='tanya_quran_hadist')
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
