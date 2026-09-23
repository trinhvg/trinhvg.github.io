from pathlib import Path
import json, html, re
root=Path(__file__).parent
content=json.loads((root/'content.json').read_text())
e=html.escape

def link(url,label,css=''):
    return f'<a class="{css}" href="{e(url,quote=True)}">{e(label)}</a>'
news=[]
for n in content['news']:
    extra=' '+link(n['url'], n['label']) if n.get('url') else ''
    news.append(f'<li><time>{e(n["date"])}</time><div>{e(n["text"])}{extra}</div></li>')
pubs={"journal":[], "conference":[], "preprint":[]}
for p in content['publications']:
    authors=e(p['authors'])
    for name in ['Trinh Thi Le Vuong','Trinh T. L. Vuong','Thi Le Trinh Vuong','Trinh Vuong']:
        authors=authors.replace(name,f'<strong>{name}</strong>')
    badge=f'<span class="status">{e(p["status"])}</span>' if p.get('status') else ''
    links=''.join(link(u,k,'paper-link') for k,u in p['links'].items())
    pubs[p['type']].append(f'''<article class="publication"><div class="pub-year">{p['year']}</div><div class="pub-body"><div class="venue">{e(p['venue'])}{badge}</div><h3>{link(next(iter(p['links'].values())),p['title'])}</h3><p class="authors">{authors}</p><p class="description">{e(p['description'])}</p><div class="paper-links">{links}</div></div></article>''')
template=(root/'template.html').read_text()
for key,value in {'NEWS':'\n'.join(news),'JOURNALS':'\n'.join(pubs['journal']),'CONFERENCES':'\n'.join(pubs['conference']),'PREPRINTS':'\n'.join(pubs['preprint']),'JOURNAL_COUNT':str(len(pubs['journal'])),'CONFERENCE_COUNT':str(len(pubs['conference'])),'PREPRINT_COUNT':str(len(pubs['preprint'])),'UPDATED':e(content['updated'])}.items():
    template=template.replace('{{'+key+'}}',value)
(root/'docs'/'index.html').write_text(template)
print(f'Built index.html: {len(news)} news items, {sum(map(len,pubs.values()))} publications')
