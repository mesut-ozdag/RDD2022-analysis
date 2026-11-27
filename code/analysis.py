"""Builds the final study list and most analysis numbers used in the manuscript; search-flow counts (Table 1, S1) are transcribed by hand from the records.
Inputs: unshared intermediate files in ../data, ../out and ../batches (listed in README.md). Output: ../out/results.json, ../out/prci_final_v2.json, ../out/status_final.json, ../data/final_studies.json."""
import collections, glob, json, os, random, re, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', 'data'); O = os.path.join(HERE, '..', 'out')
papers = json.load(open(f'{D}/papers.json'))
status = json.load(open(f'{O}/use_status_interim.json'))
wf = json.load(open(f'{O}/wf_main.json')); new = {n['id']: n for n in json.load(open(f'{O}/new_candidates.json'))}
prti = json.load(open(f'{O}/prci_final.json')); sel = json.load(open(f'{D}/analysis_21.json'))   # analysis set: all 21 studies meeting the eligibility criteria
corpus = {r['pid']: r for r in json.load(open(f'{D}/corpus.json'))}
wf1 = json.load(open(f'{D}/wf1_result.json')); cls = {c['pid']: c for c in wf1['classified']}
nb = {}
for f in glob.glob(os.path.join(HERE, '..', 'batches', 'new_*.json')):
    for r in json.load(open(f)): nb[r['id']] = r
CONTRIB_TR = {'architecture-improvement': 'Mimari iyileştirme', 'attention-module': 'Dikkat modülü', 'lightweight/edge': 'Hafif model / uç cihaz',
              'neck/feature-fusion': 'Boyun / öznitelik füzyonu', 'benchmark/comparison': 'Model karşılaştırması', 'transfer/domain-generalization': 'Transfer / alanlar arası genelleme',
              'small-object': 'Küçük nesne', 'loss/IoU': 'Kayıp fonksiyonu / IoU', 'other': 'Diğer', 'deployment/system/app': 'Sistem / uygulama', 'drone/UAV': 'İHA (drone)',
              'data-augmentation/synthetic': 'Veri artırma / sentetik veri', 'ensemble/TTA': 'Topluluk (ensemble) / TTA', 'new-dataset': 'Yeni veri seti', 'segmentation': 'Segmentasyon',
              'severity/quantification': 'Şiddet / ölçüm', 'semi/self-supervised': 'Yarı / öz-denetimli', 'multimodal/VLM/LLM': 'Görsel-dil modeli (VLM/LLM)', 'survey': 'Derleme'}
# studies added by the logged searches, coded from their abstracts with the same scheme
ADD = {
 'N001': ('YOLO (diğer)', ['architecture-improvement', 'segmentation', 'transfer/domain-generalization']),
 'N002': ('YOLOv8', ['architecture-improvement', 'attention-module', 'lightweight/edge', 'loss/IoU']),
 'N006': ('Diğer', ['architecture-improvement', 'attention-module']),
 'N007': ('YOLOv8', ['architecture-improvement', 'attention-module', 'neck/feature-fusion']),
 'N010': ('YOLOv8', ['architecture-improvement', 'attention-module', 'lightweight/edge', 'loss/IoU']),
 'N011': ('YOLOv8', ['architecture-improvement', 'lightweight/edge']),
 'N012': ('YOLOv10', ['architecture-improvement', 'multimodal/VLM/LLM', 'drone/UAV']),
 'N014': ('RT-DETR', ['architecture-improvement', 'small-object', 'lightweight/edge', 'neck/feature-fusion']),
 'N015': ('Diğer', ['architecture-improvement', 'attention-module', 'small-object', 'neck/feature-fusion']),
 'N016': ('YOLOv8', ['deployment/system/app', 'severity/quantification']),
 'N017': ('YOLOv8', ['architecture-improvement', 'attention-module']),
 'N018': ('YOLOv8', ['architecture-improvement', 'lightweight/edge', 'loss/IoU']),
 'N021': ('Diğer', ['other']),
 'N022': ('YOLO11', ['architecture-improvement', 'neck/feature-fusion']),
 'N023': ('YOLOv8', ['architecture-improvement', 'lightweight/edge', 'neck/feature-fusion', 'loss/IoU']),
 'X001': ('YOLOv8', ['architecture-improvement', 'lightweight/edge']),
 'X002': ('YOLO (diğer)', ['deployment/system/app']),
}
VERDICT = {x['id']: x for x in wf['verify']}
RS = {x['id']: x for x in json.load(open(f'{O}/rescreen.json'))}
for x in RS.values():
    status.setdefault(x['id'], dict(id=x['id']))
    status[x['id']]['status'] = {'teyit': 'teyit', 'dogrulanamadi': 'dogrulanamadi', 'yinelenen_surum': 'yinelenen'}[x['verdict']]
# record-level re-verification (2 Nov 2026): two coding passes blind to earlier codes, a third pass on disagreements
RC = {x['id']: x for x in json.load(open(f'{O}/recheck.json'))} if os.path.exists(f'{O}/recheck.json') else {}
RC_STATUS = {'teyit': 'teyit', 'dogrulanamadi': 'dogrulanamadi', 'kullanmiyor': 'kullanmiyor', 'yinelenen_surum': 'yinelenen', 'yayin_turu_uygun_degil': 'yayin_turu', 'derleme': 'derleme', 'veri_seti_tanitimi': 'veri_seti', 'konu_disi': 'konu_disi'}
for x in RC.values():
    status.setdefault(x['id'], dict(id=x['id']))
    status[x['id']]['status'] = RC_STATUS[x['verdict']]
RS_FAMILY = {'P024': 'YOLOv9', 'P028': 'YOLOv8', 'P054': 'RT-DETR', 'P090': 'Diğer', 'P120': 'YOLOv8', 'P124': 'YOLOv8', 'P164': 'YOLOv5', 'P174': 'YOLOv8', 'P194': 'YOLOv8', 'P200': 'Faster / Cascade R-CNN',
             'P233': 'YOLOv8', 'P244': 'YOLOv9', 'P278': 'YOLOv10', 'P280': 'YOLOv8', 'P394': 'YOLOv8', 'P399': 'YOLO11', 'P408': 'YOLOv5', 'P414': 'YOLO (diğer)', 'P420': 'Diğer', 'P432': 'YOLO11', 'P434': 'CNN sınıflandırıcı',
             'P464': 'YOLOv8', 'P474': 'YOLOv12', 'P483': 'DETR ailesi', 'P494': 'YOLOv8', 'W043': 'YOLOv10', 'W047': 'YOLO11', 'W058': 'RT-DETR', 'P106': 'YOLO11', 'P334': 'YOLO11'}
