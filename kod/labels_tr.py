"""Turkish labels for the raw classifier codes shown in the supplement. Dataset and method names stay as written."""
import re

U = 'Özette belirtilmemiş'
SUBSET_FULL = {
 'unspecified subset': U, 'unspecified (subset)': U + ' (alt küme)', 'unspecified (curated subset)': U + ' (seçilmiş alt küme)',
 'unspecified (UAV images derived from RDD2022, likely China_Drone)': U + ' (RDD2022’den türetilmiş İHA görüntüleri, muhtemelen Çin (İHA))',
 'unspecified (low-light and rainy conditions)': U + ' (düşük ışık ve yağmurlu koşullar)',
 'all/full (UAV + vehicle-mounted, multiple countries)': 'Tam veri seti (İHA + araç kamerası, çok ülkeli)',
 'India, Japan, Czech (direct-transfer test); main training on UAV-PDD2023': 'Hindistan, Japonya, Çekya (doğrudan aktarım testi); ana eğitim UAV-PDD2023 ile',
 'Japan + China_MotorBike merged with EcuPDD and McMaster': 'Japonya + Çin (motosiklet), EcuPDD ve McMaster ile birleştirilmiş',
 'Japan merged with other data (PDRDD-J, SoDR)': 'Japonya, başka verilerle birleştirilmiş (PDRDD-J, SoDR)',
 'all/full (resampled: 200 images per class via K-Means)': 'Tam veri seti (yeniden örneklenmiş: K-Means ile sınıf başına 200 görüntü)',
 'Japan (+ cross-dataset China_Drone, China_MotorBike)': 'Japonya (+ veri setleri arası Çin (İHA), Çin (motosiklet))',
 'all/full (domain-aware splits across geographic and sensor domains)': 'Tam veri seti (coğrafya ve sensör alanlarına göre bölünmüş)',
 'China (China_Drone/China_MotorBike not specified)': 'Çin (İHA veya motosiklet ayrımı belirtilmemiş)',
 'merged-with-other-data (RDD2022 + Spanish road imagery)': 'Başka verilerle birleştirilmiş (RDD2022 + İspanya yol görüntüleri)',
 'merged-with-other-data (China + Spain public datasets; likely China_Drone)': 'Başka verilerle birleştirilmiş (Çin + İspanya açık veri setleri; muhtemelen Çin (İHA))',
 'unspecified (cleaned/filtered RDD2022)': U + ' (temizlenmiş veya süzülmüş RDD2022)',
 'Japan (+ cross-dataset India, Czech from RDD2020)': 'Japonya (+ RDD2020’den Hindistan ve Çekya ile veri setleri arası)',
 "China_Drone (likely, 'China-D') + UAV-PDD2023": 'Çin (İHA) (muhtemelen, “China-D”) + UAV-PDD2023',
 'merged-with-other-data (RDD2022 + in-house asphalt potholes)': 'Başka verilerle birleştirilmiş (RDD2022 + kurum içi asfalt çukurları)',
 'merged-with-other-data (RDD2022 + local data, 2,272 objects)': 'Başka verilerle birleştirilmiş (RDD2022 + yerel veri, 2.272 nesne)',
 'multi-country (six countries, multiple sensing modalities)': 'Çok ülkeli (altı ülke, birden çok algılama biçimi)',
 'unspecified (RDD2022-based)': U + ' (RDD2022 tabanlı)', 'unspecified (pothole class)': U + ' (çukur sınıfı)',
 'combos (China, India + Philippines)': 'Birden çok alt küme (Çin, Hindistan + Filipinler)',
 'unspecified (cross-scene generalization) + new MRDD dataset': U + ' (sahneler arası genelleme) + yeni MRDD veri seti',
 'unspecified ("RDD test set")': U + ' (“RDD test set”)', 'unspecified (2,000-image sample)': U + ' (2.000 görüntülük örneklem)',
 'China_Drone merged-with-other-data (UAV-PDD2023)': 'Çin (İHA), başka verilerle birleştirilmiş (UAV-PDD2023)',
 'unspecified (+ self-built dataset)': U + ' (+ yazarların kendi veri seti)',
 'unspecified (cross-dataset test; main dataset SVRDD)': U + ' (veri setleri arası test; ana veri seti SVRDD)',
 'unspecified + self-made dataset': U + ' + yazarların kendi veri seti',
 'China_Drone (+China_MotorBike generalization)': 'Çin (İHA) (+ Çin (motosiklet) ile genelleme)',
 'China (1976 images; likely China_MotorBike)': 'Çin (1.976 görüntü; muhtemelen Çin (motosiklet))',
 'UAV road damage dataset (likely China_Drone) + non-UAV road damage datasets': 'İHA yol hasarı veri seti (muhtemelen Çin (İHA)) + İHA dışı yol hasarı veri setleri',
 'unspecified (curated RDDYGES subset of RDD2022)': U + ' (RDD2022’den seçilmiş RDDYGES alt kümesi)',
 'merged-with-other-data (RDD2022 + GRDDC2020)': 'Başka verilerle birleştirilmiş (RDD2022 + GRDDC2020)',
 'unspecified (cross-dataset validation)': U + ' (veri setleri arası doğrulama)', 'all/full (six countries)': 'Tam veri seti (altı ülke)',
 'unspecified (1,428 full-scene images derived from RDD2022)': U + ' (RDD2022’den türetilmiş 1.428 tam sahne görüntüsü)',
 'unspecified (RDD2020/2022 + VisA)': U + ' (RDD2020/2022 + VisA)', 'India (+ RDD2024_SA South Africa)': 'Hindistan (+ Güney Afrika RDD2024_SA)',
 'China_Drone (likely) + Spanish data': 'Çin (İHA) (muhtemelen) + İspanya verisi',
 'unspecified (plus adverse-weather subsets)': U + ' (+ olumsuz hava alt kümeleri)', 'unspecified (few-shot setting)': U + ' (az örnekli öğrenme)',
 'all/full (multiple countries)': 'Tam veri seti (çok ülkeli)',
 'merged-with-other-data (RDD2022 + Roboflow RoadDamageDetection, unified classes)': 'Başka verilerle birleştirilmiş (RDD2022 + Roboflow RoadDamageDetection, sınıflar birleştirilmiş)',
 'merged-with-other-data (re-annotated public datasets + 13,000 own images)': 'Başka verilerle birleştirilmiş (yeniden etiketlenmiş açık veri setleri + 13.000 özgün görüntü)',
 'combos (curated 4-region subset, 5 classes)': 'Birden çok alt küme (seçilmiş 4 bölge, 5 sınıf)', 'unspecified (26,620 images)': U + ' (26.620 görüntü)',
 'merged-with-other-data (RDD2022 + CrackForest)': 'Başka verilerle birleştirilmiş (RDD2022 + CrackForest)',
 'merged-with-other-data (RDD2022 + custom samples)': 'Başka verilerle birleştirilmiş (RDD2022 + özel örnekler)', 'all/full (six regions)': 'Tam veri seti (altı bölge)',
 'unspecified (external validation on RDD2022 + CPRI)': U + ' (RDD2022 + CPRI ile dış doğrulama)',
 'unspecified (UAV + dashcam portions; pure and mixed models)': U + ' (İHA + araç kamerası bölümleri; saf ve karma modeller)',
 'unspecified (global-scale, likely multi-country RDD2022)': U + ' (küresel ölçek, muhtemelen çok ülkeli RDD2022)',
 'China_MotorBike, China_Drone + RDD-CC (RDD2022 extended with Chinese car images; merged-with-other-data)': 'Çin (motosiklet), Çin (İHA) + RDD-CC (Çin araç görüntüleriyle genişletilmiş RDD2022; başka verilerle birleştirilmiş)',
 'unspecified (+ self-built dataset, evaluated separately)': U + ' (+ yazarların kendi veri seti, ayrı değerlendirilmiş)',
 'China_MotorBike (likely; re-annotated pixel-level as China_MCrack)': 'Çin (motosiklet) (muhtemelen; piksel düzeyinde yeniden etiketlenmiş: China_MCrack)',
 'China_Drone + merged-with-other-data (Spanish road dataset)': 'Çin (İHA), başka verilerle birleştirilmiş (İspanya yol veri seti)',
 'all/full (ORDDC2024, 47,420 images from six countries)': 'Tam veri seti (ORDDC2024, altı ülkeden 47.420 görüntü)',
 'all/full (ORDDC\'2024)': 'Tam veri seti (ORDDC’2024)', "unspecified (ORDDC'2024 challenge data)": U + ' (ORDDC’2024 yarışma verisi)',
 'all/full (6 country sources)': 'Tam veri seti (6 ülke kaynağı)', 'all/full (ORDDC2024 / CRDDC2022 data)': 'Tam veri seti (ORDDC2024 / CRDDC2022 verisi)',
 'merged-with-other-data (RDD2022 + Baidu; relabeled 3 classes)': 'Başka verilerle birleştirilmiş (RDD2022 + Baidu; 3 sınıfa yeniden etiketlenmiş)',
 "all/full (ORDDC'2024 challenge data, RDD2022-based)": 'Tam veri seti (ORDDC’2024 yarışma verisi, RDD2022 tabanlı)',
 "all/full (six countries, ORDDC'2024)": 'Tam veri seti (altı ülke, ORDDC’2024)', 'China_Drone (China-D)': 'Çin (İHA) (China-D)',
 'unspecified (RDD-2022 and RDD-2020)': U + ' (RDD-2022 ve RDD-2020)',
 'combos: Czech, India, United_States, Japan each merged with Türkiye (Hatay) data': 'Birden çok alt küme: Çekya, Hindistan, ABD ve Japonya, her biri Türkiye (Hatay) verisiyle birleştirilmiş',
 'merged-with-other-data (China_Drone + Spanish road dataset)': 'Başka verilerle birleştirilmiş (Çin (İHA) + İspanya yol veri seti)',
 'unspecified (preprocessed RDD2022)': U + ' (ön işlenmiş RDD2022)',
 'unspecified RDD2022 + custom Malaysia dataset (evaluated separately)': U + ' + özel Malezya veri seti (ayrı değerlendirilmiş)',
 'merged-with-other-data (RDD2022 + new China images)': 'Başka verilerle birleştirilmiş (RDD2022 + yeni Çin görüntüleri)',
 'unspecified + collected RDDA dataset': U + ' + toplanan RDDA veri seti',
 'all/full (CRDDC2022 five test sets)': 'Tam veri seti (CRDDC2022 beş test kümesi)',
 'all/full (CRDDC2022: all countries, India, Japan, Norway, United_States leaderboards)': 'Tam veri seti (CRDDC2022: tüm ülkeler, Hindistan, Japonya, Norveç, ABD liderlik tabloları)',
 'all/full (CRDDC2022 competition)': 'Tam veri seti (CRDDC2022 yarışması)', 'all/full (multi-country CRDDC2022)': 'Tam veri seti (çok ülkeli CRDDC2022)', 'all/full (CRDDC2022 leaderboards)': 'Tam veri seti (CRDDC2022 liderlik tabloları)',
 'China_MotorBike (+ UAPD_5cls)': 'Çin (motosiklet) (+ UAPD_5cls)', 'all/full (GRDDC2022) + China': 'Tam veri seti (GRDDC2022) + Çin', 'all/full + China': 'Tam veri seti + Çin',
 'Japan, China_MotorBike': 'Japonya, Çin (motosiklet)', 'Japan, China, Norway': 'Japonya, Çin, Norveç',
 'unspecified (+UAV-PDD2023)': U + ' (+ UAV-PDD2023)', 'unspecified (+ UAV-PDD2023)': U + ' (+ UAV-PDD2023)', 'unspecified (+ SVRDD)': U + ' (+ SVRDD)', 'unspecified (+ SDNET2018, CCCD)': U + ' (+ SDNET2018, CCCD)', 'unspecified (+MaskRDD-140)': U + ' (+ MaskRDD-140)',
 'combos (RDD2022_Mix)': 'Birden çok alt küme (RDD2022_Mix)', 'combos': 'Birden çok alt küme',
 'Japan (+ RDD2022 geneli, alt küme belirtilmemiş)': 'Japonya (+ RDD2022 geneli, alt küme belirtilmemiş)',
 'n/a': 'Özette belirtilmemiş',
}
PAIRS = [('merged-with-other-data', 'Başka verilerle birleştirilmiş'), ('China_MotorBike', 'Çin (motosiklet)'), ('China_Motorbike', 'Çin (motosiklet)'), ('China motorbike', 'Çin (motosiklet)'), ('China_Drone', 'Çin (İHA)'), ('China drone', 'Çin (İHA)'),
         ('United_States', 'ABD'), ('United States', 'ABD'), ('all/full', 'Tam veri seti'), ('unspecified', U)]
