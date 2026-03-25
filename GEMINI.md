# Tanya Quran Hadist - Project Context

## IMPORTANT NOTES (SELALU LAKUKAN, JANGAN HAPUS BAGIAN INI KETIKA MENGEDIT FILE GEMINI.MD)
> **setiap menerima prompt dari user:** buat dokumen list pengalaman apa saja yang kita lalui. tuliskan projectnya apa, tech stacknya apa, lalu buat tabel `task & experiences` berisi list **SEMUA** task, issue, tried approach, result, leson learned for project, leson learned for general software development, dan leson learned for AI agent prompting technique. simpan dalam format markdown di folder docs. beri nama dengan format `devlog_dd_mm_yyyy.md` tidak peduli sekecil apapun itu. jangan pernah mengedit isi baris apapun dari tabel `task & experiences`, tambahkan item baris baru setiap saat.

## Project Overview
Proyek **Tanya Quran Hadist** bertujuan untuk membangun sistem kueri dan dataset terintegrasi untuk teks Al-Quran dan Hadist. Fokus utama adalah pada integritas data, pemisahan struktural (Sanad vs Matan), dan optimasi performa menggunakan kueri semantik berbasis AI.

### Core Technologies
- **Python (3.12+):** Bahasa pemrograman utama.
- **UV:** Package manager tercepat untuk manajemen dependensi.
- **PostgreSQL (v16) + pgvector:** Database relasional dengan dukungan penyimpanan vektor (embedding).
- **Sentence-Transformers (E5-Small):** Model lokal (100% independen) untuk text embedding 384 dimensi.
- **Stitch:** Platform desain UI/UX untuk mobile browser experience.
- **pytest & psutil:** Alat pengujian otomatis dan monitoring resource.

## Architecture & Data Ingestion
1.  **Smart Ingestion:** Skrip `create_quran_dataset.py` & `create_hadist_dataset.py` mendeteksi perbedaan (*Gap Analysis*) untuk menghindari redundansi.
2.  **Turbo Execution:** Menggunakan `ThreadPoolExecutor` dan `HTTP Session Pooling` untuk penyerapan data paralel berkecepatan tinggi.
3.  **Atomic Transactions:** Penggunaan blok transaksi SQL (`conn.commit()` & `conn.rollback()`) untuk menjamin kebersihan data.
4.  **Atomic Parsing (Hadith V3):** Logika pemisahan **Sanad** dan **Matan** cerdas menggunakan *Rightmost Search* pada transisi tanda baca Indonesia.
5.  **Vector Search Core:** Library `search_engine.py` mengabstraksi logika kueri semantik menggunakan jarak kosinus (`<=>`) untuk perankingan relevansi.

## Key Files & Functions
- **`search_engine.py`:** Library inti mesin pencari semantik lintas sumber.
- **`create_quran_embeddings.py`:** Skrip pembuat vektor untuk seluruh ayat Al-Quran.
- **`create_hadist_embeddings.py`:** Skrip pembuat vektor untuk seluruh matan Hadits.
- **`perf_test.py`:** Skrip audit latensi dan penggunaan RAM sistem.
- **`docs/`**:
  - `API_CONTRACT.md`: Definisi endpoint dan standar pertukaran data JSON.
  - `UI_UX_DESIGN.md`: Bahasa desain "Pure Search" (Google-style replica).
  - `devlog_dd_mm_yyyy.md`: Dokumentasi historis dan *Lesson Learned*.
  - `performance_test_report.md`: Laporan formal efisiensi resource sistem.

## Usage & Development
### Run Search Library (CLI Test)
```bash
uv run python search_engine.py
```

### Run Performance Audit
```bash
uv run python perf_test.py
```

### Run Automated Tests
```bash
uv run pytest tests/test_search_engine.py
```

## Development Conventions
1.  **Resilience-First:** Selalu gunakan fitur *smart resume* dan *transactional blocks*.
2.  **The Invisibility of UI:** Desain antarmuka harus meniru Google Search Original (Zero distraction).
3.  **Independence:** Pastikan model AI ter-cache secara lokal (100% independent dari cloud API).
4.  **Narrative-First:** Penjelasan kode harus mencakup 'Mengapa' (arsitektur) bukan sekadar 'Bagaimana'.
5.  **Audit-Ready:** Setiap iterasi wajib mencatatkan *Lesson Learned* ke dalam DevLog.
