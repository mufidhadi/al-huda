import psycopg2
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer

class QuranHadithSearch:
    def __init__(self, db_config: Dict):
        self.db_config = db_config
        # Load model secara singleton untuk efisiensi
        print("🧠 Initializing Search Engine (Loading Local AI Model)...")
        self.model = SentenceTransformer('intfloat/multilingual-e5-small')
        
    def _get_connection(self):
        return psycopg2.connect(**self.db_config)

    def search(self, keyword: str, source: str = "semua", limit: int = 10) -> List[Dict]:
        """
        Alur pencarian utama:
        1. Embed keyword
        2. Query SQL menggunakan Vector Distance
        3. Gabungkan dan urutkan hasil
        """
        # E5 Small requirement: prefix query with 'query: '
        query_vector = self.model.encode(f"query: {keyword}", normalize_embeddings=True).tolist()
        
        results = []
        
        conn = self._get_connection()
        cur = conn.cursor()
        
        try:
            # PENCARIAN AL-QURAN
            if source in ["alquran", "semua"]:
                cur.execute(f"""
                    SELECT 
                        'Al-Quran' as sumber,
                        q.nama_surah || ' Ayat ' || q.nomor_ayat as judul,
                        q.terjemah_indonesia as konten,
                        q.text_arab as teks_asli,
                        (1 - (e.embedding <=> %s::vector)) as skor_relevansi
                    FROM sumber_quran q
                    JOIN embedding_sumber_quran e ON q.id = e.id
                    ORDER BY e.embedding <=> %s::vector
                    LIMIT %s
                """, (query_vector, query_vector, limit))
                
                for row in cur.fetchall():
                    results.append(self._format_row(row))

            # PENCARIAN HADITS
            if source in ["hadist", "semua"]:
                cur.execute(f"""
                    SELECT 
                        'Hadits' as sumber,
                        'HR. Bukhari No. ' || h.nomor_hadits as judul,
                        h.matan_indonesia as konten,
                        h.teks_arab_full as teks_asli,
                        (1 - (e.embedding <=> %s::vector)) as skor_relevansi
                    FROM sumber_hadits h
                    JOIN embedding_sumber_hadits e ON h.id = e.id
                    ORDER BY e.embedding <=> %s::vector
                    LIMIT %s
                """, (query_vector, query_vector, limit))
                
                for row in cur.fetchall():
                    results.append(self._format_row(row))

            # SORTING: Urutkan berdasarkan skor relevansi tertinggi (Google Search style)
            results.sort(key=lambda x: x['skor_relevansi'], reverse=True)
            
        finally:
            cur.close()
            conn.close()
            
        return results[:limit]

    def _format_row(self, row) -> Dict:
        return {
            "sumber": row[0],
            "judul": row[1],
            "konten": row[2],
            "teks_asli": row[3],
            "skor_relevansi": round(float(row[4]) * 100, 2) # Dalam persentase
        }

if __name__ == "__main__":
    # Test script sederhana
    config = {
        "host": "DB_HOST_PLACEHOLDER",
        "user": "DB_USER_PLACEHOLDER",
        "password": "DB_PASS_PLACEHOLDER",
        "dbname": "tanya_quran_hadist"
    }
    
    engine = QuranHadithSearch(config)
    query = input("Ketik apa yang ingin Anda cari (e.g. 'cara shalat'): ")
    sumber_pilihan = input("Pilih sumber (alquran/hadist/semua) [default: semua]: ") or "semua"
    
    print(f"\n🔍 Mencari '{query}' di {sumber_pilihan}...\n")
    results = engine.search(query, source=sumber_pilihan)
    
    for i, res in enumerate(results, 1):
        print(f"{i}. [{res['sumber']}] {res['judul']} (Relevansi: {res['skor_relevansi']}%)")
        print(f"   {res['konten'][:150]}...")
        print("-" * 50)
