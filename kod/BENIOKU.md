# Tarama ve analiz kodları

- `openalex_search.sh`: OpenAlex ana tarama sorguları (12 Ekim 2026); bu sorgular özet alanını istemez.
- `openalex_corpus.py`: Yanıtları birleştirir (572 benzersiz kayıt), özetleri ayrı bir sorguyla `abstract_inverted_index` alanından alır, anahtar sözcük ve tür filtresini uygular (554 kayıt).
- `hedefli_tarama_sorgulari.tsv`: 12 Ekim 2026 hedefli taramasında çalıştırılan 107 web sorgusu ve sonuç bağlantısı sayıları. Tarama, Semantic Scholar ve OpenAlex atıf sorguları, Semantic Scholar anahtar sözcük sorguları ile Europe PMC ve arXiv arayüzlerini de kullanmıştır (sayılar `Supplementary_Data.xlsx`, S2).
- `supp_search.py`: Belgelenmiş arayüz taraması (2 Kasım 2026): Crossref, arXiv, Semantic Scholar, Europe PMC. Betikte DBLP sorguları da vardır, ancak sunucu otomatik sorguları engellediğinden sonuç alınamamıştır (S2).
- `PRTI_kod_kitabi.md`: PRTİ ölçütleri, uygulama kuralları, kontrol listesi alt maddeleri ve karşılaştırılabilirlik değişkenleri.
- `katki_turu_kod_kitabi.md`: Katkı türü kod kitabı. 297 çalışmanın katkı türleri bu kod kitabıyla, başlık ve özetten (derlenen özetler arasında yer almayan 28 çalışmada kanıt notu ve kısa özetten) iki kez kodlanmış, uyuşmayan 30 çalışmada karar aynı kodlayıcının üçüncü bir değerlendirmesiyle verilmiştir.
- `katki_kodlama_v4_ham.json`: Katkı türü kodlamasının iki değerlendirmesi (`A`, `B`), üçüncü değerlendirmenin kararları (`ADJ`), son kodlar (`final`) ve kararın kaynağı (`src`).
- `analysis.py`: Çalışma listesini birleştirir ve analiz sayılarının büyük bölümünü hesaplar; tarama akışının sayıları (Tablo 1, S1) kayıtlardan elle aktarılmıştır.
- `figs_v3.py`: Şekiller. Kullanım: `python3 figs_v3.py ÇIKTI_KLASÖRÜ`. Times New Roman yazı tipi ister; yazı tipi yolu macOS içindir.
- `labels_tr.py`, `matrix_cells.py`: Kodların Türkçe etiketleri ile Tablo 7 ve S11’in hücre metinleri.
- `recheck_coders.json`: 91 kayıtlık üçüncü denetimde iki değerlendirmenin kararı ve kanıt düzeyi.
- `results.json`: `analysis.py` çıktısı; makaledeki analiz sayılarının çoğu bu dosyadan alınmıştır.
- `prti_final_v2.json`: 31 çalışmanın uygulama kuralları sonrası PRTİ kodları, kanıt notları ve deney kayıtları.
- `tarayici_3kasim.json`: Teyit edilemeyen 51 kaydın yayıncı sayfalarının 3 Kasım 2026’da yeniden kontrol edilmesinin kayıt bazında sonucu.

S10’daki, `recheck_coders.json` ve `katki_kodlama_v4_ham.json` dosyalarındaki iki kodlama aynı kodlayıcının farklı zamanlarda yaptığı iki ayrı değerlendirmedir; bağımsız kodlayıcı sayılmazlar (makale, Bölüm 2.2.3 ve 2.2.5).

`analysis.py`’nin okuduğu girdi dosyaları bu pakette yoktur; bu nedenle betik yalnızca paketle yeniden çalıştırılamaz. Özet metinlerini içeren `corpus.json` ve `abstract_alt.json` ile ara özet dosyaları, yayıncı metinlerini barındırdığı için paylaşılmamıştır. Ara karar ve veri çıkarım dosyaları (`papers.json`, `use_status_interim.json`, `wf_main.json`, `new_candidates.json`, `prti_final.json`, `analysis_18.json`, `wf1_result.json`, `verify_auto_from_deep.json`, `rescreen.json`, `recheck.json`, `deep_result.json`, `deep_targets.json`) da pakette bulunmamaktadır. Sorgular `openalex_search.sh` ve `supp_search.py` ile yeniden üretilebilir; sonuçlar ise dizinler güncellendiği için aynı olmayabilir. OpenAlex, 12 Ekim 2026 sonrasında arXiv ve dergi kayıtlarını birleştirmiştir; 2 Kasım 2026’da iki kimlik de aynı 221 kaydı döndürmektedir. 12 Ekim ham yanıtları (`oa/`) saklanmamış, `corpus.json` 2 Kasım 2026’da tarama kayıtlarından yeniden oluşturulmuştur. Kayıt düzeyindeki son kararlar `Supplementary_Data.xlsx` dosyasındadır. İki değerlendirmenin ayrı PRTİ kodları yalnızca analiz kümesindeki 18 çalışma için bu dosyada (S10) verilmiştir. Üçüncü denetimde OpenAlex kayıtlarının kanıtı ve iki değerlendirmenin kararı S7’de, diğer kayıtların iki kodu `recheck_coders.json` dosyasındadır.

Google Scholar’daki atıf sayısı (489) yalnızca çapraz kontrol için okunmuş, makalede kullanılmamıştır (S2).
