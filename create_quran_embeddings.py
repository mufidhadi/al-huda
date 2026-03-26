import psycopg2
import time
import os
from typing import List, Dict, Tuple
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Muat variabel lingkungan dari file .env
load_dotenv()

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "DB_HOST_PLACEHOLDER")
DB_NAME = os.getenv("DB_NAME", "tanya_quran_hadist")
DB_USER = os.getenv("DB_USER", "DB_USER_PLACEHOLDER")
DB_PASS = os.getenv("DB_PASS", "DB_PASS_PLACEHOLDER")

# Model Configuration
# E5 model requires prefix 'passage: ' for documents to be indexed
MODEL_NAME = 'intfloat/multilingual-e5-small'
EMBEDDING_DIM = 384

def get_connection():
    return psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, dbname=DB_NAME, connect_timeout=15)

def create_embedding_table():
    print(f"🛠️  Initializing Embedding Table...")
    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    
    # Create Table for Embeddings
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS embedding_sumber_quran (
            id INTEGER PRIMARY KEY REFERENCES sumber_quran(id) ON DELETE CASCADE,
            embedding VECTOR({EMBEDDING_DIM})
        );
    """)
    
    # HNSW Index untuk pencarian vektor secepat kilat
    print("   ⚡ Creating HNSW index for vector search...")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_quran_embedding ON embedding_sumber_quran USING hnsw (embedding vector_cosine_ops);")
    
    cur.close()
    conn.close()

def run_embedding_ingestion():
    print(f"🚀 STARTING QURAN EMBEDDING INGESTION ({MODEL_NAME})\n")
    
    # 1. Load Model (Lokal di VPS)
    print("🧠 Loading model into memory...")
    model = SentenceTransformer(MODEL_NAME)
    
    create_embedding_table()
    
    # 2. Audit: Temukan data yang belum punya embedding
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT q.id, q.terjemah_indonesia 
        FROM sumber_quran q
        LEFT JOIN embedding_sumber_quran e ON q.id = e.id
        WHERE e.id IS NULL
        ORDER BY q.id
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    if not rows:
        print("✨ All Quran translations are already embedded.")
        return

    print(f"📦 Processing {len(rows)} translations in batches...\n")
    
    # 3. Batch Processing (Optimized for RAM)
    batch_size = 64
    pbar = tqdm(total=len(rows), desc="Generating Embeddings")
    
    for i in range(0, len(rows), batch_size):
        batch_rows = rows[i : i + batch_size]
        
        # E5 Small requirement: prefix passages with 'passage: '
        texts = [f"passage: {row[1]}" for row in batch_rows]
        ids = [row[0] for row in batch_rows]
        
        # Generate Vectors
        embeddings = model.encode(texts, normalize_embeddings=True)
        
        # Prepare data for Postgres
        data_to_insert = [(ids[j], embeddings[j].tolist()) for j in range(len(ids))]
        
        # Bulk Insert
        conn = get_connection()
        cur = conn.cursor()
        try:
            execute_values(cur, "INSERT INTO embedding_sumber_quran (id, embedding) VALUES %s ON CONFLICT (id) DO UPDATE SET embedding = EXCLUDED.embedding", data_to_insert)
            conn.commit()
        except Exception as e:
            conn.rollback()
            pbar.write(f"❌ Batch error: {e}")
        finally:
            cur.close()
            conn.close()
            
        pbar.update(len(batch_rows))
        
    pbar.close()
    print("\n🏁 QURAN EMBEDDING INGESTION COMPLETE!")

if __name__ == "__main__":
    run_embedding_ingestion()
