# API Contract: Tanya Quran Hadist (v1.1)

Dokumen ini mendefinisikan standar interaksi data antara Frontend dan Backend untuk proyek **Tanya Quran Hadist**. API ini dirancang untuk mendukung pencarian semantik berkecepatan tinggi dan navigasi dataset suci yang efisien.

---

## 🏗️ Architectural Decisions (The Logic)

1.  **Hybrid Pagination:** Karena kita menggunakan pencarian vektor, skor relevansi akan menurun seiring bertambahnya halaman. Batas **10 halaman (100 hasil)** ditetapkan untuk menjaga presisi dan kecepatan respon.
2.  **Vector-Based Recommendations:** Rekomendasi di halaman detail tidak menggunakan kategori statis, melainkan melakukan pencarian tetangga terdekat (*Nearest Neighbor*) menggunakan `pgvector` untuk menemukan konten dengan bahasan serupa secara otomatis.
3.  **Quran Contextual Scrolling:** Navigasi Al-Quran menggunakan `next_id` dan `prev_id` berbasis urutan fisik database (1-6236) untuk memungkinkan implementasi *lazy-load* yang mulus di sisi frontend.
4.  **Highlighting Strategy:** Backend akan mengirimkan potongan teks (*snippet*) yang mengandung penanda highlight (`<em>`) untuk kata-kata yang memiliki kecocokan leksikal dengan kueri pengguna.
5.  **Server-Side Image Rendering:** Untuk menjamin kualitas tipografi Arab dan konsistensi branding, rendering gambar 1:1 dilakukan di sisi server melalui endpoint khusus.

---

## 🚀 Endpoints Summary

| Endpoint | Method | Purpose |
| :--- | :--- | :--- |
| `/api/v1/search` | GET | Global search lintas sumber dengan pagination. |
| `/api/v1/quran/{id}` | GET | Detail ayat Al-Quran + Rekomendasi + Navigasi tetangga. |
| `/api/v1/hadith/{id}` | GET | Detail hadits + Rekomendasi serupa. |
| `/api/v1/share/image` | GET | Menghasilkan gambar 1:1 untuk ayat/hadits tertentu. |

---

## 📋 Endpoint Details

### 1. Global Search
**`GET /api/v1/search`**

Mencari konten Al-Quran dan Hadits berdasarkan kueri semantik.

**Query Parameters:**
- `q` (string, required): Kata kunci pencarian.
- `source` (string, optional): Pilihan sumber (`semua`, `alquran`, `hadist`). Default: `semua`.
- `page` (integer, optional): Nomor halaman (1-10). Default: `1`.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "meta": {
    "query": "shalat",
    "total_results": 120,
    "current_page": 1,
    "per_page": 10,
    "max_pages": 10
  },
  "results": [
    {
      "id": 153,
      "sumber": "Al-Quran",
      "judul": "QS. Al-Baqarah: 153",
      "snippet": "Wahai orang-orang yang beriman! Mohonlah pertolongan (kepada Allah) dengan <em>sabar</em> dan <em>shalat</em>...",
      "skor_relevansi": 98.5,
      "detail_url": "/api/v1/quran/153"
    }
  ]
}
```

---

### 2. Quran Detail
**`GET /api/v1/quran/{id}`**

Mengambil satu ayat spesifik beserta konteks navigasi dan rekomendasi bahasan serupa.

**Path Parameters:**
- `id` (integer, required): ID internal ayat (1-6236).

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "id": 153,
    "surah": "Al-Baqarah",
    "nomor_surah": 2,
    "nomor_ayat": 153,
    "juz": 2,
    "teks_arab": "يَا أَيُّهَا الَّذِينَ آمَنُوا اسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ...",
    "terjemah": "Wahai orang-orang yang beriman! Mohonlah pertolongan (kepada Allah) dengan sabar dan shalat...",
    "tafsir": "Allah memerintahkan hamba-Nya untuk bersabar...",
    "navigation": {
      "prev_id": 152,
      "next_id": 154
    },
    "share": {
      "text_copy": "QS. Al-Baqarah: 153 - Wahai orang-orang yang beriman...",
      "image_api_url": "/api/v1/share/image?type=quran&id=153"
    }
  },
  "recommendations": [
    {
      "id": 45,
      "sumber": "Hadits",
      "judul": "HR. Bukhari No. 45",
      "konten": "Shalat adalah tiang agama...",
      "skor_kemiripan": 92.1
    }
  ]
}
```

---

### 3. Hadith Detail
**`GET /api/v1/hadith/{id}`**

Mengambil detail satu hadits lengkap dengan pemisahan sanad/matan dan rekomendasi.

**Path Parameters:**
- `id` (integer, required): ID internal hadits.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "kitab": "Shahih Bukhari",
    "nomor_hadits": 1,
    "derajat": "Shahih",
    "teks_arab": "حَدَّثَنَا الْحُمَيْدِيُّ...",
    "sanad": "Telah menceritakan kepada kami Al-Humaidi...",
    "matan": "Sesungguhnya setiap amal tergantung pada niatnya...",
    "terjemah_full": "Telah menceritakan kepada kami... Sesungguhnya setiap amal...",
    "share": {
      "text_copy": "HR. Bukhari No. 1 - Sesungguhnya setiap amal tergantung pada niatnya...",
      "image_api_url": "/api/v1/share/image?type=hadith&id=1"
    }
  },
  "recommendations": [
    {
      "id": 1,
      "sumber": "Al-Quran",
      "judul": "QS. Al-Fatihah: 1",
      "konten": "Dengan menyebut nama Allah...",
      "skor_kemiripan": 88.4
    }
  ]
}
```

---

### 4. Share Image Generator
**`GET /api/v1/share/image`**

Menghasilkan file gambar (PNG/JPG) berdasarkan konten ayat atau hadits.

**Query Parameters:**
- `type` (string, required): Tipe konten (`quran` atau `hadith`).
- `id` (integer, required): ID konten.
- `content_mode` (string, optional): `arab`, `translation`, atau `both`. Default: `both`.
- `show_branding` (boolean, optional): Menampilkan watermark branding. Default: `true`.

**Success Response (200 OK):**
- **Content-Type:** `image/png`
- **Body:** Binary image data.

---

## 🛠️ Error Codes Standard

| Code | Message | Description |
| :--- | :--- | :--- |
| 400 | Bad Request | Parameter kueri tidak valid atau hilang. |
| 404 | Not Found | Data Al-Quran/Hadits dengan ID tersebut tidak ditemukan. |
| 500 | Server Error | Terjadi kesalahan pada proses embedding atau koneksi database. |
