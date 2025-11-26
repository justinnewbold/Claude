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

        /* AI Assistant */
        .ai-fab {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
            z-index: 1000;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .ai-fab:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 30px rgba(99, 102, 241, 0.6);
        }
        .ai-fab.active {
            background: linear-gradient(135deg, #8b5cf6, #a855f7);
        }
        .ai-panel {
            position: fixed;
            bottom: 90px;
            right: 20px;
            width: 350px;
            max-width: calc(100vw - 40px);
            max-height: 500px;
            background: var(--card);
            border: 1px solid #6366f1;
            border-radius: 16px;
            display: none;
            flex-direction: column;
            overflow: hidden;
            z-index: 999;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }
        .ai-panel.open { display: flex; }
        .ai-header {
            padding: 15px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .ai-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: rgba(255,255,255,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        .ai-name { font-weight: bold; font-size: 1rem; }
        .ai-status { font-size: 0.75rem; opacity: 0.8; }
        .ai-messages {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-height: 350px;
        }
        .ai-message {
            padding: 10px 14px;
            border-radius: 12px;
            max-width: 85%;
            font-size: 0.9rem;
            line-height: 1.4;
        }
        .ai-message.ai {
            background: rgba(99, 102, 241, 0.2);
            border: 1px solid rgba(99, 102, 241, 0.3);
            align-self: flex-start;
        }
        .ai-message.user {
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid rgba(0, 255, 136, 0.3);
            align-self: flex-end;
        }
        .ai-input-container {
            display: flex;
            padding: 10px;
            background: var(--bg);
            border-top: 1px solid var(--border);
            gap: 8px;
        }
        .ai-input {
            flex: 1;
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 10px 15px;
            color: var(--text);
            font-family: inherit;
            font-size: 0.9rem;
            outline: none;
        }
        .ai-input:focus { border-color: #6366f1; }
        .ai-send {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #6366f1;
            border: none;
            color: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .ai-suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            padding: 0 15px 10px;
        }
        .ai-suggestion {
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.3);
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.75rem;
            color: #a5b4fc;
            cursor: pointer;
            transition: all 0.2s;
        }
        .ai-suggestion:hover {
            background: rgba(99, 102, 241, 0.3);
        }

        /* AI Mode Toggle */
        .ai-mode-toggle {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 15px;
            background: var(--card);
            border-top: 1px solid var(--border);
        }
        .ai-mode-label { font-size: 0.8rem; color: var(--dim); }
        .ai-toggle {
            position: relative;
            width: 44px;
            height: 24px;
            background: var(--border);
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .ai-toggle.active { background: #6366f1; }
        .ai-toggle::after {
            content: '';
            position: absolute;
            top: 2px;
            left: 2px;
            width: 20px;
            height: 20px;
            background: white;
            border-radius: 50%;
            transition: all 0.3s;
        }
        .ai-toggle.active::after { left: 22px; }

        /* AI Narrator overlay */
        .narrator-text {
            background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.1), transparent);
            padding: 10px 15px;
            margin: 5px 0;
            border-left: 3px solid #6366f1;
            font-style: italic;
            color: #a5b4fc;
        }

        /* Mobile */
        @media (max-width: 600px) {
            #terminal { height: 300px; font-size: 13px; }
            .game-grid { grid-template-columns: 1fr; }
            .ai-panel { width: calc(100vw - 40px); bottom: 80px; }
            .ai-fab { width: 50px; height: 50px; font-size: 20px; }
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
            <div class="ai-mode-toggle">
                <span class="ai-mode-label">🤖 AI Enhanced Mode</span>
                <div class="ai-toggle" id="ai-mode-toggle" onclick="toggleAIMode()"></div>
                <span class="ai-mode-label" id="ai-mode-status">OFF</span>
            </div>
            <div class="input-container">
                <span class="prompt">&gt;</span>
                <input type="text" id="user-input" placeholder="Type command or natural language..." autocomplete="off" autofocus>
            </div>
        </div>

        <div class="games-section">
            <div class="section-title">🎮 Select a Game</div>
            <div class="game-grid" id="game-grid"></div>
        </div>
    </div>

    <!-- AI Assistant Panel -->
    <button class="ai-fab" id="ai-fab" onclick="toggleAIPanel()">🤖</button>
    <div class="ai-panel" id="ai-panel">
        <div class="ai-header">
            <div class="ai-avatar">🧠</div>
            <div>
                <div class="ai-name">ARIA - AI Assistant</div>
                <div class="ai-status">Adaptive Response Intelligence Agent</div>
            </div>
        </div>
        <div class="ai-messages" id="ai-messages">
            <div class="ai-message ai">Hello! I'm ARIA, your AI game assistant. I can help with hints, explain game mechanics, or just chat about strategy. What would you like to know?</div>
        </div>
        <div class="ai-suggestions" id="ai-suggestions">
            <span class="ai-suggestion" onclick="askAI('Give me a hint')">💡 Hint</span>
            <span class="ai-suggestion" onclick="askAI('Explain this game')">📖 Explain</span>
            <span class="ai-suggestion" onclick="askAI('What should I do?')">🎯 Strategy</span>
        </div>
        <div class="ai-input-container">
            <input type="text" class="ai-input" id="ai-input" placeholder="Ask ARIA anything..." onkeypress="if(event.key==='Enter')sendAIMessage()">
            <button class="ai-send" onclick="sendAIMessage()">➤</button>
        </div>
    </div>

    <script>
        let pyodide = null;
        let currentGame = null;
        let gameState = {};
        let aiModeEnabled = false;
        let conversationHistory = [];

        // ===== AI ASSISTANT (ARIA) =====
        const AI_KNOWLEDGE = {
            vault: {
                hints: [
                    "Keep a balance between exploring and resting. Exploration is risky but rewarding!",
                    "Trading is safe but costs caps. Build up reserves before spending on rooms.",
                    "Watch your food and water closely - starvation can spiral quickly.",
                    "New dwellers arrive randomly when you rest. More dwellers = more consumption.",
                    "The Med Bay and Power Generator are crucial rooms for long-term survival."
                ],
                explain: "VAULT 13 is a survival management game inspired by Fallout Shelter. You manage resources (food, water, power, caps) and dwellers in an underground vault. The goal is to survive as long as possible while growing your vault.",
                lore: "After the Great War, Vault-Tec built underground shelters. Vault 13 was designed for extended isolation. As Overseer, you must ensure your dwellers survive the wasteland's dangers.",
                strategy: "Focus on building essential rooms first. Keep 50+ caps as emergency reserve. Explore when you have 4+ dwellers. Trade when low on food/water."
            },
            echo: {
                hints: [
                    "Visit all 5 locations to fully explore the Temporal Nexus.",
                    "Paradoxes aren't failures - they're part of the experience!",
                    "Walking too far in any direction causes interesting reality shifts.",
                    "The timeline can shift when you move east or west beyond boundaries."
                ],
                explain: "Echo Chambers is a quantum exploration puzzle. You navigate through a space where time and causality work differently. Locations exist in superposition, and paradoxes reveal deeper truths about reality.",
                lore: "The Temporal Nexus exists outside normal spacetime. Here, all possible futures and pasts converge. Travelers report experiencing memories of events that never happened.",
                strategy: "Explore systematically. Each location reveals unique quantum phenomena. Embrace the paradoxes - they're the game's core experience."
            },
            chinese_room: {
                hints: [
                    "This is more philosophy than game - ponder each response carefully.",
                    "The 'think' command reveals insights about consciousness and AI.",
                    "You can perfectly respond without understanding - what does that mean?",
                    "Consider: if you pass the test, are you conscious?"
                ],
                explain: "Based on John Searle's famous thought experiment. You're in a room with a rulebook for Chinese. You can produce perfect Chinese responses without understanding the language. It questions whether AI can truly 'understand'.",
                lore: "Philosopher John Searle proposed this in 1980 to argue against Strong AI - the idea that a properly programmed computer literally has a mind.",
                strategy: "There's no 'winning' here. Engage with the philosophy. Consider what understanding really means."
            },
            trolley: {
                hints: [
                    "There's no 'right' answer - that's the point of moral dilemmas.",
                    "Utilitarian logic says maximize lives saved. But is it that simple?",
                    "Consider: is there a difference between killing and letting die?",
                    "Your stats reveal your ethical tendencies over time."
                ],
                explain: "The Trolley Problem is a famous ethical thought experiment. A trolley is heading toward people. You can divert it, saving them but killing someone else. It tests utilitarian vs deontological ethics.",
                lore: "Proposed by philosopher Philippa Foot in 1967, this dilemma has been debated for decades. Self-driving car developers use it to program ethical decision-making.",
                strategy: "Play multiple scenarios. Track your choices with 'stats'. Reflect on your ethical framework."
            },
            prisoners: {
                hints: [
                    "Tit-for-Tat is a strong strategy: cooperate first, then mirror opponent.",
                    "Always Defect wins short-term but loses in repeated games.",
                    "Watch the opponent's pattern - some strategies are predictable.",
                    "Mutual cooperation (3,3) beats mutual defection (1,1) over time."
                ],
                explain: "A classic game theory scenario. Two prisoners can cooperate (stay silent) or defect (betray). The best collective outcome requires trust, but individuals are tempted to defect.",
                lore: "Developed by RAND Corporation in 1950. It models how rational individuals might not cooperate even when it benefits everyone. Used in economics, politics, and evolutionary biology.",
                strategy: "Against Tit-for-Tat, cooperate. Against Always Defect, defect. Against Grudger, never defect first!"
            },
            monty: {
                hints: [
                    "Mathematically, switching wins 2/3 of the time!",
                    "Your initial pick has 1/3 chance. The other door has 2/3.",
                    "Monty's reveal gives you information - use it!",
                    "Play many games to see the statistics converge."
                ],
                explain: "Based on the game show Let's Make a Deal. Pick a door, Monty reveals a goat behind another, then you choose to switch or stay. Counter-intuitively, switching doubles your win rate!",
                lore: "This problem went viral in 1990 when Marilyn vos Savant published it. Even mathematicians argued against her correct answer. It's now a famous example of probability intuition failure.",
                strategy: "Always switch! Your initial 1/3 guess doesn't change, but the remaining door absorbs the 2/3 probability."
            }
        };

        // NLP Command Mapping
        const NLP_PATTERNS = {
            vault: {
                'check|show|view|see|what.*status|how.*doing': 'status',
                'make|create|construct|build|new room': 'build',
                'go out|venture|search|scavenge|explore|expedition': 'explore',
                'buy|sell|trade|merchant|shop': 'trade',
                'sleep|rest|next day|end|pass time|wait': 'rest',
                'help|commands|what can': 'help'
            },
            echo: {
                'look|see|observe|examine|where': 'look',
                'up|north|forward': 'north',
                'down|south|back': 'south',
                'right|east': 'east',
                'left|west': 'west',
                'touch|use|interact|activate': 'interact'
            },
            chinese_room: {
                'translate|read|interpret|lookup': 'translate',
                'respond|reply|answer|send': 'respond',
                'think|ponder|consider|reflect|contemplate': 'think',
                'examine|look|inspect|see': 'examine',
                'help|commands': 'help'
            },
            trolley: {
                'pull|switch|divert|save|lever': 'pull',
                'wait|nothing|don\\'t|stay|ignore': 'wait',
                'think|consider|ponder': 'think',
                'stats|score|history|record': 'stats'
            },
            prisoners: {
                'cooperate|trust|work together|coop|c$': 'cooperate',
                'defect|betray|cheat|d$': 'defect',
                'stats|score|points': 'stats',
                'opponent|who|enemy|other': 'opponent'
            },
            monty: {
                'pick 1|choose 1|door 1|first': 'pick 1',
                'pick 2|choose 2|door 2|second|middle': 'pick 2',
                'pick 3|choose 3|door 3|third|last': 'pick 3',
                'switch|change|other': 'switch',
                'stay|keep|same': 'stay',
                'stats|record|history': 'stats'
            }
        };

        // AI Narrator responses
        const NARRATOR_TEMPLATES = {
            vault: {
                build: ["The construction crew works through the night...", "Hammers echo through the vault corridors...", "A new chapter begins for Vault 13..."],
                explore: ["Your scouts disappear into the wasteland's haze...", "The vault door creaks open, revealing the blasted landscape...", "Geiger counters click as your team ventures forth..."],
                rest: ["The vault settles into quiet slumber...", "Another day in the underground haven passes...", "Dreams of the world above fill sleeping minds..."]
            },
            echo: {
                move: ["Reality shimmers as you step forward...", "The fabric of spacetime ripples around you...", "Quantum possibilities collapse into your new position..."],
                paradox: ["Time folds back on itself...", "You glimpse yourself from another timeline...", "Causality protests your presence here..."]
            },
            trolley: {
                pull: ["Your hand trembles on the lever...", "The weight of choice presses down...", "Steel screeches against steel as the track switches..."],
                wait: ["Your muscles freeze despite your racing thoughts...", "Time seems to slow as the trolley approaches...", "Inaction becomes its own form of choice..."]
            }
        };

        function toggleAIPanel() {
            const panel = document.getElementById('ai-panel');
            const fab = document.getElementById('ai-fab');
            panel.classList.toggle('open');
            fab.classList.toggle('active');
        }

        function toggleAIMode() {
            aiModeEnabled = !aiModeEnabled;
            const toggle = document.getElementById('ai-mode-toggle');
            const status = document.getElementById('ai-mode-status');
            toggle.classList.toggle('active', aiModeEnabled);
            status.textContent = aiModeEnabled ? 'ON' : 'OFF';

            if (aiModeEnabled) {
                addAIMessage("AI Enhanced Mode activated! I'll now provide dynamic narration and help interpret your natural language commands.", 'ai');
            }
        }

        function addAIMessage(text, type) {
            const messages = document.getElementById('ai-messages');
            const div = document.createElement('div');
            div.className = 'ai-message ' + type;
            div.textContent = text;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
            conversationHistory.push({role: type, content: text});
        }

        function askAI(query) {
            document.getElementById('ai-input').value = query;
            sendAIMessage();
        }

        function sendAIMessage() {
            const input = document.getElementById('ai-input');
            const message = input.value.trim();
            if (!message) return;

            addAIMessage(message, 'user');
            input.value = '';

            // Generate AI response
            setTimeout(() => {
                const response = generateAIResponse(message);
                addAIMessage(response, 'ai');
                updateSuggestions();
            }, 500 + Math.random() * 500);
        }

        function generateAIResponse(query) {
            const q = query.toLowerCase();
            const game = currentGame?.id || 'vault';
            const knowledge = AI_KNOWLEDGE[game];

            // Check for specific intents
            if (q.includes('hint') || q.includes('help me') || q.includes('stuck')) {
                return knowledge.hints[Math.floor(Math.random() * knowledge.hints.length)];
            }
            if (q.includes('explain') || q.includes('how') || q.includes('what is')) {
                return knowledge.explain;
            }
            if (q.includes('lore') || q.includes('story') || q.includes('background')) {
                return knowledge.lore;
            }
            if (q.includes('strategy') || q.includes('should i') || q.includes('best') || q.includes('what should')) {
                return knowledge.strategy;
            }
            if (q.includes('hello') || q.includes('hi ') || q.includes('hey')) {
                return "Hello, wanderer! I'm here to help you navigate " + (currentGame?.name || "these games") + ". Ask me for hints, strategy, or lore!";
            }

            // Dynamic game state analysis
            if (currentGame) {
                return analyzeGameState(game, q);
            }

            return "I'm your AI guide for VAULT 13's game collection. Select a game, and I can provide hints, explain mechanics, share lore, or suggest strategies. What interests you?";
        }

        function analyzeGameState(gameId, query) {
            const knowledge = AI_KNOWLEDGE[gameId];

            // Return a contextual hint based on game
            const hints = knowledge.hints;
            return hints[Math.floor(Math.random() * hints.length)] + " Would you like more specific guidance?";
        }

        function updateSuggestions() {
            const suggestions = document.getElementById('ai-suggestions');
            const game = currentGame?.id;

            if (game) {
                const gameSuggestions = {
                    vault: ['Resource tips', 'Building strategy', 'Exploration risks'],
                    echo: ['Paradox meaning', 'Timeline tips', 'Location guide'],
                    chinese_room: ['Philosophy insight', 'Searle\\'s argument', 'AI consciousness'],
                    trolley: ['Ethical theory', 'Utilitarian view', 'Why it matters'],
                    prisoners: ['Best strategy', 'Game theory', 'Opponent types'],
                    monty: ['Why switch?', 'Probability math', 'Common mistakes']
                };

                const items = gameSuggestions[game] || ['Hint', 'Explain', 'Strategy'];
                suggestions.innerHTML = items.map(s =>
                    `<span class="ai-suggestion" onclick="askAI('${s}')">${s}</span>`
                ).join('');
            }
        }

        // Natural Language Processing
        function parseNaturalLanguage(input, gameId) {
            const patterns = NLP_PATTERNS[gameId];
            if (!patterns) return input;

            const normalized = input.toLowerCase().trim();

            for (const [pattern, command] of Object.entries(patterns)) {
                const regex = new RegExp(pattern, 'i');
                if (regex.test(normalized)) {
                    return command;
                }
            }

            return input; // Return original if no match
        }

        // AI Narrator
        function getNarration(gameId, action) {
            const templates = NARRATOR_TEMPLATES[gameId];
            if (!templates || !templates[action]) return null;

            const options = templates[action];
            return options[Math.floor(Math.random() * options.length)];
        }

        function appendNarration(text) {
            const terminal = document.getElementById('terminal');
            const div = document.createElement('div');
            div.className = 'narrator-text';
            div.textContent = '✨ ' + text;
            terminal.appendChild(div);
            terminal.scrollTop = terminal.scrollHeight;
        }

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

# Define newline as variable to avoid escape issues
NL = chr(10)

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
                return f"✅ Built {new_room}! (-50 caps){NL}" + self.vault_status()
            return "❌ Not enough caps! Need 50."
        elif cmd == 'explore':
            if s['dwellers'] >= 3:
                found_caps = random.randint(20, 80)
                found_food = random.randint(5, 25)
                injury = random.random() < 0.3
                s['caps'] += found_caps
                s['food'] += found_food
                result = f"🗺️ Exploration complete!{NL}+{found_caps} caps, +{found_food} food"
                if injury:
                    s['dwellers'] -= 1
                    result += f"{NL}⚠️ One dweller was injured and couldn't return."
                return result + NL + self.vault_status()
            return "❌ Need at least 3 dwellers to explore!"
        elif cmd == 'trade':
            if s['caps'] >= 30:
                s['caps'] -= 30
                s['food'] += 20
                s['water'] += 20
                return f"💰 Traded 30 caps for supplies!{NL}+20 food, +20 water{NL}" + self.vault_status()
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
                event = f"{NL}🎉 {new_dwellers} new dweller(s) arrived!"
            elif event_roll < 0.3:
                s['happiness'] = min(100, s['happiness'] + 10)
                event = f"{NL}🎵 Dwellers threw a party! +10 happiness"

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
                result += NL + NL.join(warnings)
            return result + NL + self.vault_status()
        else:
            return f"Unknown command: {cmd}{NL}Type 'help' for commands."

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
                return "⚠️ PARADOX! You walked too far and looped back..." + NL + self.echo_look()
            return self.echo_look()
        elif cmd == 'south':
            self.state['y'] -= 1
            if abs(self.state['y']) > 1:
                self.state['y'] = 0
                self.state['paradoxes'] += 1
                return "⚠️ PARADOX! Space folded on itself..." + NL + self.echo_look()
            return self.echo_look()
        elif cmd == 'east':
            self.state['x'] += 1
            if abs(self.state['x']) > 1:
                self.state['x'] = 0
                self.state['timeline'] = random.choice(['Alpha', 'Beta', 'Gamma', 'Delta'])
                return f"🌀 Timeline shift! Now in Timeline {self.state['timeline']}{NL}" + self.echo_look()
            return self.echo_look()
        elif cmd == 'west':
            self.state['x'] -= 1
            if abs(self.state['x']) > 1:
                self.state['x'] = 0
                self.state['timeline'] = random.choice(['Alpha', 'Beta', 'Gamma', 'Delta'])
                return f"🌀 Timeline shift! Now in Timeline {self.state['timeline']}{NL}" + self.echo_look()
            return self.echo_look()
        elif cmd == 'interact':
            events = [
                "You touch a memory crystal. A vision of a choice not made fills your mind.",
                "An echo of yourself waves. You wave back. Which one is real?",
                "Time hiccups. For a moment, you experience tomorrow's memories.",
                "A quantum flower blooms and wilts in your hand simultaneously."
            ]
            self.state['paradoxes'] += 1
            return random.choice(events) + f"{NL}{NL}Paradoxes: {self.state['paradoxes']}"
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
            return f"Symbol: {symbol}{NL}Rulebook says: respond with '是' (yes){NL}{NL}But do you know what {symbol} means? ({meanings.get(symbol, '???')})"
        elif cmd == 'respond':
            s['correct'] += 1
            return f"You pass '是' through the slot.{NL}The person outside thinks you understand Chinese!{NL}{NL}Correct responses: {s['correct']}"
        elif cmd == 'think':
            s['understanding'] += 1
            thoughts = [
                "You follow rules perfectly, but comprehension eludes you.",
                "Is syntax without semantics truly understanding?",
                "The rulebook knows Chinese. Do you?",
                "You process symbols. Computers process data. What's the difference?",
                "Understanding seems to require something more than symbol manipulation..."
            ]
            return f"🤔 {random.choice(thoughts)}{NL}{NL}Times pondered: {s['understanding']}"
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
            result = f"🔀 You pulled the lever!{NL}{NL}"
            result += f"The trolley diverts. {c['side']} person dies.{NL}"
            result += f"But {c['main']} people are saved.{NL}{NL}"
            result += "You chose to ACT. You took responsibility for a death to save more lives."
            s['current'] = self.new_trolley_scenario()
            return result + f"{NL}{NL}--- Next scenario loading... ---{NL}" + self.show_trolley()
        elif cmd == 'wait':
            s['scenarios'] += 1
            s['sacrificed'] += c['main']
            result = f"⏳ You did nothing.{NL}{NL}"
            result += f"The trolley continues. {c['main']} people die.{NL}"
            result += f"The {c['side']} person on the side track lives.{NL}{NL}"
            result += "You chose INACTION. Some argue you're not responsible for deaths you didn't cause."
            s['current'] = self.new_trolley_scenario()
            return result + f"{NL}{NL}--- Next scenario loading... ---{NL}" + self.show_trolley()
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
        # Enhanced AI opponents with personalities
        opponents = [
            {'name': 'Tit-for-Tat', 'personality': 'The Mirror', 'desc': 'Starts kind, then copies your moves'},
            {'name': 'Always Defect', 'personality': 'The Betrayer', 'desc': 'Never trusts, always betrays'},
            {'name': 'Random', 'personality': 'The Chaos Agent', 'desc': 'Unpredictable and erratic'},
            {'name': 'Grudger', 'personality': 'The Elephant', 'desc': 'Cooperates until betrayed, then never forgives'},
            {'name': 'Pavlov', 'personality': 'The Learner', 'desc': 'Repeats successful moves'},
            {'name': 'Generous TFT', 'personality': 'The Forgiver', 'desc': 'Like Tit-for-Tat but occasionally forgives'},
            {'name': 'Suspicious TFT', 'personality': 'The Skeptic', 'desc': 'Defects first, then mirrors'},
            {'name': 'Adaptive', 'personality': 'The Analyst', 'desc': 'Learns your patterns and exploits them'}
        ]
        opp = random.choice(opponents)
        self.state = {
            'round': 1,
            'your_score': 0,
            'opp_score': 0,
            'history': [],
            'opponent': opp['name'],
            'opp_personality': opp['personality'],
            'opp_desc': opp['desc'],
            'last_outcome': None
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
            opp = s['opponent']

            if opp == 'Tit-for-Tat':
                # Cooperate first, then mirror opponent's last move
                return s['history'][-1][0] if s['history'] else 'C'

            elif opp == 'Always Defect':
                return 'D'

            elif opp == 'Grudger':
                # Cooperate until betrayed, then always defect
                return 'D' if any(h[0] == 'D' for h in s['history']) else 'C'

            elif opp == 'Pavlov':
                # Win-stay, lose-shift: repeat last move if it was successful
                if not s['history']:
                    return 'C'
                last_you, last_opp = s['history'][-1]
                # If last round was mutual cooperation or I defected and they cooperated
                if s['last_outcome'] in ['good', 'great']:
                    return s['history'][-1][1] if len(s['history']) > 0 else 'C'
                return 'D' if s['history'][-1][1] == 'C' else 'C'

            elif opp == 'Generous TFT':
                # Like TFT but forgives defection 10% of the time
                if not s['history']:
                    return 'C'
                if s['history'][-1][0] == 'D':
                    return 'C' if random.random() < 0.1 else 'D'
                return 'C'

            elif opp == 'Suspicious TFT':
                # Defects first, then mirrors
                if not s['history']:
                    return 'D'
                return s['history'][-1][0]

            elif opp == 'Adaptive':
                # Analyzes player's cooperation rate and exploits
                if len(s['history']) < 3:
                    return 'C'
                coop_rate = sum(1 for h in s['history'] if h[0] == 'C') / len(s['history'])
                # If player cooperates often, exploit them
                if coop_rate > 0.7:
                    return 'D'
                # If player defects often, defect back
                elif coop_rate < 0.3:
                    return 'D'
                # Otherwise mirror
                return s['history'][-1][0]

            else:  # Random
                return random.choice(['C', 'D'])

        if cmd in ['cooperate', 'c']:
            opp = get_opponent_move()
            if opp == 'C':
                s['your_score'] += 3
                s['opp_score'] += 3
                s['last_outcome'] = 'good'
                result = "🤝 Both cooperated! +3 each"
            else:
                s['opp_score'] += 5
                s['last_outcome'] = 'bad'
                result = "😔 You cooperated, they defected! You: +0, Them: +5"
            s['history'].append(('C', opp))
            s['round'] += 1
            return result + NL + self.show_prisoners()
        elif cmd in ['defect', 'd']:
            opp = get_opponent_move()
            if opp == 'C':
                s['your_score'] += 5
                s['last_outcome'] = 'great'
                result = "😈 You defected, they cooperated! You: +5, Them: +0"
            else:
                s['your_score'] += 1
                s['opp_score'] += 1
                s['last_outcome'] = 'poor'
                result = "💔 Both defected! +1 each"
            s['history'].append(('D', opp))
            s['round'] += 1
            return result + NL + self.show_prisoners()
        elif cmd == 'stats':
            coop_rate = sum(1 for h in s['history'] if h[0] == 'C') / max(1, len(s['history'])) * 100
            return f"""
📊 GAME STATISTICS
═══════════════════════
Round: {s['round']}
Your Score: {s['your_score']} pts
Opponent Score: {s['opp_score']} pts
Your Cooperation Rate: {coop_rate:.0f}%
Recent History: {s['history'][-5:]}
"""
        elif cmd == 'opponent':
            return f"""
🎭 OPPONENT PROFILE
═══════════════════════
Strategy: {s['opponent']}
Codename: {s['opp_personality']}
Behavior: {s['opp_desc']}

(Understanding your opponent is key to game theory!)
"""
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
            result = f"You switched to door {final}...{NL}{NL}"
            result += f"The car was behind door {s['prize_door']}!{NL}"
            result += "🎉 YOU WON!" if won else "😔 You got a goat."
            # Reset for next game
            s['prize_door'] = random.randint(1, 3)
            s['chosen'] = None
            s['revealed'] = None
            s['phase'] = 'choose'
            return result + f"{NL}{NL}Switch win rate: {s['wins_switch']}/{s['games']} ({100*s['wins_switch']//max(1,s['games'])}%){NL}{NL}" + self.show_monty()

        elif cmd == 'stay' and s['phase'] == 'switch':
            won = s['chosen'] == s['prize_door']
            s['games'] += 1
            if won:
                s['wins_stay'] += 1
            result = f"You stayed with door {s['chosen']}...{NL}{NL}"
            result += f"The car was behind door {s['prize_door']}!{NL}"
            result += "🎉 YOU WON!" if won else "😔 You got a goat."
            # Reset
            s['prize_door'] = random.randint(1, 3)
            s['chosen'] = None
            s['revealed'] = None
            s['phase'] = 'choose'
            return result + f"{NL}{NL}Stay win rate: {s['wins_stay']}/{s['games']} ({100*s['wins_stay']//max(1,s['games'])}%){NL}{NL}" + self.show_monty()

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

            let processedCmd = cmd;

            // AI Mode: Parse natural language
            if (aiModeEnabled) {
                processedCmd = parseNaturalLanguage(cmd, currentGame.id);
                if (processedCmd !== cmd) {
                    appendOutput('> ' + cmd + ' → [' + processedCmd + ']', 'input-line');
                } else {
                    appendOutput('> ' + cmd, 'input-line');
                }

                // Add narrator text before action
                const narrationAction = getNarrationAction(processedCmd, currentGame.id);
                if (narrationAction) {
                    const narration = getNarration(currentGame.id, narrationAction);
                    if (narration) {
                        appendNarration(narration);
                    }
                }
            } else {
                appendOutput('> ' + cmd, 'input-line');
            }

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
                    `game_engine.${cmdFuncs[currentGame.id]}("${processedCmd.replace(/"/g, '\\"')}")`
                );
                appendOutput(result);
            } catch (err) {
                appendOutput('Error: ' + err.message, 'error');
            }

            document.getElementById('user-input').value = '';
            document.getElementById('user-input').focus();
        }

        // Map commands to narrator actions
        function getNarrationAction(cmd, gameId) {
            const actionMaps = {
                vault: { build: 'build', explore: 'explore', rest: 'rest' },
                echo: { north: 'move', south: 'move', east: 'move', west: 'move' },
                trolley: { pull: 'pull', wait: 'wait' }
            };
            return actionMaps[gameId]?.[cmd];
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
