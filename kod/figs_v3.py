"""Figures for the BJESR manuscript (400 dpi, Times New Roman). Palette: validated categorical order, single-hue sequential."""
import json, os, sys, statistics as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
_res = os.path.join(HERE, 'results.json')   # the archive keeps results.json next to this script
R = json.load(open(_res if os.path.exists(_res) else os.path.join(HERE, '..', 'out', 'results.json')))
for f in ['Times New Roman.ttf', 'Times New Roman Bold.ttf', 'Times New Roman Italic.ttf']:
    fm.fontManager.addfont('/System/Library/Fonts/Supplemental/' + f)
plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 10, 'axes.titlesize': 10, 'axes.labelsize': 10, 'xtick.labelsize': 9.5, 'ytick.labelsize': 9.5,
                     'legend.fontsize': 9, 'axes.spines.top': False, 'axes.spines.right': False, 'savefig.dpi': 400, 'axes.linewidth': 0.7})
INK, MUTED, GRID = '#222222', '#555555', '#E2E2E2'
CAT = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#6250d6', '#e34948']
BLUE = '#2a78d6'
LINE = '#1F4E79'
TR = lambda x: f'{x}'.replace('.', ',')

def fig1():
    S, TG, OT = R['flow'], R['targeted'], R['other']
    fig, ax = plt.subplots(figsize=(6.3, 6.9))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
    def box(x, y, w, h, lines, bold_first=True, fc='#FFFFFF', ls='-', fs=7.8):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.2,rounding_size=0.8', fc=fc, ec=LINE, lw=0.8, ls=ls))
        n = len(lines); step = 2.5; top = y + h / 2 + (n - 1) * step / 2
        for i, t in enumerate(lines):
            ax.text(x + w / 2, top - i * step, t, ha='center', va='center', fontsize=fs, fontweight='bold' if (bold_first and i == 0) else 'normal', color=INK)
    def arrow(x1, y1, x2, y2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='-|>', color=LINE, lw=0.8, mutation_scale=8))
    for (y0, y1, lab) in [(80, 100, 'Tanımlama'), (42, 79, 'Tarama'), (15.5, 41, 'Dâhil etme'), (0, 14.5, 'Analiz')]:
        ax.add_patch(FancyBboxPatch((0, y0 + 0.4), 4.2, y1 - y0 - 0.8, boxstyle='round,pad=0.1,rounding_size=0.6', fc='#DEEBF7', ec='none'))
        ax.text(2.1, (y0 + y1) / 2, lab, rotation=90, ha='center', va='center', fontsize=9, fontweight='bold', color=LINE)
    # columns
    L, LW, M, MW, Rx, RW = 6, 30.5, 38, 27.5, 67, 32
    LC, RC = L + LW / 2, Rx + RW / 2
    # identification
    box(L, 82, LW, 16.5, ['OpenAlex (12 Ekim 2026)', 'Atıf sorguları: 144 + 75 + 10', 'Metin sorguları: 417 + 46 + 224', 'Benzersiz kayıt (n = 572)'])
    box(M, 83.5, MW, 13.5, ['Taramadan önce çıkarılan', '(n = 18)', 'Anahtar sözcük filtresi: 16', 'Düzeltme ve ek kaydı: 2'])
    box(Rx, 82, RW, 16.5, ['Diğer yöntemler', 'Hedefli tarama (12 Ekim 2026):', 'benzersiz kayıt sayısı tutulmadı', 'Belgelenmiş (2 Kasım 2026):', '281 kayıt ve 29 web sorgusu'])
    arrow(L + LW, 90.2, M, 90.2)
    # screening
    box(L, 67, LW, 9, ['Özet düzeyinde taranan', '(n = 554)'])
    arrow(LC, 82, LC, 76)
    box(M, 44.5, MW, 31.5, [f"Dışlanan kayıtlar (n = {S['excluded']})", f"İlgili çalışma: {S['rel_unclear'] + S['rel_no']}", f"(kullanım belirsiz {S['rel_unclear']},", f"kullanılmıyor {S['rel_no']})", f"Veri seti makalesi/kaydı: {S['dataset']}", f"Derleme: {S['survey']}", f"Teyit edilemeyen: {S['unv_oa']}", '(kayıt bazlı denetim)', f"Özet düzeyinde konu dışı: {S['irrelevant']}", f"Yayın türü uygun değil: {S['pubtype']}"])
    arrow(L + LW, 71.5, M, 71.5)
    box(L, 47, LW, 9, ['Doğrudan kullanım', f"(n = {S['direct']})"])
    arrow(LC, 67, LC, 56)
    box(Rx, 66.5, RW, 11, [f"Değerlendirilen (n = {OT['assessed']})", f"Hedefli tarama: {TG['assessed']}", 'Belgelenmiş: 24 + 15 yeni aday'])
    arrow(RC, 82, RC, 77.5)
    box(Rx, 44.5, RW, 16.5, [f"Eklenmeyen (n = {OT['not_added']})", f"Teyit edilemeyen: {TG['unv'] + 1}", 'Bibliyografik doğrulanamayan: 2', f"Kullanmayan veya konu dışı: {OT['reg_not_using'] + 8 + TG['not_using']}", f"Yinelenen sürüm: {3 + TG['merged']}", f"Yayın türü uygun değil: {2 + TG['pubtype']}"])
    arrow(RC, 66.5, RC, 61)
    # inclusion
    box(L, 31, LW, 8, ['OpenAlex’ten dâhil edilen', f"(n = {S['oa_conf']})"])
    box(M, 31, MW, 8, ['Birleştirilen yinelenen', f"kayıt (n = {S['merged']})"])
    box(Rx, 31, RW, 8, ['Tamamlayıcı taramalarla', f"eklenen (n = {OT['added']})"])
    arrow(LC, 47, LC, 39); ax.plot([LC, M + MW / 2], [41.5, 41.5], color=LINE, lw=0.8); arrow(M + MW / 2, 41.5, M + MW / 2, 39); arrow(92, 44.5, 92, 39)
    box(L, 17.5, 93, 8, [f"Sınıflandırmaya dâhil edilen, kullanımı teyit edilen çalışmalar (n = {R['n_conf']})", 'Model ailesi, katkı türü ve yayın yılı (Bölüm 3.2.1 ve 3.2.2)'], fc='#F2F2F2')
    arrow(LC, 31, LC, 25.5); arrow(RC, 31, RC, 25.5)
    # analysis
    w = 21.25; gap = 8 / 3; xs = [L + i * (w + gap) for i in range(4)]
    box(xs[0], 1.5, w, 11, ['Ayrıntılı inceleme', '(n = 43)', '40 çalışma + 2 kayıt', '+ 1 derleme'])
    box(xs[1], 1.5, w, 11, ['Protokole atanabilen', '(n = 31)'])
    box(xs[2], 1.5, w, 11, ['Uygunluk ölçütleri', '(n = 21)', 'Dört ölçüt'])
    box(xs[3], 1.5, w, 11, ['Protokol analizi,', 'PRTİ (n = 18)', 'Kaynak sınırı kuralı'], fc='#F2F2F2')
    for i in range(3): arrow(xs[i] + w, 7, xs[i + 1], 7)
    arrow(xs[0] + w / 2, 17.5, xs[0] + w / 2, 12.5)
    fig.savefig(os.path.join(OUT, 'sekil1_prisma_akis.png'), bbox_inches='tight', pad_inches=0.03); plt.close(fig)

