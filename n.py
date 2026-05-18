# Tam Otomatik Nokta Formatlayıcı (1, 2 ve 4. Sütunları Noktaya Çevirir)

def noktaya_cevir(giris, cikis):
    try:
        # Soru sormaması için değerleri buraya sabitliyoruz
        element_adi = "nd"
        kutle_no = "147"
        parcacik = "a"
        
        satirlar = [
            f"element {element_adi}\n",
            f"mass {kutle_no}\n",
            f"projectile {parcacik}\n",
            "# Ene         dEne         dSig\n"
        ]
        
        with open(giris, 'r', encoding='utf-8') as f:
            for s in f:
                s = s.strip()
                if not s or s.startswith('#') or any(x in s for x in ['Page', 'Projec', 'Reques', 'www.nds', 'SUBENT', 'AUTHOR', 'REACTION', 'QUANTITY', 'SUBP']):
                    continue
                
                p = s.split()
                if len(p) >= 4:
                    # 1, 2 ve 4. sütunları alıp virgülden noktaya çevirir
                    ene = p[0].replace(',', '.')
                    dene = p[1].replace(',', '.')
                    dsig = p[3].replace(',', '.')
                    
                    satirlar.append(f"{ene:<13}{dene:<13}{dsig}\n")
        
        with open(cikis, 'w', encoding='utf-8') as f:
            f.writelines(satirlar)
            
        print("\nTamamdır! 'n_cikti.txt' başarıyla noktaya çevrildi.")
        
    except FileNotFoundError:
        print("Hata: ham_veri.txt bulunamadı!")

noktaya_cevir('ham_veri.txt', 'n_cikti.txt')
