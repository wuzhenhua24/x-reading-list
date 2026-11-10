import http.server, os
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s,*a,**k): super().__init__(*a,directory='dist',**k)
    def do_GET(s):
        p=s.path.split('?')[0].split('#')[0]
        if p!='/' and '.' not in p: s.path=p+'.html'
        return super().do_GET()
    def log_message(s,*a): pass
http.server.ThreadingHTTPServer(('127.0.0.1',8765),H).serve_forever()