RS_METHOD = {'P106': 'ALC-Net (YOLO11 tabanlı)', 'P334': 'StripRFNet (YOLO11 tabanlı)'}
papers = [p for p in papers if status.get(p['id'], {}).get('status') in ('teyit', 'dogrulanamadi') or p['id'] not in RC and status.get(p['id'], {}).get('status') != 'yinelenen']
have = {p['id'] for p in papers}
for pid, x in RS.items():
    if x['verdict'] in ('teyit', 'dogrulanamadi') and pid not in have:
        r_ = corpus[pid]; c_ = cls[pid]
        papers.append(dict(id=pid, source='OpenAlex', year=r_['year'], title=r_['title'], authors=x.get('authors') or ', '.join(r_['authors']), authors_full=x.get('authors') or ', '.join(r_['authors']), venue=r_['venue'] or '', cites=r_['cites'],
                           url=r_['doi'] or r_['landing'] or '', family=RS_FAMILY.get(pid, 'Diğer'), method=x.get('method_family') or c_['method_family'], contrib=[CONTRIB_TR[k] for k in c_['contribution_types']],
                           subset=c_['subset'], summary=c_['summary_tr']))
have = {p['id'] for p in papers}
for pid, x in RC.items():
    if x['verdict'] in ('teyit', 'dogrulanamadi') and pid not in have and pid in corpus:
        r_ = corpus[pid]; su_ = x.get('subset_used') or ''
        papers.append(dict(id=pid, source='OpenAlex', year=r_['year'], title=r_['title'], authors=x.get('authors') or ', '.join(r_['authors']), authors_full=x.get('authors') or ', '.join(r_['authors']), venue=r_['venue'] or x.get('venue') or '', cites=r_['cites'],
                           url=r_['doi'] or r_['landing'] or '', family=x.get('family') or 'Diğer', method=x.get('family') or 'Diğer', contrib=[CONTRIB_TR[k] for k in x.get('contribution_types', [])],
                           subset='unspecified' if 'belirtilmemiş' in su_.lower() or not su_ else su_, summary=x.get('summary_tr') or ''))
for p in papers:
    if p['id'] in RS_FAMILY: p['family'] = RS_FAMILY[p['id']]
    if p['id'] in RS_METHOD: p['method'] = RS_METHOD[p['id']]
# subsets read from abstracts during the record-level checks; these replace the first-pass code
RS_SUBSET = {'P054': 'China_MotorBike', 'P090': 'China_MotorBike', 'P464': 'China', 'P314': 'Japan (+ RDD2022 geneli, alt küme belirtilmemiş)', 'P432': 'China_Drone'}
for p in papers:
    if p['id'] in RS_SUBSET: p['subset'] = RS_SUBSET[p['id']]
AUTO = {a['id']: a for a in json.load(open(f'{O}/verify_auto_from_deep.json'))}
PAT = re.compile(r'RDD[\s-]?2022|CRDDC', re.I)
web_x = {c['title']: c for w in wf['web'] for c in w['new_candidates']}
out = []
for p in papers:
    i = p['id']; s = status[i]['status']
    if i in RC:
        v = RC[i]; reason, level, url_ev = v['evidence_tr'], v['evidence_level'], v['source_url']
    elif i == 'P048':
        reason, level = 'Aynı çalışmanın doktora tezinde (YÖK 843997) CRDDC2022 kullanımı tam metinden doğrulandı; dergi makalesinin tam metnine erişilemedi.', 'tam_metin_tez'
        url_ev = 'https://hdl.handle.net/20.500.14958/5341'
    elif i in RS:
        v = RS[i]; reason, level, url_ev = v['evidence_tr'], v['evidence_level'], v['source_url']
    elif i in VERDICT:
        v = VERDICT[i]; reason, level, url_ev = v['evidence_tr'], v['evidence_level'], v['source_url']
    elif i in AUTO:
        a = AUTO[i]; reason = 'Ayrıntılı incelemede (12 Ekim 2026) kullanım doğrulandı.'
        level = 'tam_metin' if a.get('full_text') else 'ozet_veya_yayinci'; url_ev = a.get('url')
    elif p['source'] == 'OpenAlex':
        reason = 'Özette veri setinin adı ve deneylerde kullanımı açıkça belirtiliyor.' if PAT.search(corpus[i].get('abstract') or '') else 'Sınıflandırmada doğrudan kullanım olarak kodlandı; özet erişilemedi, künye ek veri ile eşleştirildi.'
        level = 'ozet_veya_yayinci'; url_ev = p['url']
    else:
        reason = 'Hedefli taramada özet, atıf bağlamı veya yayın sayfasından RDD2022 kullanımı doğrulandı. ' + (p.get('summary') or ''); level = 'ozet_veya_yayinci'; url_ev = p['url']
    out.append(dict(id=i, arm='OpenAlex' if p['source'] == 'OpenAlex' else 'Hedefli tarama (12 Ekim 2026)', status=s, year=p['year'], title=p['title'], authors=p.get('authors_full') or p['authors'],
                    venue=p['venue'], cites=p['cites'], url=p['url'], family=p['family'], method=p['method'], contrib=p['contrib'], subset=p['subset'], summary=p['summary'],
                    evidence_level=level, inclusion_reason=reason, evidence_url=url_ev, in_analysis=False))
for i, (fam, keys) in ADD.items():
    if i in RC and RC[i]['verdict'] != 'teyit': continue
    if i.startswith('N'):
        n = new[i]; r = nb[i]
        rec = dict(title=r['title'].rstrip('.'), year=r['year'], url='https://doi.org/' + r['doi'], authors=n.get('authors') or '', venue=n.get('venue') or '', subset=n.get('subset_used') or '',
                   reason=n['evidence_tr'], level=n['evidence_level'], ev=n['source_url'], arm='Belgelenmiş tarama (2 Kasım 2026)')
    else:
        key = 'Lightweight Road Crack' if i == 'X001' else 'Investigating The'
        c = next(v for k, v in web_x.items() if k.startswith(key))
        rec = dict(title=c['title'], year=c['year'], url=c['url'], authors='Kaya, Çodur' if i == 'X002' else '', venue=c.get('venue') or '', subset=c.get('subset_used') or '', reason=c['evidence_tr'],
                   level='tam_metin', ev=c['url'], arm='Belgelenmiş tarama (2 Kasım 2026)')
    if i in RC: rec.update(reason=RC[i]['evidence_tr'], level=RC[i]['evidence_level'], ev=RC[i]['source_url'])
    out.append(dict(id=i, arm=rec['arm'], status='teyit', year=rec['year'], title=rec['title'], authors=rec['authors'], venue=rec['venue'], cites=None, url=rec['url'], family=fam, method=fam,
                    contrib=[CONTRIB_TR[k] for k in keys], subset=rec['subset'], summary='', evidence_level=rec['level'], inclusion_reason=rec['reason'], evidence_url=rec['ev'], in_analysis=False))
if 'N000' in new:
    n = new['N000']; r = nb['N000']
    out.append(dict(id='N000', arm='Belgelenmiş tarama (2 Kasım 2026)', status='dogrulanamadi', year=r['year'], title=r['title'], authors=n.get('authors') or '', venue=n.get('venue') or '', cites=None,
                    url='https://doi.org/' + r['doi'], family='', method='', contrib=[], subset='', summary='', evidence_level='yok', inclusion_reason=n['evidence_tr'], evidence_url=n['source_url'], in_analysis=False))
