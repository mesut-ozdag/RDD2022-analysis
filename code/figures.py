"""Figures 1-6 of the manuscript (400 dpi, Times New Roman), drawn from results.json.
Usage: python3 figures.py <output_dir>  -> figure1.png ... figure6.png"""
import json, os, sys, statistics as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.transforms import Bbox
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
EN = lambda x: f'{x}'   # English number format: decimal point (no number in these figures needs a thousands separator)
DPI = 400
# Target canvas size of each figure in pixels. save() widens the canvas, with a printed note, only when the content does not fit.
SIZE_PX = {1: (1977, 2149), 2: (2169, 1061), 3: (2170, 1071), 4: (2178, 1544), 5: (2129, 1913), 6: (2441, 1053)}

def save(fig, n):
    """Save figure n at 400 dpi on a canvas of the target pixel size (SIZE_PX), centred on the tight bounding box of the content."""
    W, H = SIZE_PX[n]; w, h = W / DPI, H / DPI
    fig.set_dpi(DPI); fig.canvas.draw(); tb = fig.get_tightbbox(fig.canvas.get_renderer())
    if tb.width > w or tb.height > h:
        print(f'Note: figure{n} content ({tb.width:.3f} x {tb.height:.3f} in) exceeds the target canvas ({w:.3f} x {h:.3f} in); the canvas is widened to fit.')
        w = max(w, tb.width + 0.04); h = max(h, tb.height + 0.04)
    cx, cy = (tb.x0 + tb.x1) / 2, (tb.y0 + tb.y1) / 2
    fig.savefig(os.path.join(OUT, f'figure{n}.png'), dpi=DPI, bbox_inches=Bbox.from_bounds(cx - w / 2, cy - h / 2, w, h)); plt.close(fig)

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
    for (y0, y1, lab) in [(80, 100, 'Identification'), (42, 79, 'Screening'), (15.5, 41, 'Included'), (0, 14.5, 'Analysis')]:
        ax.add_patch(FancyBboxPatch((0, y0 + 0.4), 4.2, y1 - y0 - 0.8, boxstyle='round,pad=0.1,rounding_size=0.6', fc='#DEEBF7', ec='none'))
        ax.text(2.1, (y0 + y1) / 2, lab, rotation=90, ha='center', va='center', fontsize=9, fontweight='bold', color=LINE)
    # columns
    L, LW, M, MW, Rx, RW = 6, 30.5, 38, 27.5, 67, 32
    LC, RC = L + LW / 2, Rx + RW / 2
    # identification
    box(L, 82, LW, 16.5, ['OpenAlex (12 October 2026)', 'Citation queries: 144 + 75 + 10', 'Text queries: 417 + 46 + 224', 'Unique records (n = 572)'])
    box(M, 83.5, MW, 13.5, ['Removed before screening', '(n = 18)', 'Keyword filter: 16', 'Corrections/supplements: 2'])
    box(Rx, 82, RW, 16.5, ['Other methods', 'Targeted (12 October 2026):', 'unique records not counted', 'Documented (2 November 2026):', '281 records and 29 web queries'])
    arrow(L + LW, 90.2, M, 90.2)
    # screening
    box(L, 67, LW, 9, ['Screened at abstract level', '(n = 554)'])
    arrow(LC, 82, LC, 76)
    box(M, 44.5, MW, 31.5, [f"Records excluded (n = {S['excluded']})", f"Related work: {S['rel_unclear'] + S['rel_no']}", f"(use unclear {S['rel_unclear']},", f"not used {S['rel_no']})", f"Dataset paper/record: {S['dataset']}", f"Review article: {S['survey']}", f"Use not confirmed: {S['unv_oa']}", '(record-level check)', f"Off-topic at abstract level: {S['irrelevant']}", f"Ineligible publication type: {S['pubtype']}"])
    arrow(L + LW, 71.5, M, 71.5)
    box(L, 47, LW, 9, ['Direct use', f"(n = {S['direct']})"])
    arrow(LC, 67, LC, 56)
    box(Rx, 66.5, RW, 11, [f"Assessed (n = {OT['assessed']})", f"Targeted search: {TG['assessed']}", 'Documented search: 24', '+ 15 new candidates'])
    arrow(RC, 82, RC, 77.5)
    box(Rx, 44.5, RW, 16.5, [f"Not added (n = {OT['not_added']})", f"Use not confirmed: {TG['unv'] + 1}", 'Bibliographically unverifiable: 2', f"Not using or off-topic: {OT['reg_not_using'] + 8 + TG['not_using']}", f"Duplicate version: {3 + TG['merged']}", f"Ineligible publication type: {2 + TG['pubtype']}"])
    arrow(RC, 66.5, RC, 61)
    # inclusion
    box(L, 31, LW, 8, ['Included from OpenAlex', f"(n = {S['oa_conf']})"])
    box(M, 31, MW, 8, ['Merged duplicate', f"records (n = {S['merged']})"])
    box(Rx, 31, RW, 8, ['Added via supplementary', f"searches (n = {OT['added']})"])
    arrow(LC, 47, LC, 39); ax.plot([LC, M + MW / 2], [41.5, 41.5], color=LINE, lw=0.8); arrow(M + MW / 2, 41.5, M + MW / 2, 39); arrow(92, 44.5, 92, 39)
    box(L, 17.5, 93, 8, [f"Studies with confirmed use included in the classification (n = {R['n_conf']})", 'Model family, contribution type and publication year (Sections 3.1 and 3.2)'], fc='#F2F2F2')
    arrow(LC, 31, LC, 25.5); arrow(RC, 31, RC, 25.5)
    # analysis
    w = 21.25; gap = 8 / 3; xs = [L + i * (w + gap) for i in range(4)]
    box(xs[0], 1.5, w, 11, ['Detailed examination', '(n = 43)', '40 studies + 2 records', '+ 1 review article'])
    box(xs[1], 1.5, w, 11, ['Assignable to', 'a protocol group', '(n = 31)'])
    box(xs[2], 1.5, w, 11, ['Eligibility criteria', '(n = 21)', 'Four criteria'])
    box(xs[3], 1.5, w, 11, ['Protocol analysis,', 'comparability matrix', f"and PRCI (n = {len(R['prti_rows'])})"], fc='#F2F2F2')
    for i in range(3): arrow(xs[i] + w, 7, xs[i + 1], 7)
    arrow(xs[0] + w / 2, 17.5, xs[0] + w / 2, 12.5)
    save(fig, 1)

