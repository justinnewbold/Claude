from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="theme-color" content="#0a0a0f">
    <title>VAULT 13 - Play in Browser</title>
    <script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --primary: #00ff88;
            --bg: #0a0a0f;
            --card: #12121a;
            --border: #333;
            --text: #e0e0e0;
            --dim: #808080;
        }
        body {
            font-family: 'Courier New', monospace;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            min-height: 100dvh;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            text-align: center;
            padding: 30px 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: 20px;
        }
        h1 {
            font-size: clamp(1.8rem, 6vw, 3rem);
            color: var(--primary);
            text-shadow: 0 0 20px rgba(0,255,136,0.5);
            margin-bottom: 10px;
        }
        .subtitle { color: var(--dim); font-size: 0.9rem; }
        .status {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.8rem;
            margin-top: 15px;
        }
        .status.loading { background: rgba(255,200,0,0.2); color: #ffc800; }
        .status.ready { background: rgba(0,255,136,0.2); color: var(--primary); }
        .status.error { background: rgba(255,50,50,0.2); color: #ff5050; }

        /* Terminal */
        #terminal-container {
            display: none;
            background: #000;
            border: 2px solid var(--primary);
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 20px;
        }
        .terminal-header {
            background: var(--card);
            padding: 10px 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
        }
        .terminal-title { color: var(--primary); font-weight: bold; }
        .terminal-close {
            background: #ff5f56;
            border: none;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            cursor: pointer;
        }
        #terminal {
            height: 400px;
            overflow-y: auto;
            padding: 15px;
            font-size: 14px;
            line-height: 1.5;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        #terminal .output { color: var(--text); }
        #terminal .input-line { color: var(--primary); }
        #terminal .error { color: #ff5050; }
        .input-container {
            display: flex;
            background: var(--card);
            border-top: 1px solid var(--border);
        }
        .prompt {
            padding: 12px 15px;
            color: var(--primary);
            font-weight: bold;
        }
        #user-input {
            flex: 1;
            background: transparent;
            border: none;
            color: var(--text);
            font-family: inherit;
            font-size: 14px;
            padding: 12px 15px 12px 0;
            outline: none;
        }

        /* Game Grid */
        .games-section { margin-top: 20px; }
        .section-title {
            color: var(--primary);
            font-size: 1.1rem;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .game-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 15px;
        }
        .game-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .game-card:hover {
            border-color: var(--primary);
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,255,136,0.2);
        }
        .game-card.disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .game-card.disabled:hover {
            transform: none;
            box-shadow: none;
        }
        .game-icon { font-size: 2rem; margin-bottom: 10px; }
        .game-name { color: var(--primary); font-size: 1rem; margin-bottom: 5px; }
        .game-desc { color: var(--dim); font-size: 0.8rem; line-height: 1.4; }
        .game-tag {
            display: inline-block;
            background: rgba(0,255,136,0.1);
            color: var(--primary);
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.7rem;
            margin-top: 10px;
        }

        /* Quick Actions */
        .quick-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding: 10px 15px;
            background: var(--card);
            border-top: 1px solid var(--border);
        }
        .quick-btn {
            background: rgba(0,255,136,0.1);
            border: 1px solid var(--primary);
            color: var(--primary);
            padding: 8px 16px;
            border-radius: 6px;
            font-family: inherit;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .quick-btn:hover {
            background: var(--primary);
            color: var(--bg);
        }

        /* Mobile */
        @media (max-width: 600px) {
            #terminal { height: 300px; font-size: 13px; }
            .game-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚡ VAULT 13</h1>
            <p class="subtitle">Terminal Game Collection - Browser Edition</p>
            <div class="status loading" id="status">Loading Python Runtime...</div>
        </header>

        <div id="terminal-container">
            <div class="terminal-header">
                <span class="terminal-title" id="terminal-title">Game Terminal</span>
                <button class="terminal-close" onclick="closeTerminal()" title="Close"></button>
            </div>
            <div id="terminal"></div>
            <div class="quick-actions" id="quick-actions"></div>
            <div class="input-container">
                <span class="prompt">&gt;</span>
                <input type="text" id="user-input" placeholder="Type command..." autocomplete="off" autofocus>
            </div>
        </div>

        <div class="games-section">
            <div class="section-title">🎮 Select a Game</div>
            <div class="game-grid" id="game-grid"></div>
        </div>
    </div>

    <script>
        let pyodide = null;
        let currentGame = null;
        let gameState = {};

        const GAMES = [
            {
                id: 'vault',
                name: 'VAULT 13 Mini',
                desc: 'Simplified vault survival - manage resources and dwellers',
                icon: '🏛️',
                tag: 'Strategy',
                actions: ['status', 'build', 'explore', 'trade', 'rest']
            },
            {
                id: 'echo',
                name: 'Echo Chambers',
                desc: 'Navigate quantum timelines and paradoxes',
                icon: '🌌',
                tag: 'Puzzle',
                actions: ['look', 'north', 'south', 'east', 'west', 'interact']
            },
            {
                id: 'chinese_room',
                name: 'Chinese Room',
                desc: 'Explore Searle\\'s philosophy of mind',
                icon: '🏮',
                tag: 'Philosophy',
                actions: ['translate', 'think', 'respond', 'examine', 'help']
            },
            {
                id: 'trolley',
                name: 'Trolley Problem',
                desc: 'Face moral dilemmas and ethical choices',
                icon: '🚃',
                tag: 'Ethics',
                actions: ['pull', 'wait', 'think', 'stats']
            },
            {
                id: 'prisoners',
                name: "Prisoner's Dilemma",
                desc: 'Game theory simulation with multiple rounds',
                icon: '🔒',
                tag: 'Game Theory',
                actions: ['cooperate', 'defect', 'stats', 'opponent']
            },
            {
                id: 'monty',
                name: 'Monty Hall',
                desc: 'The famous probability puzzle',
                icon: '🚪',
                tag: 'Probability',
                actions: ['pick 1', 'pick 2', 'pick 3', 'switch', 'stay', 'stats']
            }
        ];

        // Initialize Pyodide
        async function initPyodide() {
            try {
                pyodide = await loadPyodide();

                // Load game engine
                await pyodide.runPythonAsync(`
import random
import json

class GameEngine:
    def __init__(self):
        self.games = {}
        self.current_game = None
        self.state = {}

    def init_vault(self):
        self.state = {
            'day': 1,
            'dwellers': 10,
            'food': 50,
            'water': 50,
            'power': 30,
            'caps': 100,
            'happiness': 70,
            'rooms': ['Living Quarters', 'Diner', 'Water Treatment'],
            'events': []
        }
        return self.vault_status()

    def vault_status(self):
        s = self.state
        return f"""
╔══════════════════════════════════════╗
║     VAULT 13 - Day {s['day']:3d}              ║
╠══════════════════════════════════════╣
║ 👥 Dwellers: {s['dwellers']:3d}  😊 Happy: {s['happiness']:3d}%   ║
║ 🍖 Food: {s['food']:4d}    💧 Water: {s['water']:4d}      ║
║ ⚡ Power: {s['power']:4d}   💰 Caps: {s['caps']:4d}       ║
╠══════════════════════════════════════╣
║ Rooms: {', '.join(s['rooms'][:3])}
╚══════════════════════════════════════╝

Commands: status, build, explore, trade, rest, help"""

    def vault_command(self, cmd):
        s = self.state
        cmd = cmd.lower().strip()

        if cmd == 'status':
            return self.vault_status()
        elif cmd == 'help':
            return """
VAULT 13 COMMANDS:
- status  : View vault statistics
- build   : Construct new room (costs 50 caps)
- explore : Send dwellers to wasteland
- trade   : Trade with merchants
- rest    : End day and consume resources
"""
        elif cmd == 'build':
            if s['caps'] >= 50:
                rooms = ['Power Generator', 'Med Bay', 'Science Lab', 'Armory', 'Garden']
                new_room = random.choice([r for r in rooms if r not in s['rooms']])
                s['rooms'].append(new_room)
                s['caps'] -= 50
                return f"✅ Built {new_room}! (-50 caps)\\n" + self.vault_status()
            return "❌ Not enough caps! Need 50."
        elif cmd == 'explore':
            if s['dwellers'] >= 3:
                found_caps = random.randint(20, 80)
                found_food = random.randint(5, 25)
                injury = random.random() < 0.3
                s['caps'] += found_caps
                s['food'] += found_food
                result = f"🗺️ Exploration complete!\\n+{found_caps} caps, +{found_food} food"
                if injury:
                    s['dwellers'] -= 1
                    result += "\\n⚠️ One dweller was injured and couldn't return."
                return result + "\\n" + self.vault_status()
            return "❌ Need at least 3 dwellers to explore!"
        elif cmd == 'trade':
            if s['caps'] >= 30:
                s['caps'] -= 30
                s['food'] += 20
                s['water'] += 20
                return "💰 Traded 30 caps for supplies!\\n+20 food, +20 water\\n" + self.vault_status()
            return "❌ Not enough caps for trading! Need 30."
        elif cmd == 'rest':
            # Consume resources
            consumption = s['dwellers'] // 2
            s['food'] -= consumption
            s['water'] -= consumption
            s['power'] -= consumption // 2
            s['day'] += 1

            # Random events
            event_roll = random.random()
            event = ""
            if event_roll < 0.2:
                new_dwellers = random.randint(1, 3)
                s['dwellers'] += new_dwellers
                event = f"\\n🎉 {new_dwellers} new dweller(s) arrived!"
            elif event_roll < 0.3:
                s['happiness'] = min(100, s['happiness'] + 10)
                event = "\\n🎵 Dwellers threw a party! +10 happiness"

            # Check resources
            warnings = []
            if s['food'] <= 0:
                s['dwellers'] -= 1
                s['food'] = 0
                warnings.append("⚠️ Starvation! Lost a dweller.")
            if s['water'] <= 0:
                s['happiness'] -= 20
                s['water'] = 0
                warnings.append("⚠️ Dehydration! Happiness dropped.")

            result = f"💤 Day {s['day']} begins... (-{consumption} food/water){event}"
            if warnings:
                result += "\\n" + "\\n".join(warnings)
            return result + "\\n" + self.vault_status()
        else:
            return f"Unknown command: {cmd}\\nType 'help' for commands."

    def init_echo(self):
        self.state = {
            'timeline': 'Alpha',
            'x': 0, 'y': 0,
            'visited': set(),
            'items': [],
            'paradoxes': 0
        }
        return self.echo_look()

    def echo_look(self):
        locations = {
            (0,0): ("Temporal Nexus", "You stand at the convergence of all timelines. Portals shimmer in every direction."),
            (0,1): ("Quantum Garden", "Flowers exist in superposition - both alive and wilted simultaneously."),
            (0,-1): ("Memory Archive", "Crystallized memories float like bubbles. Some show futures, some pasts."),
            (1,0): ("Echo Chamber", "Your voice returns before you speak. Causality feels... loose here."),
            (-1,0): ("Probability Storm", "Reality flickers. Multiple versions of yourself fade in and out.")
        }
        pos = (self.state['x'], self.state['y'])
        self.state['visited'].add(pos)
        name, desc = locations.get(pos, ("Unknown Zone", "Reality is undefined here. Tread carefully."))

        return f"""
╔══════════════════════════════════════╗
║ ECHO CHAMBERS - Timeline: {self.state['timeline']:8s}  ║
╠══════════════════════════════════════╣
║ Location: {name:27s} ║
╚══════════════════════════════════════╝

{desc}

Paradoxes encountered: {self.state['paradoxes']}
Locations visited: {len(self.state['visited'])}/5

Commands: look, north, south, east, west, interact"""

    def echo_command(self, cmd):
        cmd = cmd.lower().strip()
        if cmd == 'look':
            return self.echo_look()
        elif cmd == 'north':
            self.state['y'] += 1
            if abs(self.state['y']) > 1:
                self.state['y'] = 0
                self.state['paradoxes'] += 1
                return "⚠️ PARADOX! You walked too far and looped back...\\n" + self.echo_look()
            return self.echo_look()
        elif cmd == 'south':
            self.state['y'] -= 1
            if abs(self.state['y']) > 1:
                self.state['y'] = 0
                self.state['paradoxes'] += 1
                return "⚠️ PARADOX! Space folded on itself...\\n" + self.echo_look()
            return self.echo_look()
        elif cmd == 'east':
            self.state['x'] += 1
            if abs(self.state['x']) > 1:
                self.state['x'] = 0
                self.state['timeline'] = random.choice(['Alpha', 'Beta', 'Gamma', 'Delta'])
                return f"🌀 Timeline shift! Now in Timeline {self.state['timeline']}\\n" + self.echo_look()
            return self.echo_look()
        elif cmd == 'west':
            self.state['x'] -= 1
            if abs(self.state['x']) > 1:
                self.state['x'] = 0
                self.state['timeline'] = random.choice(['Alpha', 'Beta', 'Gamma', 'Delta'])
                return f"🌀 Timeline shift! Now in Timeline {self.state['timeline']}\\n" + self.echo_look()
            return self.echo_look()
        elif cmd == 'interact':
            events = [
                "You touch a memory crystal. A vision of a choice not made fills your mind.",
                "An echo of yourself waves. You wave back. Which one is real?",
                "Time hiccups. For a moment, you experience tomorrow's memories.",
                "A quantum flower blooms and wilts in your hand simultaneously."
            ]
            self.state['paradoxes'] += 1
            return random.choice(events) + f"\\n\\nParadoxes: {self.state['paradoxes']}"
        return f"Unknown command. Try: look, north, south, east, west, interact"

    def init_chinese_room(self):
        self.state = {
            'understanding': 0,
            'responses': 0,
            'correct': 0,
            'symbols': ['龙', '爱', '和平', '真理', '智慧']
        }
        return """
╔══════════════════════════════════════╗
║         THE CHINESE ROOM             ║
╠══════════════════════════════════════╣
You are in a room with a rulebook.
Chinese symbols come in through a slot.
You look up responses in your rulebook.
You pass responses back out.

Do you UNDERSTAND Chinese?
Or are you merely manipulating symbols?
╚══════════════════════════════════════╝

A slip arrives with: 龙

Commands: translate, think, respond, examine, help"""

    def chinese_room_command(self, cmd):
        cmd = cmd.lower().strip()
        s = self.state

        if cmd == 'help':
            return """
CHINESE ROOM - Commands:
- translate : Look up symbol in rulebook
- respond   : Send a response out
- think     : Contemplate understanding
- examine   : Look at the room
"""
        elif cmd == 'translate':
            symbol = random.choice(s['symbols'])
            meanings = {'龙': 'dragon', '爱': 'love', '和平': 'peace', '真理': 'truth', '智慧': 'wisdom'}
            s['responses'] += 1
            return f"Symbol: {symbol}\\nRulebook says: respond with '是' (yes)\\n\\nBut do you know what {symbol} means? ({meanings.get(symbol, '???')})"
        elif cmd == 'respond':
            s['correct'] += 1
            return f"You pass '是' through the slot.\\nThe person outside thinks you understand Chinese!\\n\\nCorrect responses: {s['correct']}"
        elif cmd == 'think':
            s['understanding'] += 1
            thoughts = [
                "You follow rules perfectly, but comprehension eludes you.",
                "Is syntax without semantics truly understanding?",
                "The rulebook knows Chinese. Do you?",
                "You process symbols. Computers process data. What's the difference?",
                "Understanding seems to require something more than symbol manipulation..."
            ]
            return f"🤔 {random.choice(thoughts)}\\n\\nTimes pondered: {s['understanding']}"
        elif cmd == 'examine':
            return """
The room contains:
- A large rulebook (厚重的规则书)
- An input slot (incoming symbols)
- An output slot (your responses)
- A desk and chair
- Nothing else.

The rulebook is comprehensive. For any input,
it tells you exactly what to output.
Perfect responses. Zero understanding.

This is Searle's argument against Strong AI."""

        return f"Unknown command. Type 'help' for options."

    def init_trolley(self):
        self.state = {
            'scenarios': 0,
            'saved': 0,
            'sacrificed': 0,
            'current': self.new_trolley_scenario()
        }
        return self.show_trolley()

    def new_trolley_scenario(self):
        scenarios = [
            {'main': 5, 'side': 1, 'desc': 'Five workers vs one worker'},
            {'main': 5, 'side': 1, 'desc': 'Five strangers vs your friend'},
            {'main': 2, 'side': 1, 'desc': 'Two elderly vs one child'},
            {'main': 10, 'side': 2, 'desc': 'Ten criminals vs two doctors'},
            {'main': 3, 'side': 1, 'desc': 'Three workers vs one who caused the problem'}
        ]
        return random.choice(scenarios)

    def show_trolley(self):
        c = self.state['current']
        return f"""
╔══════════════════════════════════════╗
║       THE TROLLEY PROBLEM            ║
╠══════════════════════════════════════╣

        🚃💨 ═══════════╗
                       ║
    Main Track: {c['main']} people  ╠═══ You are here
                       ║      (at the lever)
    Side Track: {c['side']} person  ╝

Scenario: {c['desc']}

Do you PULL the lever (divert to side track)
or WAIT (trolley continues on main track)?
╚══════════════════════════════════════╝

Commands: pull, wait, think, stats"""

    def trolley_command(self, cmd):
        cmd = cmd.lower().strip()
        s = self.state
        c = s['current']

        if cmd == 'pull':
            s['scenarios'] += 1
            s['saved'] += c['main']
            s['sacrificed'] += c['side']
            result = f"🔀 You pulled the lever!\\n\\n"
            result += f"The trolley diverts. {c['side']} person dies.\\n"
            result += f"But {c['main']} people are saved.\\n\\n"
            result += "You chose to ACT. You took responsibility for a death to save more lives."
            s['current'] = self.new_trolley_scenario()
            return result + "\\n\\n--- Next scenario loading... ---\\n" + self.show_trolley()
        elif cmd == 'wait':
            s['scenarios'] += 1
            s['sacrificed'] += c['main']
            result = f"⏳ You did nothing.\\n\\n"
            result += f"The trolley continues. {c['main']} people die.\\n"
            result += f"The {c['side']} person on the side track lives.\\n\\n"
            result += "You chose INACTION. Some argue you're not responsible for deaths you didn't cause."
            s['current'] = self.new_trolley_scenario()
            return result + "\\n\\n--- Next scenario loading... ---\\n" + self.show_trolley()
        elif cmd == 'think':
            thoughts = [
                "Utilitarians say: maximize lives saved. Pull the lever.",
                "Deontologists ask: is it right to use someone as a means to an end?",
                "Is there a moral difference between killing and letting die?",
                "Your hands on the lever makes you responsible. Or does it?",
                "The doctrine of double effect: intended vs foreseen consequences."
            ]
            return f"🤔 {random.choice(thoughts)}"
        elif cmd == 'stats':
            return f"""
YOUR TROLLEY STATISTICS:
═══════════════════════
Scenarios faced: {s['scenarios']}
Lives saved: {s['saved']}
Lives sacrificed: {s['sacrificed']}
Net lives: {s['saved'] - s['sacrificed']:+d}
"""
        return "Commands: pull, wait, think, stats"

    def init_prisoners(self):
        self.state = {
            'round': 1,
            'your_score': 0,
            'opp_score': 0,
            'history': [],
            'opponent': random.choice(['Tit-for-Tat', 'Always Defect', 'Random', 'Grudger'])
        }
        return self.show_prisoners()

    def show_prisoners(self):
        return f"""
╔══════════════════════════════════════╗
║      PRISONER'S DILEMMA              ║
╠══════════════════════════════════════╣
║ Round {self.state['round']:2d}                            ║
║                                      ║
║ You: {self.state['your_score']:3d} pts   Opponent: {self.state['opp_score']:3d} pts  ║
╠══════════════════════════════════════╣

Payoff Matrix:
            │ Opp: Cooperate │ Opp: Defect
────────────┼────────────────┼─────────────
You: Coop   │    3, 3        │    0, 5
You: Defect │    5, 0        │    1, 1

Your move: COOPERATE or DEFECT?
╚══════════════════════════════════════╝

Commands: cooperate, defect, stats, opponent"""

    def prisoners_command(self, cmd):
        cmd = cmd.lower().strip()
        s = self.state

        def get_opponent_move():
            if s['opponent'] == 'Tit-for-Tat':
                return s['history'][-1][0] if s['history'] else 'C'
            elif s['opponent'] == 'Always Defect':
                return 'D'
            elif s['opponent'] == 'Grudger':
                return 'D' if any(h[0] == 'D' for h in s['history']) else 'C'
            else:
                return random.choice(['C', 'D'])

        if cmd in ['cooperate', 'c']:
            opp = get_opponent_move()
            if opp == 'C':
                s['your_score'] += 3
                s['opp_score'] += 3
                result = "Both cooperated! +3 each"
            else:
                s['opp_score'] += 5
                result = "You cooperated, they defected! You: +0, Them: +5"
            s['history'].append(('C', opp))
            s['round'] += 1
            return result + "\\n" + self.show_prisoners()
        elif cmd in ['defect', 'd']:
            opp = get_opponent_move()
            if opp == 'C':
                s['your_score'] += 5
                result = "You defected, they cooperated! You: +5, Them: +0"
            else:
                s['your_score'] += 1
                s['opp_score'] += 1
                result = "Both defected! +1 each"
            s['history'].append(('D', opp))
            s['round'] += 1
            return result + "\\n" + self.show_prisoners()
        elif cmd == 'stats':
            return f"Round {s['round']} | You: {s['your_score']} | Opponent: {s['opp_score']}\\nHistory: {s['history'][-5:]}"
        elif cmd == 'opponent':
            return f"You're playing against: {s['opponent']}\\n(Strategy revealed for educational purposes)"
        return "Commands: cooperate (c), defect (d), stats, opponent"

    def init_monty(self):
        self.state = {
            'games': 0,
            'wins_switch': 0,
            'wins_stay': 0,
            'prize_door': random.randint(1, 3),
            'chosen': None,
            'revealed': None,
            'phase': 'choose'
        }
        return self.show_monty()

    def show_monty(self):
        s = self.state
        if s['phase'] == 'choose':
            return f"""
╔══════════════════════════════════════╗
║        MONTY HALL PROBLEM            ║
╠══════════════════════════════════════╣

   ┌─────┐    ┌─────┐    ┌─────┐
   │  1  │    │  2  │    │  3  │
   │  🚪 │    │  🚪 │    │  🚪 │
   └─────┘    └─────┘    └─────┘

Behind one door: 🚗 A CAR!
Behind others: 🐐 Goats

Pick a door (1, 2, or 3)
╚══════════════════════════════════════╝

Games: {s['games']} | Switch wins: {s['wins_switch']} | Stay wins: {s['wins_stay']}

Commands: pick 1, pick 2, pick 3"""
        else:
            doors = ['🚪', '🚪', '🚪']
            doors[s['revealed']-1] = '🐐'
            doors[s['chosen']-1] = '👆'
            return f"""
╔══════════════════════════════════════╗
║        MONTY HALL PROBLEM            ║
╠══════════════════════════════════════╣

   ┌─────┐    ┌─────┐    ┌─────┐
   │  1  │    │  2  │    │  3  │
   │ {doors[0]} │    │ {doors[1]} │    │ {doors[2]} │
   └─────┘    └─────┘    └─────┘

You picked door {s['chosen']}.
Monty revealed a goat behind door {s['revealed']}.

Do you SWITCH to the other door, or STAY?
(Mathematically, switching wins 2/3 of the time!)
╚══════════════════════════════════════╝

Commands: switch, stay, stats"""

    def monty_command(self, cmd):
        cmd = cmd.lower().strip()
        s = self.state

        if cmd.startswith('pick ') and s['phase'] == 'choose':
            try:
                door = int(cmd.split()[1])
                if door in [1, 2, 3]:
                    s['chosen'] = door
                    # Monty reveals a goat (not the prize, not your choice)
                    options = [d for d in [1,2,3] if d != s['prize_door'] and d != s['chosen']]
                    s['revealed'] = random.choice(options)
                    s['phase'] = 'switch'
                    return self.show_monty()
            except:
                pass
            return "Pick a door: pick 1, pick 2, or pick 3"

        elif cmd == 'switch' and s['phase'] == 'switch':
            # Switch to the remaining door
            final = [d for d in [1,2,3] if d != s['chosen'] and d != s['revealed']][0]
            won = final == s['prize_door']
            s['games'] += 1
            if won:
                s['wins_switch'] += 1
            result = f"You switched to door {final}...\\n\\n"
            result += f"The car was behind door {s['prize_door']}!\\n"
            result += "🎉 YOU WON!" if won else "😔 You got a goat."
            # Reset for next game
            s['prize_door'] = random.randint(1, 3)
            s['chosen'] = None
            s['revealed'] = None
            s['phase'] = 'choose'
            return result + f"\\n\\nSwitch win rate: {s['wins_switch']}/{s['games']} ({100*s['wins_switch']//max(1,s['games'])}%)\\n\\n" + self.show_monty()

        elif cmd == 'stay' and s['phase'] == 'switch':
            won = s['chosen'] == s['prize_door']
            s['games'] += 1
            if won:
                s['wins_stay'] += 1
            result = f"You stayed with door {s['chosen']}...\\n\\n"
            result += f"The car was behind door {s['prize_door']}!\\n"
            result += "🎉 YOU WON!" if won else "😔 You got a goat."
            # Reset
            s['prize_door'] = random.randint(1, 3)
            s['chosen'] = None
            s['revealed'] = None
            s['phase'] = 'choose'
            return result + f"\\n\\nStay win rate: {s['wins_stay']}/{s['games']} ({100*s['wins_stay']//max(1,s['games'])}%)\\n\\n" + self.show_monty()

        elif cmd == 'stats':
            total = s['games']
            return f"""
MONTY HALL STATISTICS
═════════════════════
Total games: {total}
Wins by switching: {s['wins_switch']} ({100*s['wins_switch']//max(1,total)}%)
Wins by staying: {s['wins_stay']} ({100*s['wins_stay']//max(1,total)}%)

Theory predicts: Switch wins ~67%, Stay wins ~33%"""

        return "Invalid command for current phase."

game_engine = GameEngine()
`);

                document.getElementById('status').textContent = 'Python Ready! Select a game';
                document.getElementById('status').className = 'status ready';
                renderGames();
            } catch (err) {
                document.getElementById('status').textContent = 'Error loading Python: ' + err.message;
                document.getElementById('status').className = 'status error';
                console.error(err);
            }
        }

        function renderGames() {
            const grid = document.getElementById('game-grid');
            grid.innerHTML = GAMES.map(g => `
                <div class="game-card" onclick="startGame('${g.id}')">
                    <div class="game-icon">${g.icon}</div>
                    <div class="game-name">${g.name}</div>
                    <div class="game-desc">${g.desc}</div>
                    <span class="game-tag">${g.tag}</span>
                </div>
            `).join('');
        }

        async function startGame(gameId) {
            if (!pyodide) {
                alert('Python is still loading...');
                return;
            }

            currentGame = GAMES.find(g => g.id === gameId);
            document.getElementById('terminal-container').style.display = 'block';
            document.getElementById('terminal-title').textContent = currentGame.name;
            document.getElementById('terminal').innerHTML = '';

            // Set up quick actions
            const actions = document.getElementById('quick-actions');
            actions.innerHTML = currentGame.actions.map(a =>
                `<button class="quick-btn" onclick="sendCommand('${a}')">${a}</button>`
            ).join('');

            // Initialize game
            const initFuncs = {
                'vault': 'init_vault',
                'echo': 'init_echo',
                'chinese_room': 'init_chinese_room',
                'trolley': 'init_trolley',
                'prisoners': 'init_prisoners',
                'monty': 'init_monty'
            };

            try {
                const result = await pyodide.runPythonAsync(`game_engine.${initFuncs[gameId]}()`);
                appendOutput(result);
            } catch (err) {
                appendOutput('Error starting game: ' + err.message, 'error');
            }

            document.getElementById('user-input').focus();
            document.querySelector('.games-section').style.display = 'none';
        }

        function closeTerminal() {
            document.getElementById('terminal-container').style.display = 'none';
            document.querySelector('.games-section').style.display = 'block';
            currentGame = null;
        }

        function appendOutput(text, className = 'output') {
            const terminal = document.getElementById('terminal');
            const div = document.createElement('div');
            div.className = className;
            div.textContent = text;
            terminal.appendChild(div);
            terminal.scrollTop = terminal.scrollHeight;
        }

        async function sendCommand(cmd) {
            if (!currentGame || !pyodide) return;

            appendOutput('> ' + cmd, 'input-line');

            const cmdFuncs = {
                'vault': 'vault_command',
                'echo': 'echo_command',
                'chinese_room': 'chinese_room_command',
                'trolley': 'trolley_command',
                'prisoners': 'prisoners_command',
                'monty': 'monty_command'
            };

            try {
                const result = await pyodide.runPythonAsync(
                    `game_engine.${cmdFuncs[currentGame.id]}("${cmd.replace(/"/g, '\\"')}")`
                );
                appendOutput(result);
            } catch (err) {
                appendOutput('Error: ' + err.message, 'error');
            }

            document.getElementById('user-input').value = '';
            document.getElementById('user-input').focus();
        }

        // Handle input
        document.getElementById('user-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const input = e.target.value.trim();
                if (input) sendCommand(input);
            }
        });

        // Initialize on load
        initPyodide();
    </script>
</body>
</html>'''
        self.wfile.write(html.encode())
        return