WORD = [('China', 'Çin'), ('Japan', 'Japonya'), ('India', 'Hindistan'), ('Czech', 'Çekya'), ('Norway', 'Norveç')]
RAW = re.compile(r'\b(unspecified|merged|likely|combos|all/full|images|subset|dataset)\b|China_(?:Drone|MotorBike|Motorbike)|United_States')

def tr_subset(t):
    if not t: return t
    if t in SUBSET_FULL: return SUBSET_FULL[t]
    for a, b in PAIRS: t = t.replace(a, b)
    for a, b in WORD: t = re.sub(rf'(?<![\w_-]){a}(?![\w_-])', b, t)
    return t

METHOD_FULL = {'other': 'Diğer', 'ensemble': 'Topluluk (ensemble)', 'CNN classifier': 'CNN sınıflandırıcı', 'YOLO (unspecified)': 'YOLO (sürüm belirtilmemiş)',
 'other (deep CNN semantic segmentation)': 'Diğer (derin CNN anlamsal bölütleme)', 'other (mixture-of-experts detector)': 'Diğer (uzmanlar karışımı dedektör)', 'other (HOG features + SVM)': 'Diğer (HOG öznitelikleri + SVM)',
 "other (YOLO26 / 'YOLOv2026n')": 'Diğer (YOLO26 / “YOLOv2026n”)', 'other (MSRD-DET)': 'Diğer (MSRD-DET)', 'other (CNN + transformer)': 'Diğer (CNN + transformer)', 'other (YOLO26)': 'Diğer (YOLO26)',
 'other (custom lightweight one-stage detector with knowledge distillation)': 'Diğer (bilgi damıtmalı, özel hafif tek aşamalı dedektör)', 'other (baseline not named)': 'Diğer (temel model adı verilmemiş)',
 'CNN classifier + LLM (MobileNetV3, EfficientNet-B4, MiDaS DPT-Large, T5-XL)': 'CNN sınıflandırıcı + büyük dil modeli (MobileNetV3, EfficientNet-B4, MiDaS DPT-Large, T5-XL)', 'other (ALC-Net, YOLO-style)': 'Diğer (ALC-Net, YOLO benzeri)',
 'other (DBBPN detector + large segmentation model, zero-shot)': 'Diğer (DBBPN dedektör + büyük bölütleme modeli, sıfır örnekli)', 'CNN classifier (ResNet50) + fuzzy logic': 'CNN sınıflandırıcı (ResNet50) + bulanık mantık', 'other (YOLO-style CNN)': 'Diğer (YOLO benzeri CNN)',
 'other (FAD-Net)': 'Diğer (FAD-Net)', 'other (latent diffusion + VLM augmentation)': 'Diğer (gizil difüzyon + görsel-dil modeliyle veri artırma)', 'other (FPDDN, deformable transformer)': 'Diğer (FPDDN, deforme olabilen transformer)',
 'other (GAN + texture synthesis augmentation)': 'Diğer (GAN + doku sentezi ile veri artırma)', 'other (challenge solutions)': 'Diğer (yarışma çözümleri)', 'other (RTMDet)': 'Diğer (RTMDet)', 'YOLO (dual-stream, version unspecified)': 'YOLO (çift akışlı, sürüm belirtilmemiş)', 'YOLO (lightweight, unspecified)': 'YOLO (hafif, sürüm belirtilmemiş)', 'YOLO (base version unspecified)': 'YOLO (temel sürüm belirtilmemiş)'}

def tr_method(t):
    return METHOD_FULL.get(t, t)

def tr_metric(t):
    if not t: return t
    for a, b in (('(India)', '(Hindistan)'), ('(Japan)', '(Japonya)'), ('(Czech)', '(Çekya)'), ('(Norway)', '(Norveç)'), ('(China)', '(Çin)'), ('(United States)', '(ABD)'), ('(US)', '(ABD)')): t = t.replace(a, b)
    return t