def fig2():
    Y = R['years']
    keys = [('core', "RDD2022'yi kullanan, teyit edilmiş (OpenAlex)"), ('web', 'Tamamlayıcı taramalarla eklenen, teyit edilmiş'), ('unverified', 'Kullanımı teyit edilemeyen'),
            ('related', 'İlgili çalışma (kullanımı belirsiz veya kullanmayan)'), ('survey', 'Derleme'), ('dataset', 'Veri seti makalesi veya kaydı')]
    fig, ax = plt.subplots(figsize=(6.3, 2.85))
    x = range(len(Y)); bottom = [0] * len(Y)
    for (k, lab), c in zip(keys, CAT):
        v = [y[k] for y in Y]
        ax.bar(x, v, 0.58, bottom=bottom, color=c, label=lab, edgecolor='white', linewidth=0.6)
        bottom = [b + q for b, q in zip(bottom, v)]
    for i, t in enumerate(bottom): ax.text(i, t + 3, str(t), ha='center', va='bottom', fontsize=9, color=INK)
    ax.set_xticks(list(x)); ax.set_xticklabels([f"{y['y']}{'*' if y['y'] == 2026 else ''}" for y in Y])
    ax.set_ylabel('Kayıt sayısı'); ax.set_ylim(0, 260); ax.yaxis.grid(True, color=GRID, lw=0.5); ax.set_axisbelow(True)
    ax.legend(loc='upper left', frameon=False, ncol=1)
    ax.text(1.0, -0.17, '* 12 Ekim 2026 itibarıyla', transform=ax.transAxes, ha='right', fontsize=8.5, style='italic', color=MUTED)
    fig.savefig(os.path.join(OUT, 'sekil2_yillik_yayin.png'), bbox_inches='tight', pad_inches=0.03); plt.close(fig)