if RC.get('A001', {}).get('verdict') in ('teyit', 'dogrulanamadi'):
    x = RC['A001']
    out.append(dict(id='A001', arm='Hedefli tarama (12 Ekim 2026)', status=status['A001']['status'], year=2025, title='Accelerating Road Maintenance and Repair Processes: YOLO and Large Language Model for Detection and Classification of Defects in Flexible Pavements', authors=x.get('authors') or '', venue=x.get('venue') or 'Springer kitap bölümü', cites=None,
                    url='https://doi.org/10.1007/978-3-031-86039-3_16', family=x.get('family') or '', method=x.get('family') or '', contrib=[CONTRIB_TR[k] for k in x.get('contribution_types', [])], subset=x.get('subset_used') or '', summary=x.get('summary_tr') or '', evidence_level=x['evidence_level'], inclusion_reason=x['evidence_tr'], evidence_url=x['source_url'], in_analysis=False))
ids_set = {s['pid'] for s in sel}
deep = {d['pid']: d for d in json.load(open(f'{D}/deep_result.json'))['deep']}
for r in out:
    if r['id'] in ids_set: r['in_analysis'] = True
    # studies read in full during the detailed examination carry full-text evidence
    if r['id'] in deep and deep[r['id']].get('full_text_accessed') and r['status'] == 'teyit' and r['evidence_level'] == 'ozet_veya_yayinci' and r['id'] not in VERDICT and r['id'] not in RC:
        r['evidence_level'] = 'tam_metin'
        r['inclusion_reason'] = 'Ayrıntılı incelemede (12 Ekim 2026) tam metinden doğrulandı.'
        r['evidence_url'] = deep[r['id']].get('verified_url') or r['evidence_url']
# contribution types: coded for all confirmed studies with the written codebook (code/contribution_type_codebook.md);
# two coding passes per study, disagreements settled by a third pass (out/contribution_coding_v4_raw.json)
KV4 = json.load(open(f'{O}/contribution_codes_v4.json'))
for r in out:
    if r['status'] == 'teyit': r['contrib'] = [CONTRIB_TR[k] for k in KV4[r['id']]]
json.dump(out, open(f'{D}/final_studies.json', 'w'), ensure_ascii=False, indent=0)
conf = [r for r in out if r['status'] == 'teyit']; unv = [r for r in out if r['status'] == 'dogrulanamadi']
R = dict(n_conf=len(conf), n_unv=len(unv), conf_by_arm=collections.Counter(r['arm'] for r in conf), unv_by_arm=collections.Counter(r['arm'] for r in unv))
R['evidence_levels_conf'] = collections.Counter(r['evidence_level'] for r in conf)

# ------- publication trends
yr = range(2022, 2027); core = collections.Counter(); web = collections.Counter(); unv_y = collections.Counter(); rel = collections.Counter(); sur = collections.Counter(); dat = collections.Counter()
DUP = {'P403', 'P277', 'P166', 'P130'}
flow = collections.Counter()
for pid, c in cls.items():
    y = corpus[pid]['year']; st_ = status.get(pid, {}).get('status')
    if pid in DUP or st_ == 'yinelenen':
        flow['merged'] += 1; continue
    if st_ == 'yayin_turu': flow['pubtype'] += 1; continue
    if st_ == 'derleme': sur[y] += 1; flow['survey'] += 1; continue
    if st_ == 'veri_seti': dat[y] += 1; flow['dataset'] += 1; continue
    if st_ == 'konu_disi': flow['irrelevant'] += 1; continue
    if st_ == 'kullanmiyor': rel[y] += 1; flow['rel_no'] += 1; continue
    if c['relevance'] == 'core' or st_ in ('teyit', 'dogrulanamadi'):
        if st_ == 'teyit' or (st_ is None and c['uses_rdd2022'] in ('yes', 'likely')):
            core[y] += 1; flow['oa_conf'] += 1
        elif st_ == 'kullanmiyor':
            rel[y] += 1; flow['rel_no'] += 1
        else:
            unv_y[y] += 1; flow['unv_oa'] += 1
    elif c['relevance'] == 'survey': sur[y] += 1; flow['survey'] += 1
    elif c['relevance'] == 'dataset': dat[y] += 1; flow['dataset'] += 1
    elif c['relevance'] == 'irrelevant': flow['irrelevant'] += 1
    else:
        rel[y] += 1; flow['rel_no' if c['uses_rdd2022'] == 'no' else 'rel_unclear'] += 1
# final decision of every record, used by the supplement
json.dump({k: v.get('status') for k, v in status.items()}, open(f'{O}/status_final.json', 'w'), ensure_ascii=False)
DUP_MAP = {'P403': 'P003', 'P277': 'P167', 'P166': 'P033', 'P130': 'P007', 'P119': 'P002', 'P223': 'P046', 'P400': 'P003', 'P412': 'P003'}
DUP_PAIR = {'P277', 'P166', 'P130', 'P119', 'P223', 'P270'}; DUP_REPO = set()
for x in RC.values():
    if x['verdict'] == 'yinelenen_surum' and x['id'] in cls:
        DUP_MAP[x['id']] = x['duplicate_of']
        if x.get('pub_type') in ('veri_kaydi', 'yazilim_deposu'): DUP_REPO.add(x['id'])
R['dup_map'] = DUP_MAP; R['dup_pairs'] = len(DUP_PAIR); R['dup_repo'] = len(DUP_REPO); R['dup_repeat'] = len(DUP_MAP) - len(DUP_PAIR) - len(DUP_REPO)
W_RC = {i: x for i, x in RC.items() if i.startswith('W') or i == 'A001'}
base_w = {i for i, v in json.load(open(f'{O}/use_status_interim.json')).items() if i.startswith('W')}
conf_w = sum(1 for r in out if r['arm'].startswith('Hedefli') and r['status'] == 'teyit'); unv_w = sum(1 for r in out if r['arm'].startswith('Hedefli') and r['status'] == 'dogrulanamadi')
n_w = lambda *vs: sum(1 for x in W_RC.values() if x['verdict'] in vs)
R['targeted'] = dict(assessed=64 + (1 if 'A001' in RC else 0), conf=conf_w, unv=unv_w, not_using=n_w('kullanmiyor', 'konu_disi', 'veri_seti_tanitimi'), merged=n_w('yinelenen_surum'), pubtype=1 + n_w('yayin_turu_uygun_degil', 'derleme'))
assert sum(R['targeted'][k] for k in ('conf', 'unv', 'not_using', 'merged', 'pubtype')) == R['targeted']['assessed'], R['targeted']
DEC_W = {'kullanmiyor': 'Dışlandı: veri setini kullanmıyor', 'konu_disi': 'Dışlandı: konu dışı', 'yinelenen_surum': 'Birleştirildi', 'yayin_turu_uygun_degil': 'Dışlandı: yayın türü uygun değil', 'derleme': 'Dışlandı: derleme', 'veri_seti_tanitimi': 'Dışlandı: veri seti tanıtımı'}
R['targeted_other'] = [dict(id='W020', year=2025, title='Insights from the Road Damage Detection Challenge Series (2018–2024)', venue='Nature Machine Intelligence', url='https://doi.org/10.1038/s42256-025-01132-5', decision='Dışlandı: perspektif yazısı', level='', note='Yarışma serisini değerlendiren perspektif yazısı; özgün deney bildirmiyor.', source='')]
pap0 = {p_['id']: p_ for p_ in json.load(open(f'{D}/papers.json'))}
for i, x in sorted(W_RC.items()):
    if x['verdict'] in DEC_W:
        p_ = pap0.get(i, {}); bi_ = {b_['id']: b_ for f_ in glob.glob(os.path.join(HERE, '..', 'batches', 'recheck_*.json')) for b_ in json.load(open(f_))}.get(i, {})
        dec_ = DEC_W.get(x['verdict'], 'Teyit edilemedi'); dec_ = dec_ + (f": {x['duplicate_of']} ile aynı çalışma" if x['verdict'] == 'yinelenen_surum' else '')
        R['targeted_other'].append(dict(id=i, year=p_.get('year') or bi_.get('year'), title=p_.get('title') or bi_.get('title'), venue=p_.get('venue') or bi_.get('venue') or '', url=p_.get('url') or bi_.get('landing') or '', decision=dec_, level=x['evidence_level'], note=x['evidence_tr'], source=x['source_url']))
