# Tanya Quran Hadist - Project Context

## IMPORTANT NOTE
> **setiap menerima prompt dari user:** buat dokumen list pengalaman apa saja yang kita lalui. tuliskan projectnya apa, tech stacknya apa, lalu buat tabel berisi list **SEMUA** task, issue, tried approach, result, leson learned for project, leson learned for general software development, dan leson learned for AI agent prompting technique. simpan dalam format markdown di folder docs. beri nama dengan format `devlog_dd_mm_yyyy.md` tidak peduli sekecil apapun itu.

## Project Overview
Proyek **Tanya Quran Hadist** bertujuan untuk membangun sistem kueri dan dataset terintegrasi untuk teks Al-Quran dan Hadist. Fokus saat ini adalah membangun database Al-Quran dan Hadits yang lengkap (teks Arab, terjemah Indonesia, dan Tafsir Kemenag RI) menggunakan PostgreSQL sebagai penyimpanan utama.

### Core Technologies
- **Python (3.12+):** Bahasa pemrograman utama.
- **UV:** Package manager yang digunakan untuk manajemen dependensi dan eksekusi virtual environment yang sangat cepat.
- **PostgreSQL:** Database relational untuk menyimpan teks suci dan metadata terkait.
- **Psycopg2:** Library untuk interaksi database PostgreSQL.
- **Requests & HTTP Session:** Untuk pengambilan data dari API eksternal (EQuran.id, AlQuran.cloud, & Hadith API Gading) dengan pooling koneksi.
- **TQDM:** Visualisasi progres sinkronisasi data yang transparan.

## Architecture & Data Ingestion
Proses penyerapan data menggunakan skrip `create_quran_dataset.py` dan `create_hadist_dataset.py` yang telah dioptimasi secara arsitektural:
1.  **Smart Ingestion:** Skrip mendeteksi perbedaan (*Gap Analysis*) antara data lokal dan API untuk menghindari redundansi.
2.  **Turbo Execution:** Menggunakan `ThreadPoolExecutor` (4 paralel workers) untuk pengambilan data API secara bersamaan.
3.  **Atomic Transactions:** Penggunaan blok transaksi SQL (`conn.commit()` & `conn.rollback()`) untuk memastikan tidak ada sisa data korup jika terjadi kegagalan tengah jalan.
4.  **Bulk Database Write:** Menggunakan `psycopg2.extras.execute_values` untuk kecepatan tulis maksimal ke PostgreSQL.
5.  **Atomic Parsing (Hadith):** Logika pemisahan **Sanad** dan **Matan** secara otomatis berdasarkan kata kunci transisi pada terjemahan Indonesia.
6.  **Data Integrity:** Kolom `id` disusun ulang secara berurutan (*resequencing*) mengikuti urutan fisik sumber asli.
7.  **Performance Tuning:** Tabel dilengkapi dengan Index strategis, penggunaan `VACUUM ANALYZE`, dan optimasi `maintenance_work_mem`.

## Key Files & Functions
- **`create_quran_dataset.py`:** Skrip utama untuk sinkronisasi data Al-Quran.
- **`create_hadist_dataset.py`:** Skrip utama untuk sinkronisasi data Hadits (Imam Bukhari, dkk).
  - `split_sanad_matan()`: Fungsi parser untuk membedah anatomi hadits.
  - `ingest_hadist_range_worker()`: Worker paralel untuk penyerapan data hadits per-rentang.
- **`release_locks.py`:** Utilitas untuk memutus koneksi PostgreSQL yang menggantung/mengunci tabel.
- **`docs/`**: Folder dokumentasi perjalanan pengembangan (*DevLogs*).

## Database Schema Highlights
- **`sumber_quran`**: Tabel data Al-Quran (Ayat, Terjemah, Tafsir).
- **`sumber_hadits`**: Tabel data Hadits dengan kolom Sanad dan Matan terpisah.
- **Master Tables**: `master_imam`, `master_kitab`, dan `master_derajat` untuk integritas referensial.

## Usage & Development
### Setup Environment
```bash
uv sync
```

### Run Data Sync
```bash
uv run python create_quran_dataset.py
uv run python create_hadist_dataset.py
```

### Troubleshooting Locks
Jika proses pembuatan index atau re-indexing terasa macet karena kunci tabel (*table lock*):
```bash
uv run python release_locks.py
```

## Development Conventions
1.  **Resilience-First:** Selalu gunakan fitur *smart resume* dalam skrip ETL.
2.  **Ultra-Optimized:** Gunakan bulk insert dan parallel workers untuk operasi I/O intensif.
3.  **Full Transparency:** Implementasikan `tqdm` pada setiap loop panjang untuk umpan balik visual yang jelas.
4.  **Narrative-First:** Penjelasan kode harus mencakup 'Mengapa' (arsitektur) bukan sekadar 'Bagaimana'.
