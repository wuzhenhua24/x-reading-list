import os, json
ct = {'.svg':'image/svg+xml','.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'application/javascript; charset=utf-8'}
files = {}
for f in sorted(os.listdir('dist')):
    files['/'+f] = [ct[os.path.splitext(f)[1]], open('dist/'+f,encoding='utf-8').read()]
worker = "const FILES = " + json.dumps(files, ensure_ascii=False) + r""";
export default {
  async fetch(request) {
    const url = new URL(request.url);
    let p = decodeURIComponent(url.pathname);
    if (p.length > 1 && p.endsWith('/')) p = p.slice(0, -1);
    if (p === '/' ) p = '/index.html';
    if (p.endsWith('.html') && p !== '/index.html' && p !== '/404.html' && FILES[p]) {
      return Response.redirect(url.origin + p.slice(0, -5) + url.search, 301);
    }
    let f = FILES[p] || FILES[p + '.html'];
    const status = f ? 200 : 404;
    if (!f) f = FILES['/404.html'];
    return new Response(request.method === 'HEAD' ? null : f[1], { status, headers: {
      'content-type': f[0],
      'cache-control': f[0].startsWith('text/html') ? 'public, max-age=300' : 'public, max-age=3600',
      'x-content-type-options': 'nosniff',
      'referrer-policy': 'strict-origin-when-cross-origin'
    }});
  }
};
"""
open('_worker.js','w',encoding='utf-8').write(worker)
js = "async () => {\nconst W = " + json.dumps(worker, ensure_ascii=False) + r""";
const base = `/accounts/${accountId}/pages/projects/x-reading-list`;
const form = new FormData();
form.append('manifest', JSON.stringify({}));
form.append('branch', 'main');
form.append('_worker.js', new Blob([W], {type:'application/javascript+module'}), '_worker.js');
const dep = (await cloudflare.request({method:'POST', path:`${base}/deployments`, body: form})).result;
return {url: dep.url, id: dep.id, stage: dep.latest_stage, aliases: dep.aliases};
}"""
open('deploy2.js','w',encoding='utf-8').write(js); print(len(worker))