n_added = sum(1 for k_ in ADD if k_.startswith('N') and not (k_ in RC and RC[k_]['verdict'] != 'teyit')); x_added = sum(1 for k_ in ADD if k_.startswith('X') and not (k_ in RC and RC[k_]['verdict'] != 'teyit'))
R['other'] = dict(reg_added=n_added, web_added=x_added, reg_not_using=24 - n_added - 2 - 1, added=conf_w + n_added + x_added, assessed=R['targeted']['assessed'] + 24 + 15)
R['other']['not_added'] = R['other']['assessed'] - R['other']['added']
R['flow'] = dict(flow); R['flow'].setdefault('pubtype', 0); R['flow']['direct'] = flow['oa_conf'] + flow['merged']; R['flow']['excluded'] = 554 - R['flow']['direct']
for r in out:
    if r['arm'] != 'OpenAlex':
        (web if r['status'] == 'teyit' else unv_y)[r['year']] += 1
R['years'] = [dict(y=y, core=core[y], web=web[y], unverified=unv_y[y], related=rel[y], survey=sur[y], dataset=dat[y]) for y in yr]
R['year_total'] = sum(core.values()) + sum(web.values()) + sum(unv_y.values()) + sum(rel.values()) + sum(sur.values()) + sum(dat.values())
# ------- methods
fam = collections.Counter(r['family'] for r in conf)
R['family'] = fam.most_common()
YOLO = {'YOLOv8', 'YOLO11', 'YOLOv5', 'YOLOv7', 'YOLO (diğer)', 'YOLOv10', 'YOLOv12', 'YOLOv9', 'YOLO26', 'YOLOv13', 'YOLOv6', 'YOLOv4', 'YOLOv3'}
R['yolo_n'] = sum(fam[f] for f in YOLO); R['yolo_pct'] = R['yolo_n'] / len(conf) * 100
R['detr_n'] = fam['RT-DETR'] + fam['DETR ailesi']
fy = collections.defaultdict(collections.Counter)
for r in conf: fy[r['family']][r['year']] += 1
R['family_year'] = {k: dict(v) for k, v in fy.items()}
cc = collections.Counter(c for r in conf for c in r['contrib'])
R['contrib'] = [(k, v, v / len(conf) * 100) for k, v in cc.most_common() if k != 'Diğer']; R['contrib_other'] = cc['Diğer']
oa_conf = [r for r in conf if r['arm'] == 'OpenAlex']
targets = {t['pid'] for t in json.load(open(f'{D}/deep_targets.json'))}
st_by = {r['id']: r['status'] for r in out}
R['deep_status'] = dict(collections.Counter(st_by.get(p, 'siniflandirma_disi') for p in targets)); R['deep_outside'] = [p for p in targets if p not in st_by]
R['oa_conf'] = len(oa_conf); R['oa_unspec'] = sum(1 for r in oa_conf if (r['subset'] or '').lower().startswith('unspecified')); R['oa_unspec_pct'] = R['oa_unspec'] / len(oa_conf) * 100
web_v = [r for r in conf if r['arm'] != 'OpenAlex']
R['web_conf'] = len(web_v)
core_yes = [p_ for p_, c_ in cls.items() if c_['relevance'] == 'core' and c_['uses_rdd2022'] == 'yes']
R['oa_core_yes'] = len(core_yes); R['oa_named_in_abstract'] = sum(1 for p_ in core_yes if PAT.search(corpus[p_].get('abstract') or '')); R['oa_no_abstract_core_yes'] = sum(1 for p_ in core_yes if not (corpus[p_].get('abstract') or '').strip())
alt_ = json.load(open(f'{D}/abstract_alt.json'))
unclear_ = [p_ for p_, c_ in cls.items() if c_['relevance'] == 'related' and c_['uses_rdd2022'] != 'no' and status.get(p_, {}).get('status') is None and p_ not in DUP]
R['unclear_n'] = len(unclear_); R['unclear_no_oa_abs'] = sum(1 for p_ in unclear_ if not (corpus[p_].get('abstract') or '').strip()); R['unclear_no_abs'] = sum(1 for p_ in unclear_ if not (corpus[p_].get('abstract') or '').strip() and p_ not in alt_)
RT_PART = ['P051', 'P060', 'P071', 'P083', 'P129', 'P148', 'W000', 'W001', 'P170', 'P171', 'P173', 'P218', 'P219', 'P220', 'P152']; RT_SUM = ['P007', 'P072']; RT_OTH = ['P016', 'P334', 'P225']
cid_ = {r['id'] for r in conf}
R['resmi_test'] = dict(katilimci=sum(i_ in cid_ for i_ in RT_PART), ozet=sum(i_ in cid_ for i_ in RT_SUM), diger=sum(i_ in cid_ for i_ in RT_OTH)); R['resmi_test']['yarisma'] = R['resmi_test']['katilimci'] + R['resmi_test']['ozet']; R['resmi_test']['n'] = R['resmi_test']['yarisma'] + R['resmi_test']['diger']; R['resmi_test']['pct'] = R['resmi_test']['n'] / len(conf) * 100; R['resmi_test_ids'] = RT_PART + RT_SUM + RT_OTH
TPL = {'Dikkat modülü', 'Boyun / öznitelik füzyonu', 'Hafif model / uç cihaz', 'Kayıp fonksiyonu / IoU'}
R['contrib_union'] = sum(1 for r in conf if TPL & set(r['contrib'])); R['contrib_union_pct'] = R['contrib_union'] / len(conf) * 100
KH = json.load(open(f'{O}/contribution_coding_v4_raw.json')); ids_ = [r['id'] for r in conf]
R['contrib_rel'] = dict(n=len(ids_), exact=sum(sorted(KH['A'][i]['codes']) == sorted(KH['B'][i]['codes']) for i in ids_), adjudicated=sum(KH['src'][i] == 'hakem' for i in ids_),
                        no_abstract=sum(1 for x in json.load(open(f'{D}/contribution_coding_input_297.json')) if x['text_src'] != 'özet'))
