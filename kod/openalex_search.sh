#!/bin/sh
# OpenAlex queries of the main search arm (run on 12 October 2026). Running the script writes responses to oa/; the 12 October responses were not kept (see BENIOKU.md).
mkdir -p oa
fetch() { # $1 name, $2 filter
  cursor="*"; i=0
  while [ -n "$cursor" ] && [ "$cursor" != "null" ]; do
    curl -s "https://api.openalex.org/works?filter=$2&select=id,display_name,publication_year,cited_by_count,doi,primary_location,type,authorships&per-page=200&cursor=$cursor&mailto=research@example.org" > "oa/$1_$i.json"
    cursor=$(python3 -c "import json;d=json.load(open('oa/$1_$i.json'));print(d['meta'].get('next_cursor') or '')")
    i=$((i+1)); [ $i -gt 10 ] && break
  done
  echo "$1 pages=$i"
}
fetch cites_gdj "cites:W4400098420"
fetch cites_arxiv "cites:W4296544680"
fetch cites_fig "cites:W4394415098"
fetch ft_rdd2022 "fulltext.search:RDD2022"
fetch ft_rdd_2022 "fulltext.search:%22RDD%202022%22"
fetch ab_rdd2022 "title_and_abstract.search:RDD2022"
