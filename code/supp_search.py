"""Logged supplementary search for RDD2022 studies (PRISMA 2020 'other methods' arm).

Runs fixed queries against public scholarly APIs, stores every raw response and writes
one row per query (source, query, date, hits, retrieved) plus a de-duplicated candidate list.
Usage: python3 supp_search.py OUT_DIR
"""
import json, os, re, subprocess, sys, time, urllib.parse, xml.etree.ElementTree as ET

OUT = sys.argv[1]
RAW = os.path.join(OUT, 'search_raw')
os.makedirs(RAW, exist_ok=True)
DATE_FROM, DATE_TO = '2022-01-01', '2026-10-12'   # same cut-off as the OpenAlex arm
TERMS = ['RDD2022', '"RDD 2022"', 'CRDDC2022', 'CRDDC']
slug = lambda t: re.sub(r'[^A-Za-z0-9]', '_', t).strip('_') + ('_phrase' if t.startswith('"') else '')
UA = 'RDD2022-analysis/1.0 (academic literature search)'


def get(url, name, tries=6):
    """Download url with curl and keep the raw body on disk."""
    path = os.path.join(RAW, name)
    for t in range(tries):
        body = subprocess.run(['curl', '-sL', '-m', '90', '-A', UA, url], capture_output=True).stdout
        throttled = b'Too Many Requests' in body[:200] or b'"code": "429"' in body[:300]
        if body and not throttled and not body.lstrip().startswith((b'<html', b'<!DOCTYPE')):
            open(path, 'wb').write(body)
            return body
        time.sleep(45 * (t + 1))
    open(path, 'wb').write(body or b'')
    return body or b''


log, cands = [], []
def add(source, query, title, year, doi, url, abstract=''):
    cands.append(dict(source=source, query=query, title=title or '', year=year, doi=(doi or '').lower().replace('https://doi.org/', '') or None,
                      url=url, abstract=abstract or ''))


def crossref(term):
    q = term.strip('"')
    n, cursor, hits, page = 0, '*', None, 0
    while True:
        url = 'https://api.crossref.org/works?' + urllib.parse.urlencode({
            'query.bibliographic': q, 'rows': 200, 'cursor': cursor,
            'filter': f'from-pub-date:{DATE_FROM},until-pub-date:{DATE_TO}',
            'select': 'DOI,title,issued,abstract,URL,type', 'mailto': 'research@example.org'})
        body = get(url, f'crossref_{slug(term)}_{page}.json')
        d = json.loads(body)['message']
        hits = d['total-results']
        items = d['items']
        for it in items:
            title = (it.get('title') or [''])[0]
            text = title + ' ' + (it.get('abstract') or '')
            # Crossref ranks fuzzily: keep only records that really contain the term
            if re.search(re.escape(q).replace(r'\ ', r'[\s-]?'), text, re.I):
                y = ((it.get('issued') or {}).get('date-parts') or [[None]])[0][0]
                add('Crossref', term, title, y, it.get('DOI'), it.get('URL'), re.sub(r'<[^>]+>', ' ', it.get('abstract') or ''))
                n += 1
        page += 1
        cursor = d.get('next-cursor')
        # the first pages are the relevant ones; stop when a page no longer contains the term
        if not items or page >= 3 or not cursor:
            break
    log.append(dict(source='Crossref', query=term, field='title, abstract and bibliographic metadata (query.bibliographic)', date_filter=f'{DATE_FROM}..{DATE_TO}',
                    api_total=hits, kept=n, note='Because Crossref uses fuzzy ranking, only records with the term in the title or abstract were retained (first 3 pages).'))


def arxiv(term):
    q = term.strip('"')
    sq = f'all:"{q}"'
    url = 'http://export.arxiv.org/api/query?' + urllib.parse.urlencode({'search_query': sq, 'start': 0, 'max_results': 500})
    body = get(url, f'arxiv_{slug(term)}.xml')
    ns = {'a': 'http://www.w3.org/2005/Atom', 'x': 'http://a9.com/-/spec/opensearch/1.1/', 'ar': 'http://arxiv.org/schemas/atom'}
    root = ET.fromstring(body)
    n = 0
    for e in root.findall('a:entry', ns):
        y = int(e.find('a:published', ns).text[:4])
        if not 2022 <= y <= 2026 or e.find('a:published', ns).text[:10] > DATE_TO:
            continue
        doi = e.find('ar:doi', ns)
        add('arXiv', term, ' '.join(e.find('a:title', ns).text.split()), y, doi.text if doi is not None else None,
            e.find('a:id', ns).text, ' '.join(e.find('a:summary', ns).text.split()))
        n += 1
    log.append(dict(source='arXiv', query=term, field='all fields (all:)', date_filter=f'{DATE_FROM}..{DATE_TO}',
                    api_total=int(root.find('x:totalResults', ns).text), kept=n, note=''))
    time.sleep(3)


