"""
Vercel Serverless Function Entrypoint for VAULT 13 Web Terminal
"""

from flask import Flask, Response

app = Flask(__name__)

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="#0a0a0f">
    <title>VAULT 13 - Game Collection</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --primary: #00ff88;
            --secondary: #00ffcc;
            --bg-dark: #0a0a0f;
            --bg-card: #12121a;
            --text: #e0e0e0;
            --text-dim: #808080;
            --safe-top: env(safe-area-inset-top, 0px);
            --safe-bottom: env(safe-area-inset-bottom, 0px);
        }
        body {
            font-family: 'Courier New', monospace;
            background: var(--bg-dark);
            color: var(--text);
            min-height: 100dvh;
            padding: var(--safe-top) 16px var(--safe-bottom);
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px 0;
        }
        .header {
            text-align: center;
            padding: 40px 0;
            border-bottom: 1px solid #333;
            margin-bottom: 30px;
        }
        .logo {
            font-size: clamp(2rem, 8vw, 3.5rem);
            font-weight: bold;
            color: var(--primary);
            text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
            margin-bottom: 10px;
        }
        .subtitle {
            color: var(--text-dim);
            font-size: 1rem;
        }
        .game-grid {
            display: grid;
            gap: 16px;
        }
        .game-card {
            background: var(--bg-card);
            border: 1px solid #333;
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
        }
        .game-card:hover {
            border-color: var(--primary);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
        }
        .game-name {
            color: var(--primary);
            font-size: 1.2rem;
            margin-bottom: 8px;
        }
        .game-desc {
            color: var(--text-dim);
            font-size: 0.9rem;
            margin-bottom: 12px;
        }
        .game-category {
            display: inline-block;
            background: rgba(0, 255, 136, 0.1);
            color: var(--primary);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
        }
        .notice {
            background: rgba(255, 200, 0, 0.1);
            border: 1px solid rgba(255, 200, 0, 0.3);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 24px;
            color: #ffc800;
            font-size: 0.9rem;
        }
        .notice-title {
            font-weight: bold;
            margin-bottom: 8px;
        }
        a { color: var(--secondary); }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="logo">VAULT 13</div>
            <div class="subtitle">Terminal Game Collection v9.0</div>
        </header>

        <div class="notice">
            <div class="notice-title">Deployment Notice</div>
            <p>This is a static preview. Terminal games require WebSocket support for real-time gameplay.
            Run locally with: <code>python deploy/web-terminal/app_crossplatform.py</code></p>
        </div>

        <div class="game-grid">
            <div class="game-card">
                <div class="game-name">VAULT 13 v9.0 - Ultimate Evolution</div>
                <div class="game-desc">Complete vault survival simulation with 15+ game systems</div>
                <span class="game-category">Main Games</span>
            </div>
            <div class="game-card">
                <div class="game-name">Echo Chambers</div>
                <div class="game-desc">Navigate through quantum timeline paradoxes</div>
                <span class="game-category">Quantum & Physics</span>
            </div>
            <div class="game-card">
                <div class="game-name">Boltzmann's Demon</div>
                <div class="game-desc">Statistical mechanics thought experiment</div>
                <span class="game-category">Physics Simulations</span>
            </div>
            <div class="game-card">
                <div class="game-name">Newcomb's Paradox</div>
                <div class="game-desc">Decision theory and free will exploration</div>
                <span class="game-category">Decision Theory</span>
            </div>
            <div class="game-card">
                <div class="game-name">Chinese Room</div>
                <div class="game-desc">Searle's philosophy of mind experiment</div>
                <span class="game-category">Philosophy of Mind</span>
            </div>
        </div>
    </div>
</body>
</html>"""


@app.route('/')
def index():
    return Response(HTML_PAGE, mimetype='text/html')


@app.route('/api/health')
def health():
    return {'status': 'ok', 'platform': 'vercel'}


# Vercel handler
handler = app
