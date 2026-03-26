# 📖 al-Huda: Tanya Quran Hadist (Semantic Search)

**al-Huda** adalah mesin pencari semantik cerdas untuk teks suci Al-Quran dan Hadist (HR. Bukhari). Berbeda dengan pencarian berbasis kata kunci konvensional, al-Huda memahami konteks makna dari setiap ayat dan hadits menggunakan teknologi *Vector Embeddings*.

## 🏗️ Filosofi Arsitektur (Narrative-First)
Proyek ini dibangun dengan fokus pada **kemandirian infrastruktur AI**. Kami menggunakan model AI lokal (E5-Small) yang dijalankan sepenuhnya di sisi server tanpa ketergantungan pada API eksternal (seperti OpenAI). 

Data Al-Quran dan Hadist disimpan dalam **PostgreSQL dengan ekstensi pgvector**, memungkinkan kita melakukan kueri "jarak kosinus" (Cosine Distance) untuk menemukan teks yang secara semantik paling relevan dengan pertanyaan pengguna. Logika pemisahan Sanad dan Matan pada Hadits menggunakan algoritma *Rightmost Search* (V3) untuk menjamin akurasi data yang ditampilkan kepada umat.

## 🛠️ Tech Stack
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12+)
- **Package Manager:** [uv](https://github.com/astral-sh/uv) (Tercepat & Handal)
- **Database:** PostgreSQL 16 + [pgvector](https://github.com/pgvector/pgvector)
- **AI Engine:** [Sentence-Transformers](https://www.sbert.net/) (Model: `intfloat/multilingual-e5-small`)
- **Image Engine:** [Pillow](https://python-pillow.org/) (Untuk generator gambar share)
- **Testing:** [pytest](https://docs.pytest.org/)

## 🚀 Persiapan Instalasi

### 1. Prasyarat
Pastikan Anda sudah menginstal `uv` di sistem Anda. Jika belum:
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Konfigurasi Environment
Duplikasi file `.env.example` menjadi `.env` dan lengkapi kredensial database Anda:
```bash
cp .env.example .env
```

### 3. Instalasi Dependensi
Gunakan `uv` untuk menginstal semua library yang diperlukan secara instan:
```bash
uv sync
```

## 🏃 Menjalankan Aplikasi

### Menjalankan Backend (Development)
```bash
uv run uvicorn main:app --reload
```
Akses dokumentasi API interaktif di: `http://127.0.0.1:8000/docs`

### Menjalankan Ingestor Data (Opsional)
Jika database Anda masih kosong, jalankan skrip berikut untuk menyerap data dan membuat vektor:
```bash
# Ingest Data Al-Quran
uv run python create_quran_dataset.py
uv run python create_quran_embeddings.py

# Ingest Data Hadits
uv run python create_hadist_dataset.py
uv run python create_hadist_embeddings.py
```

## 🧪 Validasi & Testing
Kami menyediakan suite pengujian otomatis untuk memastikan mesin pencari memberikan hasil yang relevan:
```bash
uv run pytest tests/test_search_engine.py
```

## 📸 Fitur Unggulan: Share Image Generator
al-Huda dilengkapi dengan mesin perender gambar sisi server. Pengguna dapat menghasilkan gambar estetik berukuran 1:1 berisi ayat/hadits lengkap dengan branding "al-Huda" untuk dibagikan ke media sosial secara instan.

---
**al-Huda Project** - *Menghadirkan Petunjuk di Ujung Jari Anda.*
