import psycopg2
import time
from typing import List, Dict, Tuple
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from psycopg2.extras import execute_values

# Database Configuration
DB_HOST = "DB_HOST_PLACEHOLDER"
DB_NAME = "tanya_quran_hadist"
DB_USER = "DB_USER_PLACEHOLDER"
DB_PASS = "DB_PASS_PLACEHOLDER"

# Model Configuration (Same as Quran for consistency)
MODEL_NAME = 'intfloat/multilingual-e5-small'
EMBEDDING_DIM = 384

def get_connection():
    return psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, dbname=DB_NAME, connect_timeout=15)

def create_embedding_table():
    print(f"🛠️  Initializing Hadith Embedding Table...")
    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    
    # Create Table for Hadith Embeddings (Shared Primary Key Pattern)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS embedding_sumber_hadits (
            id INTEGER PRIMARY KEY REFERENCES sumber_hadits(id) ON DELETE CASCADE,
            embedding VECTOR({EMBEDDING_DIM})
        );
    """)
    
    # HNSW Index for High-Speed Vector Search
    print("   ⚡ Creating HNSW index for hadith search...")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_hadits_embedding ON embedding_sumber_hadits USING hnsw (embedding vector_cosine_ops);")
    
    cur.close()
    conn.close()

def run_hadist_embedding_ingestion():
    print(f"🚀 STARTING HADITH EMBEDDING INGESTION (Source: Matan)\n")
    
    # 1. Load Model (Should be cached locally now)
    print("🧠 Loading model...")
    model = SentenceTransformer(MODEL_NAME)
    
    create_embedding_table()
    
    # 2. Audit: Temukan matan hadits yang belum punya embedding
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT h.id, h.matan_indonesia 
        FROM sumber_hadits h
        LEFT JOIN embedding_sumber_hadits e ON h.id = e.id
        WHERE e.id IS NULL
        ORDER BY h.id
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    if not rows:
        print("✨ All Hadith matans are already embedded.")
        return

    print(f"📦 Processing {len(rows)} Hadiths in batches...\n")
    
    # 3. Batch Processing
    batch_size = 64
    pbar = tqdm(total=len(rows), desc="Hadith Ingestion")
    
    for i in range(0, len(rows), batch_size):
        batch_rows = rows[i : i + batch_size]
        
        # E5 Small requirement: prefix passages with 'passage: '
        # Handle cases where matan might be empty (though unlikely with our v3 parser)
        texts = [f"passage: {row[1] if row[1] else ' '}" for row in batch_rows]
        ids = [row[0] for row in batch_rows]
        
        # Generate Vectors
        embeddings = model.encode(texts, normalize_embeddings=True)
        
        # Prepare data
        data_to_insert = [(ids[j], embeddings[j].tolist()) for j in range(len(ids))]
        
        # Bulk Insert
        conn = get_connection()
        cur = conn.cursor()
        try:
            execute_values(cur, "INSERT INTO embedding_sumber_hadits (id, embedding) VALUES %s ON CONFLICT (id) DO UPDATE SET embedding = EXCLUDED.embedding", data_to_insert)
            conn.commit()
        except Exception as e:
            conn.rollback()
            pbar.write(f"❌ Batch error: {e}")
        finally:
            cur.close()
            conn.close()
            
        pbar.update(len(batch_rows))
        
    pbar.close()
    print("\n🏁 HADITH EMBEDDING INGESTION COMPLETE!")

if __name__ == "__main__":
    run_hadist_embedding_ingestion()
