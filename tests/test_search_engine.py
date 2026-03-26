import pytest
import os
from search_engine import QuranHadithSearch
from dotenv import load_dotenv

# Muat variabel lingkungan dari file .env
load_dotenv()

# Database Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "dbname": os.getenv("DB_NAME")
}

@pytest.fixture(scope="module")
def engine():
    return QuranHadithSearch(DB_CONFIG)

# --- 100 TEST CASES FOR QURAN ---
QURAN_QUERIES = [
    "Allah Maha Pengasih", "Hari kiamat pasti datang", "Perintah shalat lima waktu", "Zakat untuk fakir miskin",
    "Puasa di bulan Ramadhan", "Kewajiban haji ke Baitullah", "Larangan makan bangkai", "Hukum waris anak laki-laki",
    "Kisah Nabi Musa dan Firaun", "Surga di bawah telapak kaki ibu", "Neraka Jahanam yang pedih", "Malaikat Jibril membawa wahyu",
    "Kitab Taurat dan Injil", "Kaum Ad dan Tsamud", "Penciptaan langit dan bumi", "Manusia diciptakan dari tanah",
    "Syirik dosa besar", "Berbuat baik kepada tetangga", "Larangan riba dan bunga", "Adab dalam berbicara",
    "Sabar dalam cobaan", "Bersyukur atas nikmat Allah", "Keadilan bagi semua manusia", "Larangan membunuh jiwa",
    "Hukum potong tangan bagi pencuri", "Persaksian dalam pengadilan", "Wanita yang ditalak", "Masa iddah bagi janda",
    "Anak yatim dan piatu", "Sedekah di jalan Allah", "Takwa adalah sebaik-baik bekal", "Ibadah malam tahajud",
    "Kemenangan di perang Badar", "Perang Uhud dan kekalahan", "Perjanjian Hudaibiyah", "Penaklukan kota Mekah",
    "Nabi Muhammad penutup para nabi", "Al-Quran cahaya petunjuk", "Membaca Al-Quran dengan tartil", "Hidayah milik Allah",
    "Doa Nabi Ibrahim untuk keturunan", "Kisah Nabi Yusuf dan Zulaikha", "Nabi Sulaiman dan semut", "Nabi Nuh dan bahtera",
    "Nabi Luth dan kaumnya", "Nabi Yunus di perut ikan", "Kisah Ashabul Kahfi", "Burung Ababil penghancur gajah",
    "Zikir pagi dan petang", "Istighfar memohon ampun", "Tawakal kepada Allah", "Cinta kepada Allah dan Rasul",
    "Takut kepada siksa kubur", "Syafaat Nabi di hari akhir", "Telaga Kautsar di surga", "Buah Zaqqum makanan neraka",
    "Air yang mensucikan", "Tayamum dengan debu", "Wudhu sebelum shalat", "Kiblat umat Islam",
    "Masjidil Haram dan Masjidil Aqsa", "Bulan sabit penanda waktu", "Matahari dan rembulan bersujud", "Bintang-bintang sebagai hiasan",
    "Gunung-gunung sebagai pasak", "Lautan yang luas", "Hujan sebagai rahmat", "Tumbuh-tumbuhan yang hijau",
    "Hewan ternak untuk manusia", "Madu sebagai obat", "Susu sebagai minuman", "Kurma dan anggur",
    "Pakaian yang menutup aurat", "Perhiasan dunia yang fana", "Harta dan anak adalah ujian", "Umur manusia terbatas",
    "Kematian yang tidak bisa ditunda", "Alam barzakh", "Bangkit dari kubur", "Padang Mahsyar",
    "Hisab amal perbuatan", "Mizan timbangan keadilan", "Jembatan Shirathal Mustaqim", "Melihat wajah Allah di surga",
    "Bidadari surga", "Kekal di dalam surga", "Kehidupan akhirat lebih baik", "Dunia tempat bercocok tanam",
    "Fitnah Dajjal", "Turunnya Nabi Isa", "Ya'juj dan Ma'juj", "Tiupan sangkakala pertama",
    "Tiupan sangkakala kedua", "Langit terbelah", "Bumi digoncangkan", "Gunung diterbangkan",
    "Lautan meluap", "Catatan amal diberikan", "Wajah yang berseri-seri", "Wajah yang muram"
]

