# Performance & Resource Audit Report
**Project:** Tanya Quran Hadist  
**Date:** 25 Maret 2026  
**Environment:** VPS win32 (PostgreSQL Remote)

## 📊 Resource Usage
| Metric | Value | Description |
| :--- | :--- | :--- |
| **Baseline RAM** | 356.67 MB | Penggunaan RAM awal aplikasi. |
| **Loaded RAM** | 681.86 MB | RAM setelah model AI `multilingual-e5-small` dimuat. |
| **Net Model RAM** | **325.19 MB** | Kapasitas RAM murni yang dikonsumsi model AI. |
| **Peak Search RAM** | 768.60 MB | RAM maksimal saat melayani kueri pencarian. |

## ⏱️ Execution Latency
| Phase | Duration | Description |
| :--- | :--- | :--- |
| **Initialization** | 11.55 seconds | Waktu tunggu hingga model AI siap digunakan. |
| **Avg Search Latency** | **937.09 ms** | Rata-rata waktu respon per kueri (Semantic + DB JOIN). |
| **P95 Search Latency**| 1350.71 ms | 95% kueri diselesaikan di bawah waktu ini. |

## 🔍 Analysis & Insights
1.  **Efficiency:** Model `e5-small` terbukti sangat hemat resource, hanya memakan ~325MB RAM. Ini sangat ideal untuk VPS dengan RAM 2GB atau bahkan 1GB.
2.  **Performance:** Latensi di bawah 1 detik sangat dapat diterima untuk aplikasi *end-user*. Sebagian besar waktu habis di network I/O ke database remote (DB_HOST_PLACEHOLDER). Jika database dipindah ke localhost, latensi diprediksi akan turun ke kisaran 200-400ms.
3.  **Scalability:** Index HNSW pada PostgreSQL bekerja sangat efektif menjaga performa tetap stabil meskipun database memiliki belasan ribu baris vektor.

## ✅ Conclusion
Arsitektur **Hybrid Semantic Search** yang dibangun saat ini sudah **Production-Ready** dari sisi efisiensi resource dan kecepatan respon.