def fig3():
    FY = R['family_year']; yrs = [2022, 2023, 2024, 2025, 2026]
    groups = [('YOLOv8', ['YOLOv8']), ('YOLO11', ['YOLO11']), ('YOLOv5', ['YOLOv5']), ('YOLOv7', ['YOLOv7']), ('Diğer YOLO sürümleri', ['YOLO (diğer)', 'YOLOv10', 'YOLOv12', 'YOLOv9', 'YOLO26']),
              ('RT-DETR / DETR', ['RT-DETR', 'DETR ailesi']), ('Topluluk (ensemble)', ['Topluluk (ensemble)'])]
    used = {n for _, ns in groups for n in ns}; groups.append(('Diğer', [f for f in FY if f not in used]))
    fig, ax = plt.subplots(figsize=(6.3, 2.85)); bottom = [0] * 5
    for (lab, names), c in zip(groups, CAT):
        v = [sum(FY.get(n, {}).get(str(y), 0) for n in names) for y in yrs]
        ax.bar(range(5), v, 0.58, bottom=bottom, color=c, label=f'{lab} ({sum(v)})', edgecolor='white', linewidth=0.6)
        bottom = [b + q for b, q in zip(bottom, v)]
    for i, t in enumerate(bottom): ax.text(i, t + 1.5, str(t), ha='center', va='bottom', fontsize=9, color=INK)
    ax.set_xticks(range(5)); ax.set_xticklabels([str(y) + ('*' if y == 2026 else '') for y in yrs])
    ax.set_ylabel('Çalışma sayısı'); ax.yaxis.grid(True, color=GRID, lw=0.5); ax.set_axisbelow(True)
    ax.legend(loc='upper left', frameon=False, ncol=2); ax.set_ylim(0, max(bottom) * 1.55)
    ax.text(1.0, -0.17, '* 12 Ekim 2026 itibarıyla', transform=ax.transAxes, ha='right', fontsize=8.5, style='italic', color=MUTED)
    fig.savefig(os.path.join(OUT, 'sekil3_model_aileleri.png'), bbox_inches='tight', pad_inches=0.03); plt.close(fig)

# own-split mAP@0.5 results of groups (ii) and (iii): (value, class set, test definition)
II = [(70.6, '4', 'dogrulama'), (67.8, '4', 'ayri'), (71.5, '5', 'ayri'), (65.3, '4', 'ayri'), (65.7, '4', 'ayri')]
III = [(90.7, '5', 'ayri'), (91.4, '5', 'ayri'), (86.0, '5', 'ayri'), (86.0, '4', 'ayri'), (77.4, '5', 'ayri'), (75.7, '6', 'ayri'), (67.6, '4', 'dogrulama'), (86.6, '4', 'belirsiz'), (51.7, '4', 'ayri'), (79.1, '4', 'ayri')]
OFFICIAL = [('YOLOv8x (temel)', 0.668), ('RDD-YOLO', 0.696), ('CRDDC’2022 3.', 0.741), ('CRDDC’2022 2.', 0.743), ('CRDDC’2022 1.', 0.770), ('StripRFNet', 0.803)]

