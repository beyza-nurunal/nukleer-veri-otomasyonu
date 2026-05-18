# Akıllı ve Sorunsuz Otomatik Format Değiştirici

def otomatik_cevir(giris, cikis):
    try:
        element_adi = "Bilinmeyen"
        kutle_no = "X"
        parcacik = "a" # Genelde alfa çalıştığın için varsayılan alfa
        
        satirlar = []
        veri_basladi = False
        
        with open(giris, 'r', encoding='utf-8') as f:
            for s in f:
                s = s.strip()
                if not s:
                    continue
                
                # REACTION satırından element ve kütleyi otomatik cımbızlıyoruz
                if "REACTION" in s:
                    try:
                        # Örn: 60-ND-0(A,X)60-ND-147 -> Buradan Nd ve 147'yi ayıklar
                        parcalar = s.split()
                        reaksiyon_metni = parcalar[1]
                        if "-" in reaksiyon_metni:
                            element_adi = reaksiyon_metni.split("-")[1].strip().lower()
                        if "147" in s or "-" in s:
                            kutle_no = s.split("-")[-1].split()[0].strip()
                    except:
                        pass # Bir hata olursa varsayılan değerlerde kalır
                
                # Web sitesi dipnotlarını eliyoruz
                if any(x in s for x in ['Page', 'Projec', 'Reques', 'www.nds']):
                    continue
                
                # Sayısal verilerin başladığı yeri yakalıyoruz
                p = s.split()
                if len(p) >= 4 and p[0].replace('.', '', 1).isdigit():
                    veri_basladi = True
                    # 1, 2 ve 4. sütunları alıp noktayı virgüle çeviriyoruz
                    ene = p[0].replace('.', ',')
                    dene = p[1].replace('.', ',')
                    dsig = p[3].replace('.', ',')
                    satirlar.append(f"{ene:<13}{dene:<13}{dsig}\n")
        
        # Akıllı başlıkları listenin en başına enjekte ediyoruz
        basliklar = [
            f"element {element_adi}\n",
            f"mass {kutle_no}\n",
            f"projectile {parcacik}\n",
            "# Ene         dEne         dSig\n"
        ]
        tam_liste = basliklar + satirlar
        
        with open(cikis, 'w', encoding='utf-8') as f:
            f.writelines(tam_liste)
            
        print("\nTamamdır! Hiçbir şey sormadan 'v_cikti.txt' dosyasını doldurdum.")
        
    except FileNotFoundError:
        print("Hata: ham_veri.txt bulunamadı!")

otomatik_cevir('ham_veri.txt', 'v_cikti.txt')