def fig2():
    Y = R['years']
    keys = [('core', 'Confirmed use of RDD2022 (OpenAlex)'), ('web', 'Confirmed use, added via supplementary searches'), ('unverified', 'Use not confirmed'),
            ('related', 'Related work (use unclear or not used)'), ('survey', 'Review article'), ('dataset', 'Dataset paper or record')]
    fig, ax = plt.subplots(figsize=(6.3, 2.85))
    x = range(len(Y)); bottom = [0] * len(Y)
    for (k, lab), c in zip(keys, CAT):
        v = [y[k] for y in Y]
        ax.bar(x, v, 0.58, bottom=bottom, color=c, label=lab, edgecolor='white', linewidth=0.6)
        bottom = [b + q for b, q in zip(bottom, v)]
    for i, t in enumerate(bottom): ax.text(i, t + 3, str(t), ha='center', va='bottom', fontsize=9, color=INK)
    ax.set_xticks(list(x)); ax.set_xticklabels([f"{y['y']}{'*' if y['y'] == 2026 else ''}" for y in Y])
    ax.set_ylabel('Number of records'); ax.set_ylim(0, 260); ax.yaxis.grid(True, color=GRID, lw=0.5); ax.set_axisbelow(True)
    ax.legend(loc='upper left', frameon=False, ncol=1)
    ax.text(1.0, -0.17, '* As of 12 October 2026', transform=ax.transAxes, ha='right', fontsize=8.5, style='italic', color=MUTED)
    save(fig, 2)