def fig4():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.3, 3.3), gridspec_kw={'width_ratios': [1.1, 1.0], 'wspace': 0.5})
    for i, (vals, c) in enumerate([(II, CAT[0]), (III, CAT[1])]):
        for j, (v, cl, td) in enumerate(sorted(vals)):
            xp = i + ((j % 5) - 2) * 0.075
            a.scatter([xp], [v], s=26, marker='o' if cl == '4' else '^', facecolor=c if td == 'ayri' else 'white', edgecolor=c if td != 'ayri' else 'white', linewidth=1.0 if td != 'ayri' else 0.5, zorder=3)
        a.hlines(st.median(v for v, _, _ in vals), i - 0.27, i + 0.27, color=INK, lw=1.3, zorder=4)
        a.text(i + 0.3, st.median(v for v, _, _ in vals), '%' + TR(st.median(v for v, _, _ in vals)), va='center', fontsize=9, color=INK)
    a.scatter([0.18], [93.5], s=20, marker='x', color=MUTED, zorder=3, linewidth=1)
    a.annotate('test bölmesi tanımsız', (0.18, 93.5), xytext=(-0.43, 97.3), fontsize=8.5, color=MUTED, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.5))
    a.set_xticks([0, 1]); a.set_xticklabels([f'(ii) Çok ülkeli\n({len(II)} sonuç)', f'(iii) Çin\n({len(III)} sonuç)'])
    a.set_xlim(-0.5, 1.8); a.set_ylim(45, 100); a.set_ylabel('Bildirilen mAP@0.5 (%)')
    a.yaxis.grid(True, color=GRID, lw=0.5); a.set_axisbelow(True); a.set_title('(a) Kendi bölmeleriyle bildirilen sonuçlar', loc='left')
    hs = [Line2D([], [], marker='o', ls='', color=MUTED, ms=5, label='4 resmî sınıf'), Line2D([], [], marker='^', ls='', color=MUTED, ms=5, label='5 veya 6 sınıf'),
          Line2D([], [], marker='o', ls='', mfc='white', mec=MUTED, ms=5, label='Doğrulama test sayılmış\nveya test belirsiz'), Line2D([], [], color=INK, lw=1.3, label='Ortanca')]
    a.legend(handles=hs, loc='upper center', bbox_to_anchor=(0.5, -0.2), frameon=False, ncol=2, fontsize=8.5, columnspacing=1.0, handletextpad=0.4)
    labs = [l for l, _ in OFFICIAL]; vals = [v for _, v in OFFICIAL]
    b.barh(range(len(vals)), vals, color=BLUE, height=0.62)
    for i, v in enumerate(vals): b.text(v + 0.004, i, f'{v:.3f}'.replace('.', ','), va='center', fontsize=9, color=INK)
    b.set_yticks(range(len(vals))); b.set_yticklabels(labs, fontsize=9)
    b.set_xlim(0.6, 0.86); b.set_xticks([0.6, 0.7, 0.8]); b.set_xticklabels(['0,6', '0,7', '0,8']); b.set_xlabel('F1 (IoU > 0,5)')
    b.xaxis.grid(True, color=GRID, lw=0.5); b.set_axisbelow(True); b.set_title('(b) CRDDC’2022 resmî gizli test', loc='left')
    fig.savefig(os.path.join(OUT, 'sekil4_protokol_karsilastirma.png'), bbox_inches='tight', pad_inches=0.03); plt.close(fig)

LABEL = {'P016': 'RDD-YOLO', 'P334': 'StripRFNet', 'P002': 'YOLOv8-PD', 'P011': 'YOLOv8-CD', 'P019': 'İyil. YOLOv5s', 'P033': 'İyil. YOLOv8n', 'P161': 'RS-YOLOv11n', 'P260': 'YOLO_SE6',
         'P000': 'BL-YOLOv8', 'P010': 'İyil. YOLOv8s (a)', 'P026': 'İyil. YOLOv8s (b)', 'P035': 'OBC-YOLOv8', 'P046': 'YOLO-ROC', 'P075': 'YOLOv11s-ATL', 'P106': 'ALC-Net', 'P401': 'ELW-YOLO', 'P003': 'İHA çalışması', 'P027': 'Federe öğrenme'}

