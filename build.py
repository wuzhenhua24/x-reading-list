import json, html, os, re, shutil
d = json.load(open('data.json'))
OUT = 'dist'
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
e = lambda x: html.escape(x, quote=True)
CATS = [
 ('business','创业、产品与商业','产品、增长、小而赚钱的公司，以及 AI 怎样冲击软件生意。'),
 ('thinking','思维方式、投资与写作','心智模型、长期主义、金钱心理与写作。'),
 ('ai','AI 与 Agent','一线的 AI 编程、agent 产品和组织经验。'),
 ('humanities','人文','注意力、写作、养育、审美与社会心理。'),
 ('education','教育与儿童成长','幼儿认知、养育、屏幕与学校、阅读。'),
]
FEATURE = ('thariq','专题：Thariq (@trq212)','Claude Code 团队前成员 Thariq 2026 年 1 月至 11 月的长文与短帖，按主题整理。')
SHORT = {k:t for k,t,_ in CATS}; SHORT['thariq'] = 'Thariq 专题'
NAVSHORT = {'business':'创业商业','thinking':'思维投资','ai':'AI 与 Agent','humanities':'人文','education':'教育','thariq':'Thariq 专题'}
NUM = {k:'%02d'%(i+1) for i,(k,_,_) in enumerate(CATS)}
NOTE = '收藏数为 2026-11-02 抓取时的数据，之后会变化；人物简介中标 * 的内容来自公开常识，未在帖子或账号简介中核实。所有链接指向 x.com 原帖。'
ORDER = [c[0] for c in CATS] + ['thariq']

ICON_EXT = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3h7v7M13 3 6.5 9.5M11 9.5V13H3V5h3.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_BM = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2.5h8v11l-4-3-4 3z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>'
ICON_EYE = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M1.5 8S4 3.5 8 3.5 14.5 8 14.5 8 12 12.5 8 12.5 1.5 8 1.5 8z" fill="none" stroke="currentColor" stroke-width="1.4"/><circle cx="8" cy="8" r="2" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'
ICON_SEARCH = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="4.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="m10.5 10.5 3.5 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
ICON_ARROW = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
FAVICON = "data:image/svg+xml," + "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%231c1a17'/%3E%3Ctext x='16' y='22' font-size='17' text-anchor='middle' fill='%23f6f1e7' font-family='serif'%3E读%3C/text%3E%3C/svg%3E"

def slug(h): return h.lower()
def initials(name):
    w = name.split()
    if len(w) >= 2: return (w[0][0] + w[1][0]).upper()
    if name.isupper(): return name[:3]
    return name[0].upper()
def avatar(name, cat, cls='av'):
    return f'<span class="{cls} c-{cat}" aria-hidden="true">{e(initials(name))}</span>'
def star(text):
    # keep the * markers, just style them
    return e(text).replace('*', '<sup class="ast" title="来自公开常识，未核实">*</sup>')

def layout(title, body, active, desc='', cat=None):
    nav = ''.join(f'<a href="/{k}" class="c-{k}{" on" if k==active else ""}"{" aria-current=page" if k==active else ""}><i></i>{e(NAVSHORT[k])}</a>' for k in ORDER)
    nav += f'<a href="/people" class="c-people{" on" if active=="people" else ""}"{" aria-current=page" if active=="people" else ""}>人物索引</a>'
    bcls = f' class="c-{cat}"' if cat else ''
    return f'''<!doctype html>
<html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc or title)}">
<meta name="color-scheme" content="light dark"><link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="/style.css"></head>
<body{bcls}><a class="skip" href="#main">跳到正文</a>
<header class="top"><div class="wrap bar"><a class="brand" href="/"><span class="mark">读</span><span>X 上值得关注的人</span></a><nav class="nav" aria-label="主导航">{nav}</nav></div></header>
<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap"><div class="fbrand"><span class="mark">读</span> X 上值得关注的人</div>
<p>{e(NOTE)}</p><p>精选导读，仅摘要与链接，原文版权归作者所有。</p>
<nav class="fnav" aria-label="页脚导航">{''.join(f'<a href="/{k}">{e(SHORT[k])}</a>' for k in ORDER)}<a href="/people">人物索引</a></nav></div></footer>
<script src="/site.js" defer></script>
</body></html>'''

def parse_site(site):
    kind, metric = '', ''
    for part in [x.strip() for x in site.split('·')]:
        if '收藏' in part or '浏览' in part: metric = part
        elif part: kind = part
    return kind, metric

