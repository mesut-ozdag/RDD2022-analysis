# Protokol Raporlama Tamlık İndeksi (PRTİ): Kod Kitabı

Sürüm: 2 Kasım 2026. PRTİ, bu araştırma kapsamında geliştirilmiş keşfedici bir raporlama indeksidir. Aşağıdaki ölçüt tablosu, kontrol listesi alt maddeleri ve karşılaştırılabilirlik değişkenleri çalışmalar kodlanmadan önce sabitlenmiştir; “Uygulama kuralları” bölümü indeksin geliştirilmesi sürecinde eklenmiştir.
Ölçülen şey başarım değil, makalenin RDD2022 deneyini ne kadar eksiksiz raporladığıdır.
Her ölçüt 0 veya 1 puandır; toplam 0-8. Makalede açıkça bulunamayan bilgi 0 sayılır.
Değerlendirme yalnızca makalenin kendi metni, tabloları, ekleri ve makalenin verdiği bağlantılar üzerinden yapılır.

| Kod | Ölçüt | 1 puan koşulu | 0 puan örnekleri | Gerekçe |
|---|---|---|---|---|
| K1 | Ülke alt kümesi | Deneyde kullanılan RDD2022 ülke alt kümeleri adlarıyla veya "altı ülkenin tamamı" biçiminde belirtilmiş | Yalnızca "RDD2022 kullanıldı" | Alt kümeler görüntü kaynağı ve sınıf dağılımı bakımından farklıdır |
| K2 | Veri bölmesi | Raporlanan deneyin eğitim/doğrulama(/test) oranı veya görüntü sayıları verilmiş ve verilen sayılar kendi içinde ve RDD2022 ile çelişmiyor | Bölme yok; sayılar çelişiyor | Başarım bölmeye bağlıdır |
| K3 | Hasar sınıfları | Değerlendirmede kullanılan sınıflar ad veya kodla sıralanmış, sınıf sayısı bellidir | Yalnızca "dört sınıf" | Sınıf kümesi mAP değerini doğrudan etkiler |
| K4 | Metrik ve IoU | Ana metrik adlandırılmış ve IoU eşiği açıkça verilmiş (mAP@0.5, mAP50, AP50, F1@IoU>0,5 gibi) | Eşiksiz "mAP" | Eşiksiz değerler karşılaştırılamaz |
| K5 | Tekrar bilgisi | Rastgele tohum değeri verilmiş ya da deney en az iki kez tekrarlanıp ortalama/sapma raporlanmış | Tek çalıştırma, tohum yok | Tek çalıştırmadaki 1-2 puanlık fark gürültü olabilir |
| K6 | Donanım ve eğitim ayarları | GPU/donanım modeli ve şu beşten en az üçü verilmiş: epok, yığın boyutu, öğrenme oranı, eniyileyici, girdi boyutu | Yalnızca biri | Yeniden çalıştırma için gerekir |
| K7 | Kod veya ağırlık | Makalede herkese açık kod ya da model ağırlığı bağlantısı var | "İstek üzerine", bağlantı yok | Bağımsız sınamayı mümkün kılar |
| K8 | Test protokolü | (a) Resmî gizli testte değerlendirilmiş, ya da (b) doğrulamadan ayrı bir test kümesi var ve üyeliği yeniden kurulabilir (görüntü listesi/bölme dosyası paylaşılmış ya da bölme tohumu verilmiş) | Doğrulama kümesi test sayılmış; yalnızca rastgele oran, tohum yok | Başkası aynı testi kuramıyorsa sonuç sınanamaz |

## Uygulama kuralları

Aşağıdaki kurallar, yukarıdaki tablonun kapsamadığı sınır durumlar için yazılı hâle getirilmiştir. Ana deney ve K7 kuralları kodlayıcıların kodlama sırasında izlediği uygulamayı yazıya döker ve hiçbir kararı değiştirmemiştir. K2 ve K6 kuralları ise PRTİ keşfedici bir indeks olduğundan indeksin geliştirilmesi sürecinde netleştirilmiştir. Kurallar tablodaki ölçütleri değiştirmez, nasıl uygulanacaklarını açıklar; makalenin 2.2.5 numaralı bölümünde de belirtilmiştir.

- Puanlama makalenin ana RDD2022 deneyine göre yapılır. Yan deneylerdeki eksikler ana deneyin puanını düşürmez.
- K2'de çelişki, parçalar ile toplam arasında %1'i aşan farkı ya da resmî sayıdan küçük bir sayının, seçim yapıldığı yazılmadan kullanılmasını ifade eder.
- K6'da makale tur sayısını epok anlamında kullanıyorsa bu değer epok sayılır.
- K7'de bağlantı, raporlanan RDD2022 deneyine ait kodu veya ağırlığı göstermelidir. Önceki bir çalışmanın kodunu içeren bağlantı yeterli değildir.

Bu kurallarla üç karar değişmiştir (K2'de iki, K6'da bir). İlk ve son kararlar ek veri dosyasının S10 sayfasındadır. K2'de seçim yapıldığının yazılması yeterli sayılmayıp seçimin nedeni de aransaydı [14] ve [9] da 0 alır, K2 için karşılanma sayısı 8/18, toplam puan ortancası 4 olurdu.

## Kontrol listesi alt maddeleri (Evet/Hayır)

- C1a dört resmî sınıf (D00, D10, D20, D40) ana sonuçta tam olarak kullanılmış; C1b ek sınıf varsa sınıf bazında ayrı raporlanmış.
- C2a resmî gizli test F1 skoru verilmiş; C2b ülke bazında F1 verilmiş.
- C3a bölme oranı veya sayısı verilmiş; C3b kullanılan alt kümeler adlandırılmış; C3c görüntü listesi/bölme dosyası paylaşılmış.
- C4a mAP@0.5 verilmiş; C4b mAP@0.5:0.95 verilmiş; C4c en az üç tekrarın ortalama ve sapması verilmiş.
- C5a parametre sayısı; C5b GFLOPs; C5c görüntü başına süre/FPS; C5d sürenin ön ve son işlemi kapsadığı belirtilmiş; C5e donanım.
- C6a kod paylaşılmış; C6b ağırlık paylaşılmış.

## Karşılaştırılabilirlik değişkenleri

Alt küme listesi; Çin türü (İHA, motosiklet, ikisi, belirtilmemiş); ana sonuçtaki sınıf sayısı ve adları; bölme tanımı;
test tanımı (Resmî gizli, Test bölmesi tanımlı, Doğrulama test sayılmış, Tanımsız; dış test değeri analiz kümesinde kullanılmamıştır); girdi boyutu; ana sonuç değerleri ve hangi deneye ait olduğu.
