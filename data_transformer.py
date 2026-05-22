import os
import re
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter
import sys

print("==================================================")
print("SISTEM KONTROLU BASLIYOR...")
print(f"Klasor: {os.getcwd()}")
print("==================================================")

# ============================================
# LD MODEL SAYISI
# ============================================
try:
    ld_sayisi = int(input("Kac adet TALYS LDModel sutunu/input'u olusturulsun?: "))
except ValueError:
    print("HATA: Lutfen sadece bir sayi girin! Program kapatiliyor.")
    sys.exit()

# ============================================
# REAKSIYON KLASORLERI
# ============================================
reaksiyonlar = [
    k for k in os.listdir(".")
    if os.path.isdir(k) and not k.startswith(".") and k not in ["_pycache_", "venv", "outputs"]
]

if not reaksiyonlar:
    print("\nHATA: Bu klasorde hicbir reaksiyon klasoru bulunamadi!")
    sys.exit()
else:
    print(f"BILGI: {len(reaksiyonlar)} adet klasor bulundu.")

# ============================================
# YAZAR VE YIL FORMATLAYICI
# ============================================
def yazar_yil_bul(dosya_yolu):
    dosya_adi = os.path.basename(dosya_yolu)
    temiz_ad = os.path.splitext(dosya_adi)[0]

    yil_match = re.search(r'(19\d{2}|20\d{2})', temiz_ad)
    yil = yil_match.group(1) if yil_match else ""
    yazar = ""

    try:
        with open(dosya_yolu, "r", encoding="utf-8", errors="ignore") as f:
            for satir in f:
                satir_ust = satir.upper()

                if "AUTHOR" in satir_ust:
                    parcalar = satir_ust.split("AUTHOR")

                    if len(parcalar) > 1:
                        isim_ham = satir[satir_ust.find("AUTHOR") + 6:]
                        isim_kismi = isim_ham.lstrip('S \t:=')
                        yazar = isim_kismi.split(',')[0].strip()

                if not yil and re.search(r'\b(19\d{2}|20\d{2})\b', satir):
                    ym = re.search(r'\b(19\d{2}|20\d{2})\b', satir)

                    if ym and "AUTHOR" not in satir_ust and "MEV" not in satir_ust:
                        yil = ym.group(1)

                if yazar and yil:
                    break

    except Exception:
        pass

    if not yazar:
        kelimeler = re.findall(r'[a-zA-Z]+', temiz_ad)

        for kelime in kelimeler:
            if len(kelime) > 2 and kelime.lower() not in [
                'txt', 'dat', 'asc', 'out', 'csv', 'mev', 'data'
            ]:
                yazar = kelime.capitalize()
                break

    if not yazar:
        yazar = temiz_ad

    if yil:
        return f"{yazar} vd. {yil}"
    else:
        return f"{yazar} vd."

# ============================================
# TALYS INPUT & ENERJI DOSYASI OLUSTURUCU
# ============================================
def talys_dosyalari_olustur(klasor_adi, ld_sayisi, ortak_enerjiler):

    match = re.search(r'\d+-([A-Za-z]+)-(\d+)\(([A-Za-z]+),', klasor_adi)

    if match:
        element = match.group(1).lower()
        mass = match.group(2)
        projectile = match.group(3).lower()
    else:
        element = "xx"
        mass = "0"
        projectile = "x"

    enerji_dosya_yolu = os.path.join(klasor_adi, "enerji")

    with open(enerji_dosya_yolu, "w", encoding="utf-8") as f:
        for e in ortak_enerjiler:
            f.write(f"{e}\n")

    for ld in range(1, ld_sayisi + 1):

        inp_icerik = f"""#
#reaction {klasor_adi}
#
projectile {projectile}
element {element}
mass {mass}
energies enerji
ldmodel {ld}
legacy y
"""

        inp_dosya_yolu = os.path.join(
            klasor_adi,
            f"input_ld{ld}.inp"
        )

        with open(inp_dosya_yolu, "w", encoding="utf-8") as f:
            f.write(inp_icerik.strip() + "\n")

# ============================================
# VERI OKU
# ============================================
def veri_oku(dosya_yolu):

    df = pd.read_csv(
        dosya_yolu,
        sep=r"\s+",
        comment="#",
        header=None,
        engine="python"
    )

    toplam = df.shape[1]

    if toplam == 2:
        df = df.iloc[:, [0, 1]]

    elif toplam == 3:
        df = df.iloc[:, [0, 2]]

    else:
        df = df.iloc[:, [0, 2, 3]]

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

# ============================================
# MASTER EXCEL OLUSTURMA
# ============================================
excel_yolu = "MASTER_EXFOR.xlsx"

wb = Workbook()
wb.remove(wb.active)