def render_links(b):
    tag = 'ol' if b.get('numbered') else 'ul'
    out = [f'<{tag} class="posts{" num" if tag=="ol" else ""}">']
    for l in b['links']:
        kind, metric = parse_site(l.get('site',''))
        meta = []
        if l.get('date'): meta.append(f'<time datetime="{e(l["date"])}">{e(l["date"])}</time>')
        if kind: meta.append(f'<span class="kind{" long" if kind!="X 帖子" else ""}">{e(kind)}</span>')
        if metric: meta.append(f'<span class="met">{ICON_EYE if "浏览" in metric else ICON_BM}{e(metric)}</span>')
        out.append(f'<li><a href="{e(l["href"])}" target="_blank" rel="noopener noreferrer"><span class="pt">{e(l["title"])}</span><span class="pm">{"".join(meta)}</span>{ICON_EXT}</a></li>')
    out.append(f'</{tag}>'); return '\n'.join(out)

def render_blocks(blocks, quote=False):
    out = []
    for b in blocks:
        if b['type']=='text': out.append(f'<p class="intro">{star(b["text"])}</p>')
        elif b['type']=='callout': out.append(f'<blockquote class="pull"><p>{e(b["text"])}</p></blockquote>')
        elif b['type']=='links': out.append(render_links(b))
        else:
            t = b['type']; out.append(f'<{t} class="list">' + ''.join(f'<li>{e(i)}</li>' for i in b['items']) + f'</{t}>')
    return '\n'.join(out)

def count_people(k): return sum(1 for s in d[k]['sections'] if s['handle'])
def count_posts(k): return sum(len(b['links']) for s in d[k]['sections'] for b in s['blocks'] if b['type']=='links')

# first pass: people membership (so category pages can show cross-links)
people = {}
for k in ORDER:
    for s in d[k]['sections']:
        if s['handle']:
            sid = slug(s['handle'])
            info = people.setdefault(sid, {'name': s['name'], 'handle': s['handle'], 'cats': [], 'intro': ''})
            info['cats'].append(k)
            if not info['intro']:
                info['intro'] = next((b['text'] for b in s['blocks'] if b['type']=='text'), '')
people.setdefault('trq212', {'name':'Thariq','handle':'trq212','cats':['thariq'],'intro': d['thariq']['summary']})

