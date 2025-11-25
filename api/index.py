from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VAULT 13</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: monospace;
            background: #0a0a0f;
            color: #00ff88;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 20px;
        }
        h1 { font-size: 3rem; margin-bottom: 1rem; text-shadow: 0 0 20px rgba(0,255,136,0.5); }
        p { color: #808080; margin-bottom: 2rem; }
        .games { display: grid; gap: 1rem; max-width: 600px; margin: 0 auto; }
        .game {
            background: #12121a;
            border: 1px solid #333;
            padding: 1rem;
            border-radius: 8px;
        }
        .game:hover { border-color: #00ff88; }
        .name { color: #00ff88; font-size: 1.1rem; }
        .desc { color: #666; font-size: 0.85rem; margin-top: 0.5rem; }
    </style>
</head>
<body>
    <div>
        <h1>VAULT 13</h1>
        <p>Terminal Game Collection v9.0</p>
        <p style="color:#ffc800;background:rgba(255,200,0,0.1);padding:1rem;border-radius:8px;margin-bottom:2rem;">
            Run locally: python deploy/web-terminal/app_crossplatform.py
        </p>
        <div class="games">
            <div class="game"><div class="name">VAULT 13 Ultimate</div><div class="desc">Full vault simulation</div></div>
            <div class="game"><div class="name">Echo Chambers</div><div class="desc">Quantum timeline paradoxes</div></div>
            <div class="game"><div class="name">Chinese Room</div><div class="desc">Philosophy of mind</div></div>
        </div>
    </div>
</body>
</html>'''
        self.wfile.write(html.encode())
        return