sari_dolgu = PatternFill(
    start_color="FFFF00",
    end_color="FFFF00",
    fill_type="solid"
)

kalin_font = Font(bold=True)

merkez_hizalama = Alignment(
    horizontal="center",
    vertical="center"
)

islenen_klasor_sayisi = 0

for reaksiyon in reaksiyonlar:

    dosyalar = [
        d for d in os.listdir(reaksiyon)
        if d.endswith((".txt", ".dat", ".asc", ".out"))
    ]

    if not dosyalar:
        continue

    print(f"Islemler Yurutuluyor: {reaksiyon}")

    sayfa_adi = reaksiyon[:31].replace(":", "").replace("/", "")
    ws = wb.create_sheet(title=sayfa_adi)

    ortak_enerjiler = []

    current_col = 1

    # ============================================
    # EXCEL'E VERILERI YAZ
    # ============================================
    for dosya in dosyalar:

        tam_yol = os.path.join(reaksiyon, dosya)

        df = veri_oku(tam_yol)

        baslik_yazisi = yazar_yil_bul(tam_yol)

        sutun_sayisi = df.shape[1]

        ws.cell(
            row=1,
            column=current_col,
            value=baslik_yazisi
        )

        ws.merge_cells(
            start_row=1,
            start_column=current_col,
            end_row=1,
            end_column=current_col + sutun_sayisi - 1
        )

        ws.cell(row=1, column=current_col).alignment = merkez_hizalama
        ws.cell(row=1, column=current_col).font = kalin_font

        alt_basliklar = [
            "Enerji (MeV)",
            "Data (mb)",
            "Hata (mb)"
        ]

        for i in range(sutun_sayisi):

            baslik = (
                alt_basliklar[i]
                if i < len(alt_basliklar)
                else f"Sutun {i+1}"
            )

            c = ws.cell(
                row=2,
                column=current_col + i,
                value=baslik
            )

            c.alignment = merkez_hizalama
            c.font = Font(bold=False)

        for row_idx, row_data in enumerate(df.values):

            for col_idx, val in enumerate(row_data):

                if pd.notna(val):

                    ws.cell(
                        row=row_idx + 3,
                        column=current_col + col_idx,
                        value=val
                    )

        ortak_enerjiler.extend(
            df.iloc[:, 0].dropna().tolist()
        )

        current_col += sutun_sayisi

    # ============================================
    # ORTAK ENERJILER SUTUNU
    # ============================================
    ortak_enerjiler = sorted(list(set(ortak_enerjiler)))

    ws.cell(row=1, column=current_col).fill = sari_dolgu
    ws.cell(row=2, column=current_col).fill = sari_dolgu

    for row_idx, val in enumerate(ortak_enerjiler):

        c = ws.cell(
            row=row_idx + 3,
            column=current_col,
            value=val
        )

        c.fill = sari_dolgu

    current_col += 1

    # ============================================
    # TALYS EXCEL SUTUNLARI
    # ============================================
    for ld in range(1, ld_sayisi + 1):

        # ÜST BAŞLIK
        ws.merge_cells(
            start_row=1,
            start_column=current_col,
            end_row=1,
            end_column=current_col + 1
        )

        c1 = ws.cell(
            row=1,
            column=current_col,
            value=f"TALYS 2.0 (AOMP{ld})"
        )

        c1.alignment = merkez_hizalama
        c1.font = Font(bold=True)

        # ALT BAŞLIKLAR
        c2 = ws.cell(
            row=2,
            column=current_col,
            value="Enerji (MeV)"
        )

        c2.alignment = merkez_hizalama

        c3 = ws.cell(
            row=2,
            column=current_col + 1,
            value="Data (mb)"
        )

        c3.alignment = merkez_hizalama

        current_col += 2

    # ============================================
    # SUTUN GENISLIKLERI
    # ============================================
    for col in range(1, current_col):

        ws.column_dimensions[
            get_column_letter(col)
        ].width = 16

    # ============================================
    # TALYS DOSYALARINI OLUSTUR
    # ============================================
    talys_dosyalari_olustur(
        reaksiyon,
        ld_sayisi,
        ortak_enerjiler
    )

    islenen_klasor_sayisi += 1

# ============================================
# KAYDETME
# ============================================
if islenen_klasor_sayisi > 0:

    try:
        wb.save(excel_yolu)

        print("\nISLEM BASARIYLA TAMAMLANDI")
        print(f"Rapor Dosyasi: '{excel_yolu}'")
        print("TALYS ve enerji dosyalari ilgili dizinlere eklendi.")

    except PermissionError:
        print("\nHATA: Dosya kaydedilemedi, Excel su an acik durumda.")

else:
    print("\nUYARI: Icerisinde veri dosyasi barindiran gecerli bir klasor bulunamadi.")

