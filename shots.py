import sys
from playwright.sync_api import sync_playwright
base = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8765'
pre = sys.argv[2] if len(sys.argv)>2 else ''
pages=[('home','/'),('ai','/ai'),('people','/people'),('thariq','/thariq')]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for scheme in ['light','dark']:
      for w,h,tag in [(1280,900,'desktop'),(390,844,'mobile')]:
        ctx=b.new_context(viewport={'width':w,'height':h},device_scale_factor=1 if w>500 else 2,color_scheme=scheme)
        pg=ctx.new_page()
        for name,path in pages:
            if scheme=='dark' and name=='thariq': continue
            pg.goto(base+path); pg.wait_for_timeout(300)
            pg.screenshot(path=f'shots/{pre}{name}-{tag}{"-dark" if scheme=="dark" else ""}.png', full_page=False)
            if scheme=='light': pg.screenshot(path=f'shots/{pre}{name}-{tag}-full.png', full_page=True)
        ctx.close()
    b.close()
