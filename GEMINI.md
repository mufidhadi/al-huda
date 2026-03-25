# al-Huda - Project Context

## Project Overview
Proyek **al-Huda** (sebelumnya: Tanya Quran Hadist) bertujuan untuk membangun sistem kueri dan dataset terpadu untuk teks Al-Quran dan Hadist. Fokus utama adalah pada integritas data, pemisahan struktural (Sanad vs Matan), dan optimasi performa menggunakan kueri semantik berbasis AI yang telah teruji secara masif.

### Core Technologies
- **Python (3.12+):** Bahasa pemrograman utama backend.
- **FastAPI:** Framework API modern untuk penyajian data.
- **Next.js (App Router):** Framework frontend untuk antarmuka mobile-friendly.
- **Tailwind CSS:** Styling antarmuka yang bersih dan minimalis.
- **PostgreSQL (v16) + pgvector:** Database relasional dengan dukungan kueri semantik (vektor).
- **Sentence-Transformers (E5-Small):** Model lokal (100% independen) untuk text embedding 384 dimensi.
- **Docker & Docker Compose:** Orkestrasi infrastruktur aplikasi.

## Architecture & Data Ingestion
1.  **Smart Ingestion:** Skrip mendeteksi perbedaan data lokal vs API untuk menghindari redundansi.
2.  **Turbo Execution:** Paralelisme tingkat tinggi menggunakan `ThreadPoolExecutor` dan `Bulk Write` ke database.
3.  **Atomic Integrity:** Blok transaksi SQL dan pemisahan Sanad-Matan (V3) yang presisi.
4.  **Vector Core:** Library `search_engine.py` menggunakan perankingan Cosine Distance (`<=>`).
5.  **Social Sharing Engine:** Generator gambar 1:1 sisi server untuk penyebaran konten religi yang estetik dengan branding **al-Huda**.

## Key Files & Functions
- **`main.py`:** Server utama FastAPI yang menyajikan endpoint v1.1.
- **`frontend/`**: Aplikasi web Next.js dengan desain "Pure Search".
- **`search_engine.py`:** Library inti mesin pencari semantik.
- **`image_generator.py`:** Modul perender gambar 1:1 berbasis Pillow.
- **`docker-compose.yml`:** Konfigurasi orkestrasi Backend & Frontend.

## Usage & Development
### Start Application (Docker)
```bash
docker-compose up -d --build
```

### Local Development (Backend)
```bash
uv run uvicorn main:app --reload
```

### Local Development (Frontend)
```bash
cd frontend && npm run dev
```

## Development Conventions
1.  **Resilience-First:** Gunakan *smart resume* dan *transactional blocks*.
2.  **The Invisibility of UI:** Antarmuka harus meniru Google Search Original secara ketat (al-Huda branding).
3.  **Independence:** Model AI harus ter-cache secara lokal (offline-capable).
4.  **Narrative-First:** Penjelasan kode harus mencakup 'Mengapa' (arsitektur) bukan sekadar 'How'.
5.  **Audit-Ready:** Dokumentasikan setiap *Lesson Learned* ke dalam DevLog secara kumulatif.