kap_ = {}
for k_ in CONTRIB_TR:
    if k_ == 'survey': continue
    a_ = [int(k_ in KH['A'][i]['codes']) for i in ids_]; b_ = [int(k_ in KH['B'][i]['codes']) for i in ids_]
    if sum(a_) + sum(b_) == 0: continue
    n_ = len(a_); po_ = sum(x == y for x, y in zip(a_, b_)) / n_; pa_ = sum(a_) / n_; pb_ = sum(b_) / n_; pe_ = pa_ * pb_ + (1 - pa_) * (1 - pb_)
    kp_ = (po_ - pe_) / (1 - pe_); kap_[CONTRIB_TR[k_]] = dict(po=po_ * 100, kappa=kp_)
R['contrib_rel']['per_code'] = kap_
R['contrib_rel']['kappa_min'] = min(v['kappa'] for v in kap_.values()); R['contrib_rel']['kappa_max'] = max(v['kappa'] for v in kap_.values())
R['pair_yolo_year'] = dict(y23=sum(1 for r in conf if r['year'] == 2023), y24=sum(1 for r in conf if r['year'] == 2024), v8_23=sum(1 for r in conf if r['year'] == 2023 and r['family'] == 'YOLOv8'), v8_24=sum(1 for r in conf if r['year'] == 2024 and r['family'] == 'YOLOv8'))
R['rescreen_counts'] = {f"{k[0]}|{k[1]}": v for k, v in collections.Counter((x['verdict'], x['evidence_level']) for x in RS.values()).items()}
R['verify_counts'] = collections.Counter((x['verdict'], x['evidence_level']) for x in wf['verify'])
R['verify_counts'] = {f'{a}|{b}': v for (a, b), v in R['verify_counts'].items()}

# ------- PRCI on the studies of the analysis set (criteria C1-C8 are stored as K1-K8)
K = ['K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7', 'K8']
C = ['C1a', 'C1b', 'C2a', 'C2b', 'C3a', 'C3b', 'C3c', 'C4a', 'C4b', 'C4c', 'C5a', 'C5b', 'C5c', 'C5d', 'C5e', 'C6a', 'C6b']
A, B = wf['coderA'], wf['coderB']
YEAR = {s['pid']: s['year'] for s in sel}; YEAR['P046'] = 2026   # Crossref: vol. 37, 2026
# K2 threshold and K6 epoch rule, settled after coding and reported as application rules (PRCI_codebook.md, section 'Application rules')
RECODE = {('P000', 'K2'): (1, 'Bölüm 4.2: 8:1:1; toplam 4.398 deniyor, parçalar 2.401 + 1.977 = 4.378 (fark %0,46); filtre sonrası 4.373; uygulama kuralına göre çelişki sayılmadı.'),
          ('P003', 'K2'): (0, 'Tablo 4: 4000/584/289 (4.873) kendi içinde tutarlı; §III.B’de her eğitim örneğinden iki çıktı üretildiği yazılı olduğundan (2.893−873)×2 = 4.040 ile tablodaki 4.000 arasındaki fark %1’i aşmıyor. Ancak metin Çin İHA görüntülerinin küçük bir kısmının kullanıldığını söylüyor, sayı yazılmamış; Tablo 3 ise alt kümenin resmî etiketlerinin tamamını (3.068) veriyor. Alt kümenin tamamı kullanıldıysa da 2.401+568 = 2.969 ile 2.893 arasındaki %2,6’lık fark açıklanmıyor. Uygulama kuralına göre çelişki sayıldı.'),
          ('P019', 'K2'): (0, 'Bölüm 4.2: 36.000 etiketli görüntüden yaklaşık 14.700 boş dosyanın çıkarıldığı, Çin İHA’nın kullanılmadığı ve seyrek sınıfların elendiği yazılı; bölmelerin toplamı ise 15.382 (10.798 + 3.042 + 1.542). 36.000’in Çin İHA’yı içerip içermediği yazılmamış (resmî eğitim sayısı Çin İHA hariç 35.984, dâhil 38.385); bu yüzden bu adımlardan sonra kalması gereken sayı yaklaşık 18.900 ile 21.300 arasındadır. Seyrek sınıf elemesinin kaç görüntü düşürdüğü yazılmadığından son toplamla aradaki yaklaşık 3.500–5.900 görüntülük (%19–28) fark sayı olarak açıklanmıyor; parçalar ile toplam arasında %1’i aşan fark olarak çelişki sayıldı.'),
          ('P033', 'K6'): (1, 'Bölüm 4.1: GTX 1080Ti, yığın 32, öğrenme oranı 0,01; metin 300 tur ile birlikte 150. epoktan söz ettiğinden tur epok anlamındadır; uygulama kuralına göre epok sayıldı (beş ayarın üçü).')}
for (p_, k_), (v_, why) in RECODE.items():
    prti[p_]['K'][k_]['first_pass'] = prti[p_]['K'][k_]['score']; prti[p_]['K'][k_]['score'] = v_; prti[p_]['K'][k_]['evidence'] = why
json.dump(prti, open(f'{O}/prci_final_v2.json', 'w'), ensure_ascii=False, indent=0)
rows = []
for s in sel:
    f = prti[s['pid']]; sc = {k: f['K'][k]['score'] for k in K}
    rows.append(dict(pid=s['pid'], short=s['short'], group=s['group'], year=YEAR[s['pid']], K=sc, total=sum(sc.values()), total7=sum(sc.values()) - sc['K8'], C=f['C'], code=f.get('code_url')))
N = len(rows)
R['prti_rows'] = rows
R['prti_crit'] = {k: sum(r['K'][k] for r in rows) for k in K}
t = [r['total'] for r in rows]
R['prti_median'] = st.median(t); R['prti_min'] = min(t); R['prti_max'] = max(t); R['prti_dist'] = dict(sorted(collections.Counter(t).items()))
R['prti_q1'], _, R['prti_q3'] = st.quantiles(t, n=4, method='inclusive')
off = [r for r in rows if r['group'] == 'i']; oth = [r for r in rows if r['group'] != 'i']
R['prti_off'] = [r['total'] for r in off]; R['prti_off7'] = [r['total7'] for r in off]
R['prti_oth_median'] = st.median(r['total'] for r in oth); R['prti_oth7_median'] = st.median(r['total7'] for r in oth); R['prti_oth7_max'] = max(r['total7'] for r in oth)
def rank(v):
    s_ = sorted(v); return [(s_.index(x) + 1 + s_.index(x) + s_.count(x)) / 2 for x in v]
def spearman(x, y):
    a, b = rank(x), rank(y); ma, mb = sum(a) / len(a), sum(b) / len(b)
    num = sum((p - ma) * (q - mb) for p, q in zip(a, b)); den = (sum((p - ma) ** 2 for p in a) * sum((q - mb) ** 2 for q in b)) ** .5
    return num / den
xs = [r['year'] for r in rows]; ys = [r['total'] for r in rows]
rho = spearman(xs, ys); rng = random.Random(2026); hits = 0
for _ in range(20000):
    z = ys[:]; rng.shuffle(z)
    if abs(spearman(xs, z)) >= abs(rho) - 1e-12: hits += 1