def fig5():
    order = R['matrix_order']; M = R['matrix_vars']; n = len(order)
    G = {r['pid']: r['group'] for r in R['prti_rows']}
    V = np.full((n, n), np.nan)
    for i in range(n):
        for j in range(i):
            V[i, j] = sum(M[order[i]][k] == M[order[j]][k] for k in range(3))
    ramp = ['#F3F7FC', '#BCD6F4', '#6AA5E8', '#1F5FAF']
    fig, ax = plt.subplots(figsize=(6.3, 5.0))
    im = ax.imshow(np.ma.masked_invalid(V), cmap=ListedColormap(ramp), norm=BoundaryNorm([-.5, .5, 1.5, 2.5, 3.5], 4))
    ax.set_xticks(range(n)); ax.set_yticks(range(n)); ax.set_xticklabels([LABEL[p] for p in order], rotation=60, ha='right', fontsize=8.5); ax.set_yticklabels([LABEL[p] for p in order], fontsize=8.5)
    ax.tick_params(length=0)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xticks(np.arange(-.5, n, 1), minor=True); ax.set_yticks(np.arange(-.5, n, 1), minor=True); ax.grid(which='minor', color='white', lw=1.2); ax.tick_params(which='minor', length=0)
    for i in range(n):
        for j in range(i):
            if not np.isnan(V[i, j]):
                ax.text(j, i, f'{int(V[i, j])}', ha='center', va='center', fontsize=7.5, color='white' if V[i, j] >= 2.5 else INK)
    # protocol-group boundaries
    idx = [next(k for k, p in enumerate(order) if G[p] == g) for g in ('ii', 'iii', 'iv')]
    for b_ in idx:
        ax.plot([-.5, b_ - .5], [b_ - .5, b_ - .5], color=INK, lw=0.7); ax.plot([b_ - .5, b_ - .5], [b_ - .5, n - .5], color=INK, lw=0.7)
    cax = fig.add_axes([0.62, 0.74, 0.25, 0.028])
    cb = fig.colorbar(im, cax=cax, orientation='horizontal', ticks=[0, 1, 2, 3]); cb.outline.set_visible(False); cb.ax.tick_params(labelsize=8.5, length=0)
    cb.set_label('Ortak boyut sayısı (alt küme, sınıf, test)', fontsize=8.5); cb.ax.xaxis.set_label_position('top')
    fig.savefig(os.path.join(OUT, 'sekil5_karsilastirilabilirlik.png'), bbox_inches='tight', pad_inches=0.03); plt.close(fig)

def fig6():
    NAMES = {'K1': 'Ülke alt kümesi', 'K2': 'Veri bölmesi', 'K3': 'Hasar sınıfları', 'K4': 'Metrik ve IoU', 'K5': 'Tekrar bilgisi', 'K6': 'Donanım ve ayarlar', 'K7': 'Kod veya ağırlık', 'K8': 'Test protokolü'}
    C = R['prti_crit']; N = len(R['prti_rows'])
    items = sorted(C.items(), key=lambda kv: (kv[1], kv[0]), reverse=False)
    fig, ax = plt.subplots(figsize=(6.3, 2.8))
    ax.barh(range(len(items)), [v / N * 100 for _, v in items], color=BLUE, height=0.62)
    for i, (k, v) in enumerate(items): ax.text(v / N * 100 + 1.2, i, f"{v}/{N} (%{TR(round(v / N * 100))})", va='center', fontsize=9, color=INK)
    ax.set_yticks(range(len(items))); ax.set_yticklabels([NAMES[k] for k, _ in items])
    ax.set_xlim(0, 118); ax.set_xticks([0, 25, 50, 75, 100]); ax.set_xlabel('Ölçütü karşılayan çalışma (%)')
    ax.xaxis.grid(True, color=GRID, lw=0.5); ax.set_axisbelow(True)
    fig.savefig(os.path.join(OUT, 'sekil6_prti_olcutleri.png'), bbox_inches='tight', pad_inches=0.03); plt.close(fig)

fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); print('ok')
