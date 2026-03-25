import psycopg2
conn = psycopg2.connect(host='DB_HOST_PLACEHOLDER', user='DB_USER_PLACEHOLDER', password='DB_PASS_PLACEHOLDER', dbname='tanya_quran_hadist')
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