R['prti_rho'] = rho; R['prti_rho_p'] = hits / 20000
R['prti_by_year'] = {y: [r['total'] for r in rows if r['year'] == y] for y in sorted(set(xs))}
R['prti_by_group'] = {g: [r['total'] for r in rows if r['group'] == g] for g in ('i', 'ii', 'iii', 'iv')}
# agreement of the two assessments (same coder, different times) before adjudication
def kappa(a, b):
    n = len(a); po = sum(x == y for x, y in zip(a, b)) / n; pa = sum(a) / n; pb = sum(b) / n; pe = pa * pb + (1 - pa) * (1 - pb)
    return po, ((po - pe) / (1 - pe) if pe < 1 else None)
allA, allB = [], []; per = {}
ids = [r['pid'] for r in rows]
for k in K:
    a = [A[i]['K'][k]['score'] for i in ids]; b = [B[i]['K'][k]['score'] for i in ids]; allA += a; allB += b
    po, kp = kappa(a, b); per[k] = dict(po=po * 100, kappa=kp)
R['prti_rel'] = per; po, kp = kappa(allA, allB); R['prti_rel_all'] = dict(po=po * 100, kappa=kp, n=len(allA), disagree=sum(x != y for x, y in zip(allA, allB)))
R['prti_disputes_in_set'] = [d['pid'] for d in wf['disputes'] if d['pid'] in ids]
# details of the two coding rounds within the analysis set (all items: PRCI criteria, checklist sub-items, comparability variables)
R['prti_disputes_items'] = {d['pid']: [i_['item'] for i_ in d['items']] for d in wf['disputes'] if d['pid'] in ids}
R['prti_adjudications_in_set'] = [(a_['pid'], a_['item']) for a_ in wf['adjudications'] if a_['pid'] in ids]
R['prti_rel_counts'] = {k: dict(agree=sum(A[i]['K'][k]['score'] == B[i]['K'][k]['score'] for i in ids), n=len(ids)) for k in K}
_pe = lambda a, b: (sum(a) / len(a)) * (sum(b) / len(b)) + (1 - sum(a) / len(a)) * (1 - sum(b) / len(b))
R['prti_rel_all']['pe_pooled'] = _pe(allA, allB)
R['prti_rel_all']['pe_mean_within'] = st.mean(_pe([A[i]['K'][k]['score'] for i in ids], [B[i]['K'][k]['score'] for i in ids]) for k in K)
ids_x = [i for i in ids if i != 'P027']   # federated learning study: different full-text access in the two rounds
R['prti_rel_excl_P027'] = dict(agree=sum(A[i]['K'][k]['score'] == B[i]['K'][k]['score'] for i in ids_x for k in K), n=len(ids_x) * len(K))
R['prti_disagree_by_study'] = {i: [k for k in K if A[i]['K'][k]['score'] != B[i]['K'][k]['score']] for i in ids if any(A[i]['K'][k]['score'] != B[i]['K'][k]['score'] for k in K)}
# effect of the application rules on the headline numbers
def prti_scenario(over):
    tot = {r['pid']: sum({**r['K'], **over.get(r['pid'], {})}[k] for k in K) for r in rows}
    k2 = sum({**r['K'], **over.get(r['pid'], {})}['K2'] for r in rows); k6 = sum({**r['K'], **over.get(r['pid'], {})}['K6'] for r in rows)
    v = [tot[r['pid']] for r in rows]; o = [tot[r['pid']] for r in rows if r['group'] != 'i']; o7 = [tot[r['pid']] - {**r['K'], **over.get(r['pid'], {})}['K8'] for r in rows if r['group'] != 'i']
    yrs = [r['year'] for r in rows]; rho_ = spearman(yrs, v); rng_ = random.Random(2026); h_ = 0
    for _ in range(20000):
        z_ = v[:]; rng_.shuffle(z_)
        if abs(spearman(yrs, z_)) >= abs(rho_) - 1e-12: h_ += 1
    return dict(K2=k2, K6=k6, median=st.median(v), oth_median=st.median(o), oth7_median=st.median(o7), rho=rho_, p=h_ / 20000, dist=dict(sorted(collections.Counter(v).items())))
R['prti_no_rules'] = prti_scenario({'P000': {'K2': 0}, 'P019': {'K2': 1}, 'P033': {'K6': 0}})   # first adjudicated decisions
R['prti_strict_reason'] = prti_scenario({'P002': {'K2': 0}, 'P026': {'K2': 0}})   # a written reason required for every selection, not only a written selection
# CrackLite-Net (P234) also states a 6,000-image selection; whether it states the reason was not coded, so this variant is reported separately
R['prti_strict_reason_plus_P234'] = prti_scenario({'P002': {'K2': 0}, 'P026': {'K2': 0}, 'P234': {'K2': 0}})
R['prti_by_year_median'] = {y: st.median(v) for y, v in R['prti_by_year'].items()}
R['prti_by_group_median'] = {g: (st.median(v) if v else None) for g, v in R['prti_by_group'].items()}
ft_ = [p_ for p_, f_ in prti.items() if f_['access_level'] == 'tam_metin']
R['ft26_strict'] = dict(K2=sum(prti[p_]['K']['K2']['score'] for p_ in ft_) - 2, median=st.median(sum(prti[p_]['K'][k]['score'] for k in K) - (p_ in ('P002', 'P026')) for p_ in ft_))
# checklist
R['checklist'] = {c: sum(1 for r in rows if r['C'][c]) for c in C}
all_of = lambda cs: sum(1 for r in rows if all(r['C'][c] for c in cs))
R['checklist_all'] = dict(sinif=R['checklist']['C1a'], resmi=all_of(['C2a', 'C2b']), bolme=all_of(['C3a', 'C3b', 'C3c']), metrik=all_of(['C4a', 'C4b', 'C4c']), verim=all_of(['C5a', 'C5b', 'C5c', 'C5d', 'C5e']), kod=all_of(['C6a', 'C6b']))
R['checklist_extra_class'] = sum(1 for r in rows if not r['C']['C1a'])
R['checklist_extra_reported'] = sum(1 for r in rows if not r['C']['C1a'] and r['C']['C1b'])
# ------- comparability matrix (main experiment of each study, normalised from the coded fields)
M = {  # subset composition, class set, test definition, split
 'P016': ('6 ülke', '4', 'resmi', 'resmi'), 'P334': ('6 ülke', '4', 'resmi', 'resmi'),
 'P002': ('6 ülke', '4', 'dogrulama', '8:2'), 'P011': ('5 ülke', '4', 'tanimsiz', 'tanimsiz'), 'P019': ('6 ülke, Çin İHA hariç', '4', 'ayri', '7:2:1'),
 'P033': ('6 ülke', '4', 'ayri', '7:1:2'), 'P161': ('Çin + Çekya + ABD', '5', 'ayri', '7:1:2'), 'P260': ('6 ülke', '4', 'ayri', '8:1:1'),
 'P000': ('Çin', '5', 'ayri', '8:1:1'), 'P010': ('Çin', '6', 'ayri', '8:1:1'), 'P026': ('Çin', '5', 'ayri', '7:2:1'), 'P035': ('Çin', '5', 'ayri', '8:1:1'),
 'P046': ('Çin İHA', '4', 'dogrulama', 'tanimsiz'), 'P075': ('Çin', '5', 'ayri', '7:2:1'), 'P106': ('Çin İHA', '4', 'ayri', '8:1:1'), 'P401': ('Çin', '4', 'ayri', '8:1:1'),
 'P003': ('Çin İHA + İspanya', '5', 'dogrulama', 'özel'), 'P027': ('Japonya + Hindistan + ABD', '4', 'ayri', '9:1'),
 # coded test_def 'dis_test' (external / cross-dataset test of a model trained on another dataset) is kept as its own category
 'P234': ('Belirtilmemiş (6.000 görüntü seçimi)', '4', 'dis', '8:1:1'), 'P235': ('Çin', '5', 'ayri', '7:1:2'), 'P440': ('Hindistan + Japonya + Çekya', '4', 'dis', 'tanimsiz')}