def semantic(term):
    q = term
    n, token, page, hits = 0, None, 0, None
    while True:
        params = {'query': q, 'fields': 'title,year,externalIds,abstract,url,publicationDate', 'year': '2022-2026'}
        if token:
            params['token'] = token
        url = 'https://api.semanticscholar.org/graph/v1/paper/search/bulk?' + urllib.parse.urlencode(params)
        body = get(url, f'semanticscholar_{slug(term)}_{page}.json')
        d = json.loads(body)
        hits = d.get('total', hits)
        for it in d.get('data') or []:
            if (it.get('publicationDate') or '9') > DATE_TO:
                continue
            add('Semantic Scholar', term, it.get('title'), it.get('year'), (it.get('externalIds') or {}).get('DOI'), it.get('url'), it.get('abstract'))
            n += 1
        token = d.get('token')
        page += 1
        if not token or page >= 10:
            break
        time.sleep(35)
    log.append(dict(source='Semantic Scholar', query=term, field='title and abstract (search/bulk)', date_filter=f'2022-2026, publication date ≤ {DATE_TO}',
                    api_total=hits, kept=n, note=''))
    time.sleep(35)


def europepmc(term):
    n, cursor, hits, page = 0, '*', None, 0
    q = f'{term} AND FIRST_PDATE:[{DATE_FROM} TO {DATE_TO}]'
    while True:
        url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?' + urllib.parse.urlencode(
            {'query': q, 'format': 'json', 'pageSize': 200, 'cursorMark': cursor, 'resultType': 'core'})
        body = get(url, f'europepmc_{slug(term)}_{page}.json')
        d = json.loads(body)
        hits = d['hitCount']
        for it in d['resultList']['result']:
            add('Europe PMC', term, it.get('title'), int(it['pubYear']) if it.get('pubYear') else None, it.get('doi'),
                f"https://europepmc.org/article/{it.get('source')}/{it.get('id')}", re.sub(r'<[^>]+>', ' ', it.get('abstractText') or ''))
            n += 1
        next_c = d.get('nextCursorMark')
        page += 1
        if not next_c or next_c == cursor or n >= hits or page > 20:
            break
        cursor = next_c
        time.sleep(1)
    log.append(dict(source='Europe PMC', query=term, field='full text and bibliographic metadata', date_filter=f'{DATE_FROM}..{DATE_TO}', api_total=hits, kept=n, note=''))


def dblp(term):
    q = term.strip('"')
    url = 'https://dblp.org/search/publ/api?' + urllib.parse.urlencode({'q': q, 'format': 'json', 'h': 1000})
    d = json.loads(get(url, f'dblp_{slug(term)}.json'))['result']['hits']
    n = 0
    for h in d.get('hit', []):
        i = h['info']
        y = int(i.get('year', 0))
        if 2022 <= y <= 2026:
            add('DBLP', term, i.get('title'), y, i.get('doi'), i.get('ee') if isinstance(i.get('ee'), str) else None)
            n += 1
    log.append(dict(source='DBLP', query=term, field='title', date_filter='2022-2026', api_total=int(d['@total']), kept=n, note=''))
    time.sleep(3)


for term in TERMS:
    for fn in (crossref, arxiv, semantic, europepmc, dblp):
        try:
            fn(term)
        except Exception as e:  # keep the failure in the log instead of hiding it
            log.append(dict(source=fn.__name__, query=term, field='', date_filter='', api_total=None, kept=0, note=f'ERROR: {type(e).__name__}: {e}'))
        print(log[-1]['source'], term, log[-1]['api_total'], log[-1]['kept'], log[-1]['note'][:70], flush=True)

json.dump(log, open(os.path.join(OUT, 'search_log.json'), 'w'), ensure_ascii=False, indent=1)
json.dump(cands, open(os.path.join(OUT, 'search_hits.json'), 'w'), ensure_ascii=False)
print('hits', len(cands))
