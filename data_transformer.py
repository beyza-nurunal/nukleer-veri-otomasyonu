import os
import pandas as pd

# ============================================
# KURUMSAL STANDARTLAR & SABİTLER (Constants)
# ============================================
OUTPUT_PADDING = 15
IDX_ENERJI = 0
IDX_DATA = 1
IDX_HATA = 3  # EXFOR standardındaki 4. sütun (0 tabanlı indeksle 3)

# ============================================
# OTOMATİK KLASÖR BULMA
# ============================================
reaksiyonlar = [
    klasor for klasor in os.listdir(".")
    if os.path.isdir(klasor) and not klasor.startswith('.')
]

# ============================================
# VERİ İŞLEME FONKSİYONU (Pipeline Core)
# ============================================
def veri_isle(dosya_yolu, reaksiyon_klasoru, dosya_adi):
    try:
        # Çıktıların ham veri klasörünü kirletmemesi için izole alt dizin oluşturuluyor
        cikti_dizini = os.path.join(reaksiyon_klasoru, "outputs")
        os.makedirs(cikti_dizini, exist_ok=True)

        # 1. HAM VERİYİ HEDEFLENEN İNDEKSLERE GÖRE OKU (Sütun Kayma Riski Sıfırlandı)
        df_ham = pd.read_csv(
            dosya_yolu,
            sep=r"\s+",
            comment="#",
            header=None,
            usecols=[IDX_ENERJI, IDX_DATA, IDX_HATA]
        )
        
        # Sütunları net olarak isimlendir
        df_ham.columns = ["Enerji", "Data", "Hata"]

        # ============================================
        # 1. EXCEL ÇIKTISI (Nokta -> Virgül Dönüşümü)
        # ============================================
        df_excel = df_ham.copy()
        for col in df_excel.columns:
            df_excel[col] = (
                df_excel[col]
                .astype(str)
                .str.strip()
                .str.replace(".", ",", regex=False)
            )

        df_excel.columns = ["Enerji (MeV)", "Data (mb)", "Hata (mb)"]
        excel_cikti = os.path.join(cikti_dizini, f"{dosya_adi}_excel.xlsx")
        df_excel.to_excel(excel_cikti, index=False)
        print(f"[BAŞARILI] Excel Dosyası -> {excel_cikti}")

        # ============================================
        # 2. ÖZEL HATA ANALİZİ ÇIKTISI (Sadece 1. ve 3. Sütun)
        # ============================================
        # Orijinal .inp dosyalarınla karışmaması için adlandırma ve konum izole edildi
        ozel_cikti = os.path.join(cikti_dizini, f"{dosya_adi}_ayiklanmis_veri.txt")

        with open(ozel_cikti, "w", encoding="utf-8") as f:
            for _, row in df_ham.iterrows():
                # Sayısal temizlik ve ondalık nokta standardı garantisi
                ene = str(row["Enerji"]).strip().replace(",", ".")
                hat = str(row["Hata"]).strip().replace(",", ".")

                # Tanımlanan padding değerine göre hizalı yazım
                f.write(f"{ene:<{OUTPUT_PADDING}} {hat}\n")

        print(f"[BAŞARILI] Ayıklanmış Veri Dosyası -> {ozel_cikti}\n")

    except Exception as e:
        print(f"[KRİTİK HATA] {dosya_yolu} işlenirken bir kesinti oluştu:")
        print(str(e))

# ============================================
# PIPELINE TETİKLEYİCİ
# ============================================
if __name__ == "__main__":
    print("=== Endüstriyel EXFOR Toplu İşleme Hattı Başlatıldı ===")
    
    for reaksiyon in reaksiyonlar:
        # Sistem klasörlerini ve sistemin kendi ürettiği çıktı klasörlerini pas geç
        if reaksiyon in ["_pycache_", "venv", "outputs"]:
            continue
            
        print(f"\nKlasör taranıyor: {reaksiyon}")

        for dosya in os.listdir(reaksiyon):
            # Sadece işlenmemiş ham veri dosyalarını hedef al
            if dosya.endswith((".txt", ".dat", ".asc", ".out")):
                
                tam_yol = os.path.join(reaksiyon, dosya)
                dosya_adi = os.path.splitext(dosya)[0]

                veri_isle(tam_yol, reaksiyon, dosya_adi)

    print("\n===========================================")
    print("Tüm endüstriyel dönüşüm işlemleri başarıyla tamamlandı.")
    print("===========================================")