order = [r['pid'] for r in sorted(rows, key=lambda r: (['i', 'ii', 'iii', 'iv'].index(r['group']), r['pid']))]
mat = {}; pairs = []
for a_ in range(len(order)):
    for b_ in range(a_ + 1, len(order)):
        x, y = M[order[a_]], M[order[b_]]
        same = [x[i] == y[i] for i in range(4)]
        pairs.append(dict(a=order[a_], b=order[b_], subset=same[0], classes=same[1], test=same[2], split=same[3], three=all(same[:3]), four=all(same)))
R['pairs_total'] = len(pairs); R['pairs_subset'] = sum(p['subset'] for p in pairs); R['pairs_classes'] = sum(p['classes'] for p in pairs); R['pairs_test'] = sum(p['test'] for p in pairs)
R['pairs_three'] = [(p['a'], p['b']) for p in pairs if p['three']]; R['pairs_four'] = [(p['a'], p['b']) for p in pairs if p['four']]
R['pairs_two_plus'] = sum(1 for p in pairs if sum([p['subset'], p['classes'], p['test']]) >= 2); R['pairs_zero'] = sum(1 for p in pairs if sum([p['subset'], p['classes'], p['test']]) == 0)
R['matrix_order'] = order; R['matrix_vars'] = M
R['class_counts'] = dict(collections.Counter(M[i][1] for i in order)); R['test_counts'] = dict(collections.Counter(M[i][2] for i in order))
G0_ = {r['pid']: r['group'] for r in rows}
R['pairs_within'] = sum(1 for p in pairs if G0_[p['a']] == G0_[p['b']]); R['pairs_between'] = len(pairs) - R['pairs_within']
R['pairs_three_between'] = sum(1 for p in pairs if p['three'] and G0_[p['a']] != G0_[p['b']])
_pc = lambda v: round(v / len(pairs) * 100, 1)
R['pairs_pct'] = dict(subset=_pc(R['pairs_subset']), classes=_pc(R['pairs_classes']), test=_pc(R['pairs_test']), three=_pc(len(R['pairs_three'])), four=_pc(len(R['pairs_four'])), zero=_pc(R['pairs_zero']), two_plus=_pc(R['pairs_two_plus']))
# studies stating explicitly that the reported values come from their separate test split (sheet S11, last column)
EXPLICIT_TEST = ['P019', 'P033', 'P161', 'P401', 'P027']
R['test_ayri_explicit'] = [i for i in order if M[i][2] == 'ayri' and i in EXPLICIT_TEST]; R['test_ayri_not_explicit'] = [i for i in order if M[i][2] == 'ayri' and i not in EXPLICIT_TEST]
# ------- reported own-split mAP@0.5 values
VAL = {  # (study, value, number of classes) as coded from the source tables
 'ii': [('P002', 70.6, '4'), ('P019', 67.8, '4'), ('P161', 71.5, '5'), ('P260', 65.3, '4'), ('P033', 65.7, '4')],
 'iii': [('P000', 90.7, '5'), ('P075', 91.4, '5'), ('P035', 86.0, '5'), ('P401', 86.0, '4'), ('P026', 77.4, '5'), ('P010', 75.7, '6'), ('P046', 67.6, '4'), ('P046', 86.6, '4'), ('P106', 51.7, '4'), ('P106', 79.1, '4'),
         ('P235', 85.8, '5')]}   # RSF-DETR: Tables 4-5, 7:1:2 split; test split defined but the source split of the values is not stated
# reported values kept out of all medians, ranges and gain statistics (marked in the tables):
# P011 93.5 (test split undefined; OUTLIER below) and P234 61.2 ('mAP' without an IoU threshold, cross-dataset test of a model trained on another dataset)
VAL_EXCLUDED = {'P011': (93.5, '4', 'test split undefined'), 'P234': (61.2, '4', 'mAP without IoU threshold; cross-dataset test of a model trained on another dataset')}
R['values_excluded'] = VAL_EXCLUDED
OUTLIER = 93.5
m2, m3 = st.median(v for _, v, _ in VAL['ii']), st.median(v for _, v, _ in VAL['iii'])
R['values'] = VAL; R['med_ii'] = m2; R['med_iii'] = m3; R['gap'] = m3 - m2; R['n_ii'] = len(VAL['ii']); R['n_iii'] = len(VAL['iii'])
R['rng_ii'] = (min(v for _, v, _ in VAL['ii']), max(v for _, v, _ in VAL['ii'])); R['rng_iii'] = (min(v for _, v, _ in VAL['iii']), max(v for _, v, _ in VAL['iii']))
ii4 = [v for _, v, c in VAL['ii'] if c == '4']; iii4 = [v for _, v, c in VAL['iii'] if c == '4']; iii5 = [v for _, v, c in VAL['iii'] if c != '4']
R['med_ii4'] = st.median(ii4); R['med_iii4'] = st.median(iii4); R['med_iii5'] = st.median(iii5); R['gap4'] = R['med_iii4'] - R['med_ii4']; R['n_ii4'] = len(ii4); R['n_iii4'] = len(iii4); R['n_iii5'] = len(iii5)
ii_all = [v for _, v, _ in VAL['ii']]; iii_all = [v for _, v, _ in VAL['iii']]
vars_ = {'taban': (m3, m2), 'aykırı eklendi': (m3, st.median(ii_all + [OUTLIER])), 'resmî grup ek sonuçları': (st.median(iii_all + [84.4]), st.median(ii_all + [62.5])),
         'ikisi birden': (st.median(iii_all + [84.4]), st.median(ii_all + [62.5, OUTLIER]))}
