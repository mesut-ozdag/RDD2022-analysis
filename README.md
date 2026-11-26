# RDD2022-analysis

*A Quantitative Analysis of Evaluation Protocols and Reporting Completeness in RDD2022-Based Road Damage Detection Studies*

Bu depo, **"RDD2022 Tabanlı Yol Hasarı Tespiti Çalışmalarında Değerlendirme Protokolleri ve Raporlama Tamlığının Nicel Analizi"** başlıklı makalenin ek veri dosyasını, tarama ve analiz kodlarını ve kod kitaplarını içerir.

**Yazarlar:** Mesut ÖZDAĞ¹, Gökay BOYNUKISA¹, Sude Yaren ÇELİK², Esra CANPOLAT², Saliha Cansu PULAT², Meryem ÜNALDI²

¹ Karabük Üniversitesi, Bilişim Teknolojileri Meslek Yüksekokulu, Karabük, Türkiye  
² Karabük Üniversitesi, Bilgisayar ve Bilişim Bilimleri Fakültesi, Karabük, Türkiye

## İçerik

| Dosya veya klasör | Açıklama |
|---|---|
| `Supplementary_Data.xlsx` | Ek veri dosyası. README sayfası ile S1–S17 sayfalarında tarama akışı, tarama kayıtları, kayıt düzeyindeki kararlar, sınıflandırılan 297 çalışma, analiz kümesindeki 18 çalışmanın deney kayıtları, PRTİ kodları, karşılaştırılabilirlik matrisi, kontrol listesi ve kod kitapları yer alır. |
| `kod/` | Tarama ve analiz kodları, kod kitapları ve ara çıktılar. Dosyaların tek tek açıklaması `kod/BENIOKU.md` dosyasındadır. |

## Notlar

- **PRTİ (Protokol Raporlama Tamlık İndeksi):** Bu araştırma kapsamında geliştirilmiş keşfedici bir raporlama indeksidir. Kod kitabı `kod/PRTI_kod_kitabi.md` dosyasında ve Excel'in S16 sayfasındadır.
- **Eksik girdiler:** `kod/analysis.py`'nin okuduğu bazı girdi dosyaları bu depoda yoktur. Bunlar yayıncı özetlerini içeren dosyalar ile ara karar dosyalarıdır. Bu nedenle betik yalnızca bu depodaki dosyalarla yeniden çalıştırılamaz; ayrıntı için `kod/BENIOKU.md` dosyasına bakın.
- **Sorguların yeniden çalıştırılması:** Tarama sorguları `kod/openalex_search.sh` ve `kod/supp_search.py` ile yeniden çalıştırılabilir. Dizinler sürekli güncellendiği için sonuçlar makaledeki sayılarla aynı olmayabilir.
- **Kayıt düzeyindeki son kararlar:** Tümü `Supplementary_Data.xlsx` dosyasındadır.

## Lisans

MIT Lisansı; ayrıntı için `LICENSE` dosyasına bakın.

## Atıf

Makale yayımlandığında künye buraya eklenecektir.
