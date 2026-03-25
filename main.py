from fastapi import FastAPI, Query, HTTPException, Response
from typing import Optional
import re
import psycopg2
from search_engine import QuranHadithSearch
from image_generator import generate_share_image

app = FastAPI(title="Tanya Quran Hadist API", version="1.1")

# Database Configuration
DB_CONFIG = {
    "host": "DB_HOST_PLACEHOLDER",
    "user": "DB_USER_PLACEHOLDER",
    "password": "DB_PASS_PLACEHOLDER",
    "dbname": "tanya_quran_hadist"
}

# Inisialisasi Search Engine
search_engine = QuranHadithSearch(DB_CONFIG)

def highlight_text(text: str, query: str) -> str:
    if not query: return text
    words = query.split()
    pattern = re.compile(f"({'|'.join(map(re.escape, words))})", re.IGNORECASE)
    return pattern.sub(r"<em>\1</em>", text)

@app.get("/api/v1/search")
async def search(
    q: str = Query(None, description="Kata kunci pencarian"),
    source: str = Query("semua", pattern="^(semua|alquran|hadist)$"),
    page: int = Query(1, ge=1, le=10)
):
    if not q: raise HTTPException(status_code=400, detail="Query 'q' is required")
    try:
        limit = 10
        raw_results = search_engine.search(keyword=q, source=source, limit=100)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paged_results = raw_results[start_idx:end_idx]
        
        formatted_results = []
        for res in paged_results:
            content_type = "quran" if res["sumber"] == "Al-Quran" else "hadith"
            highlighted_snippet = highlight_text(res["konten"][:200], q)
            formatted_results.append({
                "id": res["id"], "sumber": res["sumber"], "judul": res["judul"],
                "snippet": highlighted_snippet + "...", "skor_relevansi": res["skor_relevansi"],
                "detail_url": f"/api/v1/{content_type}/{res['id']}"
            })
        return {
            "status": "success",
            "meta": {"query": q, "total_results": len(raw_results), "current_page": page, "per_page": limit, "max_pages": 10},
            "results": formatted_results
        }
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/quran/{id}")
async def get_quran_detail(id: int):
    conn = search_engine._get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, nomor_surah, nama_surah, nomor_ayat, text_arab, terjemah_indonesia, tafsir_idonesia FROM sumber_quran WHERE id = %s", (id,))
        row = cur.fetchone()
        if not row: raise HTTPException(status_code=404, detail="Ayat not found")
        
        # Recommendations (Hadits serupa)
        cur.execute("SELECT embedding FROM embedding_sumber_quran WHERE id = %s", (id,))
        vec_row = cur.fetchone()
        recommendations = []
        if vec_row:
            cur.execute("""
                SELECT h.id, 'HR. Bukhari No. ' || h.nomor_hadits, h.matan_indonesia, (1 - (e.embedding <=> %s::vector))
                FROM sumber_hadits h JOIN embedding_sumber_hadits e ON h.id = e.id
                ORDER BY e.embedding <=> %s::vector LIMIT 3
            """, (vec_row[0], vec_row[0]))
            recommendations = [{"id": r[0], "sumber": "Hadits", "judul": r[1], "konten": r[2][:150], "skor": round(float(r[3])*100, 2)} for r in cur.fetchall()]

        return {
            "status": "success",
            "data": {
                "id": row[0], "surah": row[2], "nomor_ayat": row[3], "teks_arab": row[4], "terjemah": row[5], "tafsir": row[6],
                "navigation": {"prev_id": id-1 if id>1 else None, "next_id": id+1 if id<6236 else None},
                "share": {"text_copy": f"{row[2]} {row[3]} - {row[5]}", "image_api_url": f"/api/v1/share/image?type=quran&id={id}"}
            },
            "recommendations": recommendations
        }
    finally: cur.close(); conn.close()

@app.get("/api/v1/hadith/{id}")
async def get_hadith_detail(id: int):
    conn = search_engine._get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT h.id, k.nama_kitab, h.nomor_hadits, h.teks_arab_full, h.sanad_indonesia, h.matan_indonesia 
            FROM sumber_hadits h JOIN master_kitab k ON h.id_kitab = k.id WHERE h.id = %s
        """, (id,))
        row = cur.fetchone()
        if not row: raise HTTPException(status_code=404, detail="Hadits not found")
        return {
            "status": "success",
            "data": {
                "id": row[0], "kitab": row[1], "nomor_hadits": row[2], "teks_arab": row[3], "sanad": row[4], "matan": row[5],
                "share": {"text_copy": f"{row[1]} No. {row[2]} - {row[5]}", "image_api_url": f"/api/v1/share/image?type=hadith&id={id}"}
            },
            "recommendations": []
        }
    finally: cur.close(); conn.close()

@app.get("/api/v1/share/image")
async def get_share_image(
    type: str = Query(..., pattern="^(quran|hadith)$"),
    id: int = Query(...),
    content_mode: str = "both",
    show_branding: bool = True
):
    conn = search_engine._get_connection()
    cur = conn.cursor()
    try:
        if type == "quran":
            cur.execute("SELECT nama_surah || ' Ayat ' || nomor_ayat, text_arab, terjemah_indonesia FROM sumber_quran WHERE id = %s", (id,))
        else:
            cur.execute("SELECT 'HR. Bukhari No. ' || nomor_hadits, teks_arab_full, matan_indonesia FROM sumber_hadits WHERE id = %s", (id,))
        
        row = cur.fetchone()
        if not row: raise HTTPException(status_code=404, detail="Content not found")
        
        title, text_ar, text_id = row
        
        # Logic for content_mode
        ar_to_draw = text_ar if content_mode in ["both", "arab"] else ""
        id_to_draw = text_id if content_mode in ["both", "translation"] else ""
        
        image_bytes = generate_share_image(title, ar_to_draw, id_to_draw, show_branding)
        return Response(content=image_bytes, media_type="image/png")
    finally: cur.close(); conn.close()

@app.get("/")
def read_root(): return {"message": "Tanya Quran Hadist API is running"}