def fig3():
    FY = R['family_year']; yrs = [2022, 2023, 2024, 2025, 2026]
    # (legend label, model-family keys as stored in results.json)
    groups = [('YOLOv8', ['YOLOv8']), ('YOLO11', ['YOLO11']), ('YOLOv5', ['YOLOv5']), ('YOLOv7', ['YOLOv7']), ('Other YOLO versions', ['YOLO (diğer)', 'YOLOv10', 'YOLOv12', 'YOLOv9', 'YOLO26']),
              ('RT-DETR / DETR', ['RT-DETR', 'DETR ailesi']), ('Ensemble', ['Topluluk (ensemble)'])]
    used = {n for _, ns in groups for n in ns}; groups.append(('Other', [f for f in FY if f not in used]))
    fig, ax = plt.subplots(figsize=(6.3, 2.85)); bottom = [0] * 5
    for (lab, names), c in zip(groups, CAT):
        v = [sum(FY.get(n, {}).get(str(y), 0) for n in names) for y in yrs]
        ax.bar(range(5), v, 0.58, bottom=bottom, color=c, label=f'{lab} ({sum(v)})', edgecolor='white', linewidth=0.6)
        bottom = [b + q for b, q in zip(bottom, v)]
    for i, t in enumerate(bottom): ax.text(i, t + 1.5, str(t), ha='center', va='bottom', fontsize=9, color=INK)
    ax.set_xticks(range(5)); ax.set_xticklabels([str(y) + ('*' if y == 2026 else '') for y in yrs])
    ax.set_ylabel('Number of studies'); ax.yaxis.grid(True, color=GRID, lw=0.5); ax.set_axisbelow(True)
    ax.legend(loc='upper left', frameon=False, ncol=2); ax.set_ylim(0, max(bottom) * 1.55)
    ax.text(1.0, -0.17, '* As of 12 October 2026', transform=ax.transAxes, ha='right', fontsize=8.5, style='italic', color=MUTED)
    save(fig, 3)

# own-split mAP@0.5 results of groups (ii) and (iii): (value, class set, test definition)
# test definition codes: 'separate' = separate test split, 'validation' = validation set reported as test, 'unclear' = test definition unclear
II = [(70.6, '4', 'validation'), (67.8, '4', 'separate'), (71.5, '5', 'separate'), (65.3, '4', 'separate'), (65.7, '4', 'separate')]
III = [(90.7, '5', 'separate'), (91.4, '5', 'separate'), (86.0, '5', 'separate'), (86.0, '4', 'separate'), (77.4, '5', 'separate'), (75.7, '6', 'separate'), (67.6, '4', 'validation'), (86.6, '4', 'unclear'), (51.7, '4', 'separate'), (79.1, '4', 'separate'),
       (85.8, '5', 'separate')]   # RSF-DETR; CrackLite-Net (unthresholded mAP, cross-dataset test) is not plotted
assert sorted(v for v, _, _ in II) == sorted(v for _, v, _ in R['values']['ii']) and sorted(v for v, _, _ in III) == sorted(v for _, v, _ in R['values']['iii'])
OFFICIAL = [('YOLOv8x\n(baseline)', 0.668), ('RDD-YOLO', 0.696), ('CRDDC’2022 3rd', 0.741), ('CRDDC’2022 2nd', 0.743), ('CRDDC’2022 1st', 0.770), ('StripRFNet', 0.803)]