def page(key):
    p = d[key]
    is_people = key != 'thariq'
    toc, secs = [], []
    n = 0
    for s in p['sections']:
        if s['handle']:
            sid = slug(s['handle']); n += 1
            nposts = sum(len(b['links']) for b in s['blocks'] if b['type']=='links')
            toc.append(f'<li data-name="{e((s["name"]+" "+s["handle"]).lower())}"><a href="#{sid}">{avatar(s["name"], key, "av xs")}<span>{e(s["name"])}</span><em>{nposts}</em></a></li>')
            others = [c for c in people[sid]['cats'] if c != key]
            also = ''.join(f'<a class="chip c-{c}" href="/{c}#{sid}">也见于 · {e(SHORT[c])}</a>' for c in others)
            head = f'''<header class="phead">{avatar(s["name"], key, "av lg")}<div><h2>{e(s["name"])}</h2>
<p class="hmeta"><a class="handle" href="https://x.com/{e(s["handle"])}" target="_blank" rel="noopener noreferrer">@{e(s["handle"])}</a><span class="dot">·</span><span>{nposts} 条精选</span></p>{f'<p class="also">{also}</p>' if also else ''}</div><span class="idx">{n:02d}</span></header>'''
            secs.append(f'<section id="{sid}" class="person" data-name="{e((s["name"]+" "+s["handle"]).lower())}">{head}\n{render_blocks(s["blocks"])}</section>')
        else:
            sid = 'theme' if s['heading']=='共同的主线' else 'sec-%d' % len(secs)
            if s['heading'] == '共同的主线':
                toc.append(f'<li class="tl-theme"><a href="#{sid}"><span class="qm">“</span><span>{e(s["heading"])}</span></a></li>')
                items = ''.join(f'<li>{e(i)}</li>' for b in s['blocks'] for i in b.get('items',[]))
                secs.append(f'<section id="{sid}" class="threads"><p class="kick">读完之后</p><h2>{e(s["heading"])}</h2><ol class="tlist">{items}</ol></section>')
            elif any(b['type']=='callout' for b in s['blocks']):
                toc.append(f'<li class="tl-theme"><a href="#{sid}"><span class="qm">“</span><span>{e(s["heading"])}</span></a></li>')
                secs.append(f'<section id="{sid}" class="threads"><p class="kick">总结</p><h2>{e(s["heading"])}</h2>{render_blocks(s["blocks"])}</section>')
            else:
                n += 1
                nposts = sum(len(b['links']) for b in s['blocks'] if b['type']=='links')
                toc.append(f'<li><a href="#{sid}"><b class="tn">{n:02d}</b><span>{e(s["heading"])}</span><em>{nposts}</em></a></li>')
                secs.append(f'<section id="{sid}" class="person theme"><header class="phead"><div><h2>{e(s["heading"])}</h2><p class="hmeta"><span>{nposts} 条</span></p></div><span class="idx">{n:02d}</span></header>\n{render_blocks(s["blocks"])}</section>')
    notes = ''.join(f'<p>{e(nn)}</p>' for nn in p['notes'])
    disp = p['title'].split('：',1)[1] if '：' in p['title'] else p['title']
    kicker = f'清单 {NUM[key]}' if key in NUM else '专题'
    filt = f'<label class="filter">{ICON_SEARCH}<input type="search" placeholder="筛选人名…" aria-label="按人名筛选" data-target="section.person" data-toc=".toc li[data-name]"></label>' if is_people else ''
    tochead = f'本页 {count_people(key)} 人' if is_people else f'本页 {n} 个主题'
    toclist = f'<ol class="toc">{"".join(toc)}</ol>'
    stats = f'<span><b>{count_people(key)}</b> 人</span>' if is_people else ''
    stats += f'<span><b>{count_posts(key)}</b> 条精选</span><span>数据截至 <b>2026-11-02</b></span>'
    body = f'''<section class="phero"><div class="wrap"><a class="crumb" href="/">首页</a><span class="crumb-sep">/</span><span class="kick">{kicker}</span>
<h1>{e(disp)}</h1><p class="lede">{e(p["summary"])}</p><p class="stats">{stats}</p>{f'<div class="pnote">{notes}</div>' if notes else ''}</div></section>
<div class="wrap cols">
<aside class="side" aria-label="本页目录"><div class="sticky"><p class="sidehead">{tochead}</p>{filt}<nav>{toclist}</nav></div></aside>
<details class="mtoc"><summary>{tochead} · 目录</summary>{toclist}</details>
<div class="content">{f'<div class="mfilter">{filt}</div>' if is_people else ''}
{''.join(secs)}
<p class="empty" hidden>没有匹配的人。</p>
<nav class="pager">{pager(key)}</nav>
</div></div>'''
    open(f'{OUT}/{key}.html','w').write(layout(p['title'], body, key, p['summary'], key))

def pager(key):
    i = ORDER.index(key); out = ''
    if i > 0:
        k = ORDER[i-1]; out += f'<a class="prev c-{k}" href="/{k}"><small>上一份</small><span>{e(SHORT[k])}</span></a>'
    else: out += '<span></span>'
    if i < len(ORDER)-1:
        k = ORDER[i+1]; out += f'<a class="next c-{k}" href="/{k}"><small>下一份</small><span>{e(SHORT[k])}</span></a>'
    else: out += f'<a class="next c-people" href="/people"><small>继续</small><span>人物索引</span></a>'
    return out

for k in ORDER: page(k)

