# Katkı türü kod kitabı

Her çalışma, başlığı ve özeti (kodlama için derlenen özetler arasında yer almayan çalışmalarda kullanım teyidinde kaydedilen kanıt notu ve kısa özet) okunarak kodlanır. Yalnızca metnin çalışmanın kendi katkısı veya yöntemi olarak açıkça belirttiği türler kodlanır; kullanılan modelin adından çıkarım yapılmaz. Bir çalışma birden fazla türe girebilir. Hiçbir tür uymuyorsa “Diğer” kodlanır.

| Kod | Ad | 1 verilme koşulu |
|---|---|---|
| architecture-improvement | Mimari iyileştirme | Bir dedektörün omurga, boyun, başlık, blok veya evrişim yapısında değişiklik ya da yeni bir ağ yapısı öneriliyor. Dikkat, boyun veya hafifletme amaçlı yapısal değişiklikler de bu koda girer. Yalnızca eğitim ayarı, veri veya kayıp değişikliği bu kodu almaz. |
| attention-module | Dikkat modülü | Kanal, uzamsal veya öz-dikkat mekanizması (ör. SE, CBAM, CA, EMA, dönüştürücü dikkat bloğu) eklenmesi ya da değiştirilmesi katkı olarak belirtiliyor. Hazır bir dönüştürücü dedektörün (ör. RT-DETR) değiştirilmeden kullanılması bu kodu almaz. |
| lightweight/edge | Hafif model / uç cihaz | Parametre, hesaplama yükü veya model boyutunun azaltılması, çıkarım hızının artırılması ya da mobil, gömülü veya uç cihazda çalıştırma açık bir hedef olarak belirtiliyor. |
| neck/feature-fusion | Boyun / öznitelik füzyonu | Boyun yapısı veya çok ölçekli öznitelik füzyonu (FPN, PAN, BiFPN, yeni füzyon modülü, ölçekler arası bağlantılar) değiştiriliyor. Boyuna yalnızca bir dikkat bloğu eklenmesi bu kodu almaz. |
| loss/IoU | Kayıp fonksiyonu / IoU | Sınırlayıcı kutu regresyon kaybı veya başka bir kayıp fonksiyonu değiştiriliyor ya da öneriliyor (ör. WIoU, SIoU, EIoU, Inner-IoU, odak kaybı). |
| data-augmentation/synthetic | Veri artırma / sentetik veri | Yeni bir veri artırma yöntemi ya da sentetik veya üretilmiş veri katkı olarak sunuluyor. Standart artırmanın kullanılması bu kodu almaz. |
| ensemble/TTA | Topluluk (ensemble) / TTA | Birden fazla modelin birleştirilmesi veya test zamanı artırma ana yöntemin parçası. |
| benchmark/comparison | Model karşılaştırması | Ana katkı, yeni bir yöntem önermeden mevcut modellerin veya yapılandırmaların karşılaştırılması ya da yeni bir karşılaştırma protokolü. |
| deployment/system/app | Sistem / uygulama | Tespitin etrafında bir uygulama veya sistem kuruluyor (mobil veya web uygulaması, araç üstü sistem, haritalama, bildirim). |
| transfer/domain-generalization | Transfer / alanlar arası genelleme | Transfer öğrenmesi, alan uyarlaması ya da ülkeler veya veri setleri arası genelleme katkı olarak sınanıyor. |
| semi/self-supervised | Yarı / öz-denetimli | Yarı denetimli, öz-denetimli, zayıf denetimli öğrenme, etkin öğrenme veya sözde etiketleme kullanılıyor. |
| multimodal/VLM/LLM | Görsel-dil modeli (VLM/LLM) | Görsel-dil modeli, büyük dil modeli veya çok kipli girdi kullanılıyor. |
| severity/quantification | Şiddet / ölçüm | Hasarın boyutu, alanı veya şiddeti ölçülüyor ya da derecelendiriliyor. |
| segmentation | Segmentasyon | Örnek veya anlamsal segmentasyon görevi yapılıyor. |
| small-object | Küçük nesne | Küçük nesnelerin veya küçük hasarların tespiti açık bir hedef (ör. küçük nesne tespit katmanı). |
| drone/UAV | İHA uygulamaları | İnsansız hava aracı görüntüleri çalışmanın odağında. |
| new-dataset | Yeni veri seti | RDD2022 dışında yeni toplanmış veya etiketlenmiş bir veri seti tanıtılıyor. |
| other | Diğer | Yukarıdaki türlerin hiçbiri metindeki katkıya uymuyor. |