def fig4():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.3, 3.3), gridspec_kw={'width_ratios': [1.1, 1.0], 'wspace': 0.5})
    for i, (vals, c) in enumerate([(II, CAT[0]), (III, CAT[1])]):
        for j, (v, cl, td) in enumerate(sorted(vals)):
            xp = i + ((j % 5) - 2) * 0.075
            a.scatter([xp], [v], s=26, marker='o' if cl == '4' else '^', facecolor=c if td == 'separate' else 'white', edgecolor=c if td != 'separate' else 'white', linewidth=1.0 if td != 'separate' else 0.5, zorder=3)
        a.hlines(st.median(v for v, _, _ in vals), i - 0.27, i + 0.27, color=INK, lw=1.3, zorder=4)
        a.text(i + 0.3, st.median(v for v, _, _ in vals), EN(st.median(v for v, _, _ in vals)) + '%', va='center', fontsize=9, color=INK)
    a.scatter([0.18], [93.5], s=20, marker='x', color=MUTED, zorder=3, linewidth=1)
    a.annotate('test split undefined', (0.18, 93.5), xytext=(-0.43, 97.3), fontsize=8.5, color=MUTED, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.5))
    a.set_xticks([0, 1]); a.set_xticklabels([f'(ii) Multi-country\n({len(II)} results)', f'(iii) China\n({len(III)} results)'])
    a.set_xlim(-0.5, 1.8); a.set_ylim(45, 100); a.set_ylabel('Reported mAP@0.5 (%)')
    a.yaxis.grid(True, color=GRID, lw=0.5); a.set_axisbelow(True); a.set_title('(a) Results reported on their own splits', loc='left')
    hs = [Line2D([], [], marker='o', ls='', color=MUTED, ms=5, label='4 official classes'), Line2D([], [], marker='^', ls='', color=MUTED, ms=5, label='5 or 6 classes'),
          Line2D([], [], marker='o', ls='', mfc='white', mec=MUTED, ms=5, label='Validation reported as test\nor test unclear'), Line2D([], [], color=INK, lw=1.3, label='Median')]
    a.legend(handles=hs, loc='upper center', bbox_to_anchor=(0.5, -0.2), frameon=False, ncol=2, fontsize=8.5, columnspacing=1.0, handletextpad=0.4)
    labs = [l for l, _ in OFFICIAL]; vals = [v for _, v in OFFICIAL]
    b.barh(range(len(vals)), vals, color=BLUE, height=0.62)
    for i, v in enumerate(vals): b.text(v + 0.004, i, f'{v:.3f}', va='center', fontsize=9, color=INK)
    b.set_yticks(range(len(vals))); b.set_yticklabels(labs, fontsize=9)
    b.set_xlim(0.6, 0.86); b.set_xticks([0.6, 0.7, 0.8]); b.set_xticklabels(['0.6', '0.7', '0.8']); b.set_xlabel('F1 (IoU > 0.5)')
    b.xaxis.grid(True, color=GRID, lw=0.5); b.set_axisbelow(True); b.set_title('(b) CRDDC’2022 official hidden test', loc='right')
    save(fig, 4)

LABEL = {'P016': 'RDD-YOLO', 'P334': 'StripRFNet', 'P002': 'YOLOv8-PD', 'P011': 'YOLOv8-CD', 'P019': 'Impr. YOLOv5s', 'P033': 'Impr. YOLOv8n', 'P161': 'RS-YOLOv11n', 'P260': 'YOLO_SE6',
         'P000': 'BL-YOLOv8', 'P010': 'Impr. YOLOv8s (a)', 'P026': 'Impr. YOLOv8s (b)', 'P035': 'OBC-YOLOv8', 'P046': 'YOLO-ROC', 'P075': 'YOLOv11s-ATL', 'P106': 'ALC-Net', 'P401': 'ELW-YOLO', 'P003': 'UAV study', 'P027': 'Federated learning',
         'P234': 'CrackLite-Net', 'P235': 'RSF-DETR', 'P440': 'YOLO-MCG'}

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
    cb.set_label('Number of shared dimensions\n(subset, class set, test definition)', fontsize=8.5); cb.ax.xaxis.set_label_position('top')
    save(fig, 5)

def fig6():
    # PRCI criteria C1-C8 (stored as K1-K8 in results.json)
    NAMES = {'K1': 'Country subset', 'K2': 'Data split', 'K3': 'Damage classes', 'K4': 'Metric and IoU', 'K5': 'Seed/repeated runs', 'K6': 'Hardware and settings', 'K7': 'Code or weights', 'K8': 'Test protocol'}
    C = R['prti_crit']; N = len(R['prti_rows'])
    items = sorted(C.items(), key=lambda kv: (kv[1], kv[0]), reverse=False)
    fig, ax = plt.subplots(figsize=(6.15, 2.8))   # 6.15 in keeps the '20/21 (95%)' labels inside the fixed canvas
    ax.barh(range(len(items)), [v / N * 100 for _, v in items], color=BLUE, height=0.62)
    for i, (k, v) in enumerate(items): ax.text(v / N * 100 + 1.2, i, f"{v}/{N} ({EN(round(v / N * 100))}%)", va='center', fontsize=9, color=INK)
    ax.set_yticks(range(len(items))); ax.set_yticklabels([NAMES[k] for k, _ in items])
    ax.set_xlim(0, 118); ax.set_xticks([0, 25, 50, 75, 100]); ax.set_xlabel('Studies meeting the criterion (%)')
    ax.xaxis.grid(True, color=GRID, lw=0.5); ax.set_axisbelow(True)
    save(fig, 6)

fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); print('ok')
