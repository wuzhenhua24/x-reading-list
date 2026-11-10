import re, json
STR = r'"((?:[^"\\]|\\.)*)"'
def s(x): return json.loads('"'+x+'"')
def parse(fn):
    t = open(fn, encoding='utf-8').read()
    body = t[t.index('<Page'):]
    title = s(re.search(r'title=' + STR, body).group(1))
    summary = s(re.search(r'summary=' + STR, body).group(1))
    # split into pre-section and sections
    first = body.find('<Section')
    pre = body[:first]
    notes = re.findall(r'<Text>(.*?)</Text>', pre, re.S)
    sections = []
    for m in re.finditer(r'<Section heading=' + STR + r'>(.*?)</Section>', body, re.S):
        heading = s(m.group(1)); inner = m.group(2)
        blocks = []
        for b in re.finditer(r'<Text>(.*?)</Text>|<Callout>(.*?)</Callout>|<LinkCards(.*?)/>|<(NumberedList|BulletList)(.*?)/>', inner, re.S):
            if b.group(1) is not None: blocks.append({'type':'text','text':b.group(1).strip()})
            elif b.group(2) is not None: blocks.append({'type':'callout','text':b.group(2).strip()})
            elif b.group(3) is not None:
                links = []
                for o in re.finditer(r'\{([^{}]*?)\}', b.group(3)):
                    d = {k: s(v) for k, v in re.findall(r'(\w+):\s*' + STR, o.group(1))}
                    if 'href' in d: links.append(d)
                blocks.append({'type':'links','numbered': 'numbered' in b.group(3).split('links=')[0],'links':links})
            else:
                items = [s(x) for x in re.findall(STR, b.group(5))]
                blocks.append({'type':'ol' if b.group(4)=='NumberedList' else 'ul','items':items})
        hm = re.match(r'(.*?)\s+@(\w+)$', heading)
        sections.append({'heading':heading,'name':hm.group(1) if hm else None,'handle':hm.group(2) if hm else None,'blocks':blocks})
    return {'title':title,'summary':summary,'notes':notes,'sections':sections}
cats = [('business','src-business.txt'),('thinking','src-thinking.txt'),('ai','src-ai.txt'),('humanities','src-humanities.txt'),('education','src-education.txt'),('thariq','src-thariq.txt')]
data = {k: parse(f) for k,f in cats}
json.dump(data, open('data.json','w'), ensure_ascii=False, indent=1)
for k,v in data.items():
    print(k, v['title'], len(v['notes']), [ (x['heading'], sum(len(b.get('links',[])) for b in x['blocks'])) for x in v['sections']])