# --- 100 TEST CASES FOR HADITH ---
HADITH_QUERIES = [
    "Niat dalam setiap amal", "Kebersihan sebagian dari iman", "Wudhu yang sempurna", "Shalat berjamaah di masjid",
    "Keutamaan shalat subuh", "Shalat tahajud di sepertiga malam", "Puasa senin kamis", "Sedekah sembunyi-sembunyi",
    "Senyum adalah sedekah", "Berbakti kepada orang tua", "Mencium tangan ibu", "Larangan durhaka kepada bapak",
    "Menyambung tali silaturahmi", "Adab bertamu ke rumah orang", "Menghormati tetangga", "Menjamu tamu dengan baik",
    "Larangan berkata kasar", "Berkata baik atau diam", "Kejujuran membawa keberuntungan", "Dusta membawa kehancuran",
    "Sifat amanah perawi hadits", "Menepati janji adalah ciri mukmin", "Sifat sombong dilarang", "Rendah hati atau tawadhu",
    "Sabar saat tertimpa musibah", "Syukur saat mendapat nikmat", "Keutamaan menuntut ilmu", "Ulama adalah pewaris nabi",
    "Mengamalkan ilmu yang didapat", "Menyebarkan salam", "Mendoakan orang sakit", "Mengantar jenazah ke kubur",
    "Ziarah kubur untuk ingat mati", "Makan dengan tangan kanan", "Larangan makan sambil berdiri", "Membaca bismillah sebelum makan",
    "Mencuci tangan sebelum makan", "Memakai baju dari kanan", "Melepas sepatu dari kiri", "Tidur miring ke kanan",
    "Zikir sebelum tidur", "Mimpi baik dari Allah", "Menyayangi anak kecil", "Menghormati orang tua",
    "Larangan marah-marah", "Kuat adalah yang mampu tahan amarah", "Memaafkan kesalahan orang", "Meminta maaf jika salah",
    "Ciri-ciri orang munafik", "Tanda-tanda kiamat sudah dekat", "Kemunculan Imam Mahdi", "Dajjal mata satu",
    "Turunnya Isa Al-Masih", "Siksa kubur bagi yang tidak bersih kencing", "Syafaat bagi pembaca hadits", "Keutamaan menghafal 40 hadits",
    "Jihad di jalan Allah", "Mati syahid masuk surga", "Hukum jual beli yang sah", "Larangan menipu dalam dagang",
    "Harta yang haram", "Bahaya lisan", "Ghibah memakan daging saudara", "Adu domba atau namimah",
    "Menutup aurat bagi wanita", "Adab berpakaian bagi pria", "Keutamaan menikah", "Mendidik anak dengan agama",
    "Doa setelah adzan", "Menjawab adzan", "Shalat sunnah rawatib", "Shalat witir penutup malam",
    "Puasa syawal enam hari", "Puasa arafah menghapus dosa", "Puasa asyura", "Keutamaan hari jumat",
    "Mandi jumat", "Memakai wangi-wangian", "Membaca surah Al-Kahfi", "Istighfar 70 kali sehari",
    "Cinta tanah air", "Taat kepada pemimpin", "Larangan memberontak", "Membela yang benar",
    "Keadilan penguasa", "Hak-hak pekerja", "Upah sebelum keringat kering", "Menyayangi binatang",
    "Larangan menyiksa hewan", "Memberi minum anjing yang haus", "Kucing hewan yang suci", "Waspada fitnah akhir zaman",
    "Persaudaraan sesama muslim", "Mukmin itu satu bangunan", "Tangan di atas lebih baik", "Jangan meminta-minta",
    "Keutamaan qurban", "Menyembelih dengan pisau tajam", "Haji yang mabrur", "Umrah ke umrah penghapus dosa"
]

@pytest.mark.parametrize("query", QURAN_QUERIES)
def test_search_quran(engine, query):
    """Memastikan hasil pencarian Al-Quran relevan dan terfilter benar."""
    results = engine.search(query, source="alquran", limit=5)
    
    assert len(results) > 0, f"Pencarian Quran untuk '{query}' tidak boleh kosong."
    for res in results:
        assert res["sumber"] == "Al-Quran", f"Sumber harus Al-Quran, tapi ditemukan {res['sumber']}"
        assert res["skor_relevansi"] > 0, "Skor relevansi harus positif."
        assert "judul" in res and "konten" in res, "Field judul dan konten harus ada."

@pytest.mark.parametrize("query", HADITH_QUERIES)
def test_search_hadith(engine, query):
    """Memastikan hasil pencarian Hadits relevan dan terfilter benar."""
    results = engine.search(query, source="hadist", limit=5)
    
    assert len(results) > 0, f"Pencarian Hadits untuk '{query}' tidak boleh kosong."
    for res in results:
        assert res["sumber"] == "Hadits", f"Sumber harus Hadits, tapi ditemukan {res['sumber']}"
        assert res["skor_relevansi"] > 0, "Skor relevansi harus positif."
        assert "judul" in res and "konten" in res, "Field judul dan konten harus ada."

def test_search_all(engine):
    """Memastikan hasil pencarian 'Semua' mencakup kedua sumber."""
    results = engine.search("Shalat dan Niat", source="semua", limit=20)
    
    sumber = [res["sumber"] for res in results]
    assert "Al-Quran" in sumber, "Hasil pencarian 'semua' harus mengandung Al-Quran."
    assert "Hadits" in sumber, "Hasil pencarian 'semua' harus mengandung Hadits."
