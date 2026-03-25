import requests
from typing import Tuple

def split_sanad_matan_v2(text: str) -> Tuple[str, str]:
    """
    Logika V2: Menggunakan prioritas dan sensitivitas tanda baca.
    """
    # 1. Prioritas Utama: "bersabda" dengan tanda baca (Hampir pasti awal Matan)
    # Gunakan split (dari kiri) karena sabda pertama biasanya adalah inti hadits/cerita
    for d in ["bersabda:", "bersabda;", "bersabda \"", "bersabda '"]:
        if d in text:
            parts = text.split(d, 1)
            return (parts[0] + d).strip(), parts[1].strip()

    # 2. Prioritas Kedua: Transisi kutipan perawi terakhir (Structural transition)
    # Gunakan rsplit (dari kanan) karena sanad sering mengandung kata 'berkata' berkali-kali, 
    # tapi matan dimulai setelah 'berkata' perawi terakhir (sahabat).
    quote_indicators = [
        "berkata, \"", "berkata, '", "berkata: \"", "berkata; \"", 
        "berkata, bahwa", "mengatakan, \"", "mengatakan, '"
    ]
    for d in quote_indicators:
        if d in text:
            parts = text.rsplit(d, 1)
            return (parts[0] + d).strip(), parts[1].strip()

    # 3. Prioritas Ketiga: Akhir Sanad sederhana dengan koma
    if "berkata," in text:
        parts = text.rsplit("berkata,", 1)
        return (parts[0] + "berkata,").strip(), parts[1].strip()

    # Fallback: Anggap semuanya Matan jika tidak ditemukan pola transisi yang jelas
    return "", text.strip()

def test_on_ids():
    test_ids = [4, 5, 412, 450, 451, 467]
    print(f"🧪 TESTING NEW PARSER ON {len(test_ids)} HADITHS...\n")
    
    for hid in test_ids:
        url = f"https://api.hadith.gading.dev/books/bukhari/{hid}"
        try:
            data = requests.get(url).json()["data"]["contents"]
            full_text = data["id"]
            sanad, matan = split_sanad_matan_v2(full_text)
            
            print(f"--- HADITS NO: {hid} ---")
            print(f"[SANAD]: {sanad[:150]}...{sanad[-50:] if len(sanad)>50 else ''}")
            print(f"[MATAN]: {matan[:150]}...")
            print("-" * 30 + "\n")
        except Exception as e:
            print(f"❌ Error testing ID {hid}: {e}")

if __name__ == "__main__":
    test_on_ids()