total_posts = sum(count_posts(k) for k in d)
cards = []
for k,t,desc in CATS:
    names = [s['name'] for s in d[k]['sections'] if s['handle']]
    avs = ''.join(avatar(nm, k, 'av sm') for nm in names[:6]) + (f'<span class="av sm more">+{len(names)-6}</span>' if len(names)>6 else '')
    cards.append(f'''<a class="card c-{k}" href="/{k}"><span class="num">{NUM[k]}</span><h3>{e(t)}</h3><p class="cdesc">{e(desc)}</p>
<p class="cnames">{e(" · ".join(names))}</p><div class="cfoot"><span class="stack">{avs}</span><span class="cm">{len(names)} 人 · {count_posts(k)} 条</span></div></a>''')
fk,ft,fd = FEATURE
tq = d['thariq']
picks = ''.join(f'<li>{e(l["title"])}</li>' for l in tq['sections'][0]['blocks'][0]['links'][:3])
feature = f'''<a class="feature c-thariq" href="/{fk}"><div class="fl"><span class="kick">专题</span><h3>{e(ft)}</h3><p>{e(fd)}</p><span class="cta">进入专题 {ICON_ARROW}</span></div>
<div class="fr"><p class="fh">先读这几篇</p><ol>{picks}</ol><p class="cm">{count_posts(fk)} 条帖子与长文</p></div></a>'''
wall = ''.join(f'<a href="/{p["cats"][0]}#{sid}" class="c-{p["cats"][0]}" title="{e(p["name"])} · {e(SHORT[p["cats"][0]])}">{avatar(p["name"], p["cats"][0], "av md")}</a>' for sid,p in people.items())
legend = ''.join(f'<span class="c-{k}"><i></i>{e(NAVSHORT[k])}</span>' for k in ORDER)
home = f'''<section class="hero"><div class="wrap hgrid"><div><p class="kick">精选阅读清单 · 2026</p>
<h1>X 上值得关注的人</h1>
<p class="lede">一组按主题整理的 X（Twitter）阅读清单：创业与产品、思维与投资、AI 与 Agent、人文、教育与儿童成长，外加一份 Thariq 专题。每个人一段简介，配上 2026 年最值得一读的帖子，每条一句话讲清要点，点开即可看原帖。</p>
<dl class="hstats"><div><dt>人物</dt><dd>{len(people)}</dd></div><div><dt>精选帖子</dt><dd>{total_posts}</dd></div><div><dt>清单</dt><dd>{len(ORDER)}</dd></div><div><dt>数据截至</dt><dd class="sm">2026-11-02</dd></div></dl>
<p class="hcta"><a class="btn" href="/people">{ICON_SEARCH}按人名查找</a><a class="btn ghost" href="#lists">浏览清单 {ICON_ARROW}</a></p></div>
<aside class="wall" aria-label="收录的人物"><p class="wh">收录的 {len(people)} 人</p><div class="wgrid">{wall}</div><p class="legend">{legend}</p></aside></div></section>
<section class="wrap home" id="lists"><div class="shead"><h2>六份清单</h2><p>每份清单都以“共同的主线”收尾</p></div>
<div class="cards">{''.join(cards)}</div>
{feature}</section>'''
open(f'{OUT}/index.html','w').write(layout('X 上值得关注的人 · 精选阅读清单', home, 'home', '按主题整理的 X 阅读清单：创业产品、思维投资、AI 与 Agent、人文、教育。'))

rows = []
for sid, p in sorted(people.items(), key=lambda kv: kv[1]['name'].lower()):
    c0 = p['cats'][0]
    tags = ''.join(f'<a class="chip c-{c}" href="/{c}#{sid}">{e(SHORT[c])}</a>' for c in p['cats'])
    rows.append(f'''<li class="pc c-{c0}" data-name="{e((p["name"]+" "+p["handle"]).lower())}" data-cats="{" ".join(p["cats"])}">
<div class="pctop">{avatar(p["name"], c0, "av md")}<div><a class="pname" href="/{c0}#{sid}">{e(p["name"])}</a><a class="handle" href="https://x.com/{e(p["handle"])}" target="_blank" rel="noopener noreferrer">@{e(p["handle"])}</a></div></div>
<p class="pintro">{star(p["intro"])}</p><div class="chips">{tags}</div></li>''')
seg = '<button type="button" class="seg on" data-cat="">全部</button>' + ''.join(f'<button type="button" class="seg c-{k}" data-cat="{k}"><i></i>{e(NAVSHORT[k])}</button>' for k in ORDER)
pbody = f'''<section class="phero"><div class="wrap"><a class="crumb" href="/">首页</a><span class="crumb-sep">/</span><span class="kick">索引</span>
<h1>人物索引</h1><p class="lede">按名字字母排序，共 {len(people)} 人。标签表示此人出现在哪些清单里，点标签可直接跳到对应段落。</p></div></section>
<div class="wrap pindex"><div class="pbar"><label class="filter big">{ICON_SEARCH}<input type="search" placeholder="输入名字或 @账号筛选…" aria-label="筛选人物" data-target="li.pc"></label>
<div class="segs" role="group" aria-label="按清单筛选">{seg}</div><p class="count" aria-live="polite"><b>{len(people)}</b> 人</p></div>
<ul class="pgrid">{''.join(rows)}</ul><p class="empty" hidden>没有匹配的人。</p></div>'''
open(f'{OUT}/people.html','w').write(layout('人物索引 · X 上值得关注的人', pbody, 'people'))
open(f'{OUT}/404.html','w').write(layout('页面不存在', '<section class="phero"><div class="wrap"><span class="kick">404</span><h1>页面不存在</h1><p class="lede"><a href="/">回到首页</a></p></div></section>', ''))
shutil.copy('style.css', OUT); shutil.copy('site.js', OUT)
print(len(people), 'people', total_posts, 'posts', sorted(os.listdir(OUT)))
