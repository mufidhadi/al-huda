# Design Document: Tanya Quran Hadist (Pure Search Experience)

Dokumen ini mendefinisikan bahasa desain, alur pengguna (UX), dan spesifikasi antarmuka (UI) untuk proyek **Tanya Quran Hadist**. Fokus utama adalah menciptakan replikasi pengalaman Google Search pada mobile browser untuk meminimalkan kurva pembelajaran pengguna.

---

## 🎨 Design Philosophy: "The Invisibility of UI"
Aplikasi ini tidak berusaha untuk terlihat cantik secara dekoratif, melainkan **terlihat familiar secara fungsional**. 
- **Zero Friction:** Pengguna tidak perlu belajar cara menggunakan aplikasi.
- **Speed First:** Konten adalah raja; UI hanyalah pelayan yang harus tidak terlihat (*invisible*).
- **Mobile-Centric:** Navigasi dirancang untuk satu tangan (thumb-friendly).

---

## 🛠️ Design Tokens (Google-Style)
- **Background:** Pure White (`#FFFFFF`).
- **Surface/Header:** Subtle Gray Line (`#F2F2F2`) untuk pemisah.
- **Primary Text (Titles):** Link Blue (`#1A0DAB`) - Digunakan untuk judul ayat/hadits.
- **Secondary Text (Source):** Dark Green/Gray (`#202124`) - Untuk label Al-Quran/Hadits.
- **Snippet Text:** Gray (`#4D5156`) - Untuk potongan terjemahan.
- **Highlight Text:** Bold atau darker gray.
- **Typography:** System Sans-Serif (Google menggunakan Roboto/Product Sans, kita menggunakan Inter).

---

## 📱 Page Specifications

### 1. Home Page (The Gateway)
**Tujuan:** Fokus 100% pada niat pencarian pengguna.
- **Layout:** Sangat sparse (luas).
- **Logo:** Teks "Tanya Quran Hadist" di tengah atas dengan ukuran proporsional.
- **Search Bar:** Pill-shaped (bulat sempurna) dengan shadow sangat halus. Berisi icon kaca pembesar dan input teks.
- **Call to Action:** Tombol "Cari" yang bersih di bawah search bar atau terintegrasi di dalam bar.
- **UX Behavior:** Autofocus pada search bar saat halaman dimuat.

### 2. Results Page (The Discovery)
**Tujuan:** Memberikan jawaban cepat dengan format daftar klasik.
- **Sticky Header:** Search bar tetap berada di atas saat di-scroll.
- **Source Tabs:** Tab bar di bawah header [Semua, Al-Quran, Hadits]. Aktifkan indikator garis bawah biru tebal pada tab terpilih.
- **Result Item:**
    - Source Label: Abu-abu kecil di atas judul.
    - Title: Biru besar (clickable). Contoh: "QS. Al-Baqarah: 153" atau "HR. Bukhari No. 1".
    - Arabic Snippet (Optional): Teks Arab 1 baris (jika Al-Quran).
    - Translation Snippet: Potongan teks terjemahan dengan **highlight** pada kata yang relevan.
- **Note:** Tidak ada tombol interaksi (share/favorit) pada halaman ini untuk menjaga kemurnian alur pencarian.
- **Pagination:** Angka 1-10 di bagian bawah dengan desain minimalis.

### 3. Detail Page (The Knowledge)
**Tujuan:** Konsumsi teks secara mendalam dan eksplorasi kontekstual.
- **Main Content:** Teks Arab berukuran besar (24px+) diikuti terjemahan dan tafsir yang bersih.
- **Share Action:** Satu tombol "Share" minimalis yang terletak di akhir konten utama (sebelum bagian rekomendasi). Ini adalah satu-satunya tempat fitur sharing tersedia.
- **Quran Contextual Scroll (Lazy Load):**
    - Saat pengguna scroll ke atas, sistem memuat ayat sebelumnya secara otomatis.
    - Saat scroll ke bawah habis, sistem memuat ayat selanjutnya.
    - User merasa sedang membaca Mushaf yang tidak terputus.
- **Recommendation Engine (Discovery):**
    - Judul: "Bahasan Serupa" atau "Mungkin Anda Mencari".
    - List hasil serupa (cross-source) di bawah konten utama, menggunakan gaya visual Results Page.

---

## 🧠 User Experience Strategy (Google Expectation)

1.  **Instant Feedback:** Menampilkan *loading skeleton* yang mirip dengan pola teks asli agar transisi terasa instan.
2.  **Standard Gestures:** Swipe back untuk kembali ke hasil pencarian, tap logo untuk kembali ke home.
3.  **No Distractions:** Menghapus semua tombol 'Like', 'Share', atau 'Save' dari tampilan utama untuk menjaga kemurnian antarmuka pencarian.
4.  **Semantic Ranking:** Hasil teratas harus yang paling relevan secara makna (Semantic Search), bukan sekadar urutan nomor.

---

## 📤 Share Engine & Aesthetics

Fitur berbagi dirancang untuk memfasilitasi penyebaran konten religi dengan estetika yang tinggi tanpa mengganggu pengalaman pencarian murni.

### 1. Format Berbagi
- **Teks Murni:** Salinan teks mentah yang diformat dengan struktur: `[Teks Arab (opsional)] - [Terjemahan (opsional)] - [Sumber (Link)]`.
- **Gambar 1:1 (Square):** Rendering teks ke dalam kanvas persegi untuk Instagram/Status media sosial.
    - **Background:** Solid white atau tekstur kertas sangat halus.
    - **Typography:** Teks Arab menggunakan font Naskh yang elegan, terjemahan menggunakan Inter (Sans-serif).
    - **Watermark:** Link aplikasi 'tanyaquran.id' di pojok bawah.

### 2. Share Settings (Bottom Sheet)
Saat tombol "Share" ditekan, muncul *Bottom Sheet* minimalis dengan opsi:
- **Pilih Konten:** [Arab saja], [Terjemah saja], [Arab & Terjemah].
- **Format:** [Gambar (Share Image)], [Salin Teks (Copy Text)].
- **Branding Toggle:** Switch "Sertakan Label Aplikasi" (Default: ON).

### 3. Visual Layout Gambar Sharing
- Header: Label sumber (Contoh: Al-Quran atau Hadits) dengan ukuran kecil.
- Center: Teks Arab & Terjemahan dengan perataan tengah (Centered).
- Footer: Referensi (Contoh: QS. Al-Baqarah: 153) dan watermark branding.

---

## 🏁 Technical Goal
Frontend harus dibangun dengan framework yang mendukung **Server-Side Rendering (SSR)** atau **Hydration** cepat (seperti Next.js atau Remix) agar indeksibilitas dan kecepatan muat awal menyerupai Google Search.