R['sensitivity'] = {k: dict(iii=a, ii=b, gap=a - b) for k, (a, b) in vars_.items()}
ALL_FT = [p_ for p_, f_ in prti.items() if f_['access_level'] == 'tam_metin']
R['ft26_crit'] = {k: sum(prti[p_]['K'][k]['score'] for p_ in ALL_FT) for k in K}; R['ft26_n'] = len(ALL_FT)
t26 = [sum(prti[p_]['K'][k]['score'] for k in K) for p_ in ALL_FT]; R['ft26_median'] = st.median(t26); R['ft26_min'] = min(t26); R['ft26_max'] = max(t26)
R['outside_k'] = {k: sum(prti[p_]['K'][k]['score'] for p_ in ALL_FT if p_ not in ids) for k in K}
R['outside_ids'] = [p_ for p_ in ALL_FT if p_ not in ids]; R['outside_n'] = len(R['outside_ids'])
# one value per study (China motorbike or drone choice shown as a range)
def med(v): return st.median(v)
one_a = [v for p_, v, _ in VAL['iii'] if p_ not in ('P046', 'P106')] + [67.6, 51.7]; one_b = [v for p_, v, _ in VAL['iii'] if p_ not in ('P046', 'P106')] + [86.6, 79.1]   # UAV or motorbike value of YOLO-ROC and ALC-Net
R['sens_one_value'] = dict(a=med(one_a), b=med(one_b), gap_a=med(one_a) - m2, gap_b=med(one_b) - m2)
base3 = iii_all; base2 = ii_all
opts = {'taban': (base3, base2), 'ek_resmi': (base3 + [84.4], base2 + [62.5]), 'belirsiz_test': (base3, base2 + [93.5, 90.1]), 'ikisi': (base3 + [84.4], base2 + [62.5, 93.5, 90.1]),
        'dogrulama_cikar': ([v for v in base3 if v != 67.6], [v for v in base2 if v != 70.6]), 'belirsiz_motosiklet_cikar': ([v for v in base3 if v != 86.6], base2)}
R['sens_all'] = {k: dict(iii=med(a_), ii=med(b_), gap=med(a_) - med(b_)) for k, (a_, b_) in opts.items()}
R['sens_range'] = (min(v['gap'] for v in R['sens_all'].values()), max(v['gap'] for v in R['sens_all'].values()))
R['sens_one_value']['n'] = len(one_a)
# only values explicitly stated to come from the test split
R['explicit_test_values'] = dict(ii=[v for p_, v, _ in VAL['ii'] if p_ in EXPLICIT_TEST], iii=[v for p_, v, _ in VAL['iii'] if p_ in EXPLICIT_TEST])
R['explicit_test_values']['med_ii'] = med(R['explicit_test_values']['ii']); R['explicit_test_values']['med_iii'] = med(R['explicit_test_values']['iii'])
# sensitivity only (the manuscript excludes it): CrackLite-Net's unthresholded 61.2% added to group (ii)
_ii234 = ii_all + [61.2]; _ii4_234 = ii4 + [61.2]
R['sens_with_P234'] = dict(n_ii=len(_ii234), med_ii=med(_ii234), gap=m3 - med(_ii234), rng_ii=(min(_ii234), max(_ii234)), med_ii4=med(_ii4_234), gap4=R['med_iii4'] - med(_ii4_234))
# stricter subset coding: sampled selections counted as different subsets
M2 = dict(M); M2['P002'] = ('6 ülke: 10.000 seçim',) + M['P002'][1:]; M2['P026'] = ('Çin: 2.000 seçim',) + M['P026'][1:]; M2['P401'] = ('Çin: 3.853 seçim',) + M['P401'][1:]; M2['P033'] = ('6 ülke: sayılar bağdaşmıyor',) + M['P033'][1:]; M2['P106'] = ('Çin İHA: 1.919 görüntü',) + M['P106'][1:]
p2 = []
G_ = {r['pid']: r['group'] for r in rows}
within = 0; within3 = 0
for a_ in range(len(order)):
    for b_ in range(a_ + 1, len(order)):
        x, y = M2[order[a_]], M2[order[b_]]; same = [x[i] == y[i] for i in range(4)]; p2.append(same)
        x0, y0 = M[order[a_]], M[order[b_]]
        if G_[order[a_]] == G_[order[b_]]:
            within += 1; within3 += all(x0[i] == y0[i] for i in range(3))
R['strict_studies'] = ['P002', 'P026', 'P401', 'P033', 'P106']; R['strict_pairs'] = [(order[a_], order[b_]) for a_ in range(len(order)) for b_ in range(a_ + 1, len(order)) if M2[order[a_]][0] == M2[order[b_]][0]]
R['strict_subset'] = sum(p[0] for p in p2); R['strict_three'] = sum(all(p[:3]) for p in p2); R['strict_four'] = sum(all(p) for p in p2)
R['within_pairs'] = within; R['within_three'] = within3
# reported gains (proposed minus baseline, main experiment)
GAIN = {'P000': (87.4, 90.7), 'P075': (88.2, 91.4), 'P035': (84.2, 86.0), 'P401': (82.4, 86.0), 'P026': (74.6, 77.4), 'P010': (69.9, 75.7), 'P046': (66.2, 67.6), 'P106': (49.3, 51.7), 'P002': (69.2, 70.6), 'P019': (65.91, 67.81),
        'P161': (70.85, 71.49), 'P260': (63.6, 65.3), 'P033': (61.8, 65.7), 'P011': (78.3, 93.5), 'P016': (59.9, 62.5), 'P334': (81.5, 84.4), 'P235': (83.9, 85.8)}
GAIN_EXCLUDED = {'P234': (60.8, 61.2)}   # unthresholded mAP in a cross-dataset test; YOLO-MCG (P440) reports no RDD2022 baseline result
R['gain_excluded'] = GAIN_EXCLUDED
g_ = {k: round(b - a, 2) for k, (a, b) in GAIN.items()}
R['gain_median_excl_official'] = med(v_ for k_, v_ in g_.items() if k_ not in ('P016', 'P334'))
R['gains'] = g_; R['gain_median'] = med(g_.values()); R['gain_min'] = min(g_.values()); R['gain_max_excl_cd'] = max(v for k, v in g_.items() if k != 'P011'); R['gain_cd'] = g_['P011']; R['gain_table'] = GAIN
R['gain_n'] = len(g_); R['gain_median_excl_cd'] = med(v for k, v in g_.items() if k != 'P011')
_g234 = list(g_.values()) + [round(GAIN_EXCLUDED['P234'][1] - GAIN_EXCLUDED['P234'][0], 2)]
R['gain_with_P234'] = dict(n=len(_g234), median=med(_g234), min=min(_g234))   # sensitivity only
R['repair_iii'] = sum(1 for r in rows if r['group'] == 'iii' and M[r['pid']][1] != '4'); R['n_iii_studies'] = sum(1 for r in rows if r['group'] == 'iii'); R['repair_ii'] = sum(1 for r in rows if r['group'] == 'ii' and M[r['pid']][1] != '4'); R['n_ii_studies'] = sum(1 for r in rows if r['group'] == 'ii')
json.dump(R, open(f'{O}/results.json', 'w'), ensure_ascii=False, indent=1, default=str)
for k, v in R.items():
    if k in ('prti_rows', 'family_year', 'matrix_vars', 'values'): continue
    print(k, ':', v)
for r in rows: print(r['short'][:30].ljust(31), r['group'].ljust(4), r['year'], r['K'], r['total'])
