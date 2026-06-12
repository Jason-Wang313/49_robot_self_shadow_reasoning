import requests, csv, time, sys
from urllib.parse import quote
queries = [
    'robot vision shadow', 'robot self shadow', 'shadow detection robot vision',
    'self shadowing robotics', 'reflection robot perception', 'robot proprioception vision',
    'embodied visual self model robotics', 'occlusion reasoning robot vision',
    'shadow removal computer vision', 'cast shadow reasoning robotics',
    'robot self localization shadow', 'mobile robot shadow environment'
]
seen = {}
rows = []
headers = {'User-Agent':'Mozilla/5.0'}
for q in queries:
    for offset in range(0, 200, 20):
        url = f'https://api.crossref.org/works?query={quote(q)}&rows=20&offset={offset}'
        try:
            r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()
            items = r.json()['message']['items']
        except Exception as e:
            print('ERR', q, offset, e)
            break
        if not items:
            break
        for it in items:
            doi = it.get('DOI','')
            key = doi.lower() if doi else (it.get('title',[None])[0] or '').lower()
            if not key or key in seen:
                continue
            seen[key] = True
            title = (it.get('title') or [''])[0]
            year = None
            for fld in ('published-print','published-online','created','issued'):
                parts = it.get(fld,{}).get('date-parts') or []
                if parts and parts[0]:
                    year = parts[0][0]
                    break
            venue = (it.get('container-title') or [''])[0]
            rows.append({'query':q,'title':title,'year':year or '', 'venue':venue, 'doi':doi, 'type':it.get('type','')})
        if len(rows) >= 1200:
            break
    if len(rows) >= 1200:
        break
print('rows', len(rows))
import os
os.makedirs('docs', exist_ok=True)
with open('docs/related_work_matrix.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['query','title','year','venue','doi','type'])
    w.writeheader(); w.writerows(rows)