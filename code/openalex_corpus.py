"""Merges the responses of openalex_search.sh into the screening set (12 October 2026): 572 unique records, abstracts fetched
from abstract_inverted_index, keyword and record-type filters, 554 records. Reads oa/*.json, writes corpus.json."""
import collections, glob, json, re, subprocess, time

seen, src = {}, collections.defaultdict(set)
for f in sorted(glob.glob('oa/*.json')):
    d = json.load(open(f)); tag = f.split('/')[1].rsplit('_', 1)[0]
    for w in d.get('results', []):
        seen[w['id']] = w; src[w['id']].add(tag)
rows = []
for k, w in seen.items():
    venue = ((w.get('primary_location') or {}).get('source') or {}) or {}
    rows.append(dict(oa=k.split('/')[-1], title=w['display_name'], year=w['publication_year'], cites=w['cited_by_count'], doi=w['doi'], venue=venue.get('display_name'), type=w['type'], src=sorted(src[k]),
                     authors=[a['author']['display_name'] for a in w.get('authorships', [])][:4]))
print('unique', len(rows))

def inv(ii):
    return ' '.join(w for p, w in sorted((p, w) for w, ps in ii.items() for p in ps)) if ii else ''
ids = [r['oa'] for r in rows]; abs_ = {}
for i in range(0, len(ids), 50):
    url = 'https://api.openalex.org/works?filter=openalex:' + '|'.join(ids[i:i + 50]) + '&select=id,abstract_inverted_index,primary_location&per-page=50'
    d = None
    for _ in range(3):
        try:
            d = json.loads(subprocess.run(['curl', '-s', url], capture_output=True, text=True, timeout=90).stdout); break
        except Exception:
            time.sleep(2)
    for w in (d or {}).get('results', []):
        pl = w.get('primary_location') or {}
        abs_[w['id'].split('/')[-1]] = dict(abstract=inv(w.get('abstract_inverted_index')), landing=pl.get('landing_page_url'))
for r in rows:
    a = abs_.get(r['oa'], {}); r['abstract'] = a.get('abstract', ''); r['landing'] = a.get('landing')

# records that came only from the full-text queries must mention road damage in the title or abstract
kw = re.compile(r'road|pavement|crack|pothole|asphalt|highway|street|distress|rutting|yol|jalan|đường|дорог', re.I)
keep = [r for r in rows if any(s.startswith(('cites', 'ab_')) for s in r['src']) or kw.search((r['title'] or '') + ' ' + (r['abstract'] or ''))]
print('keep', len(keep), 'drop', len(rows) - len(keep))
keep = [r for r in keep if r['type'] not in ('erratum', 'paratext')]
keep.sort(key=lambda r: -(r['cites'] or 0))
for i, r in enumerate(keep): r['pid'] = 'P%03d' % i
json.dump(keep, open('corpus.json', 'w'), ensure_ascii=False, indent=1)
print('corpus', len(keep))
