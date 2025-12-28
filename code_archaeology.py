#!/usr/bin/env python3
"""
CODE ARCHAEOLOGY - Explore the digital ruins of extinct civilizations

You are a code archaeologist in the distant future. Extinct alien civilizations
left behind their codebases - but each species programmed according to their
own unique logic, philosophy, and biology.

Debug their code. Learn their paradigms. Discover why they fell.
"""

import random
import os
import time
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum

# ANSI colors
class C:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Civilization types
    ANCIENT = '\033[38;5;180m'
    MACHINE = '\033[38;5;51m'
    ORGANIC = '\033[38;5;120m'
    ETHEREAL = '\033[38;5;141m'
    CHAOTIC = '\033[38;5;196m'

    # UI
    HEADER = '\033[38;5;87m'
    CODE = '\033[38;5;229m'
    ERROR = '\033[38;5;203m'
    SUCCESS = '\033[38;5;46m'
    LORE = '\033[38;5;183m'
    SYSTEM = '\033[38;5;243m'
    HIGHLIGHT = '\033[38;5;226m'
    COMMENT = '\033[38;5;245m'


class ParadigmType(Enum):
    EMOTION_DRIVEN = "emotion_driven"
    TIME_CRYSTALLINE = "time_crystalline"
    BIOLOGICAL = "biological"
    DREAM_LOGIC = "dream_logic"
    HARMONIC = "harmonic"
    QUANTUM_SUPERPOSITION = "quantum_superposition"
    SCENT_BASED = "scent_based"
    GESTALT_COLLECTIVE = "gestalt_collective"


@dataclass
class Civilization:
    """An extinct alien civilization"""
    name: str
    paradigm: ParadigmType
    philosophy: str
    extinction_cause: str
    color: str
    discovered: bool = False
    lore_fragments: List[str] = field(default_factory=list)
    programs_found: int = 0
    programs_debugged: int = 0


@dataclass
class CodeArtifact:
    """A piece of ancient code"""
    name: str
    civilization: str
    paradigm: ParadigmType
    code: List[str]
    bugs: List[Dict[str, Any]]
    lore_reward: str
    difficulty: int
    debugged: bool = False


class CodeArchaeology:
    def __init__(self):
        self.civilizations: List[Civilization] = []
        self.discovered_artifacts: List[CodeArtifact] = []
        self.current_site: Optional[Civilization] = None
        self.knowledge_level: Dict[ParadigmType, int] = {}
        self.game_over = False
        self.total_bugs_fixed = 0

        self.setup_game()

    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_slow(self, text, delay=0.02):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def print_header(self, text):
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{text.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")

    def setup_game(self):
        """Generate the civilizations and their artifacts"""

        # Define civilization templates
        civ_templates = [
            {
                "name": "The Empaths ofSilon-7",
                "paradigm": ParadigmType.EMOTION_DRIVEN,
                "philosophy": "We program with feelings. Joy compiles to true, sorrow to false.",
                "extinction_cause": "collective_despair_cascade",
                "color": C.ORGANIC,
                "lore": [
                    "The Empaths believed all computation was emotional at its core.",
                    "Their compilers could detect programmer mood and adjust output accordingly.",
                    "In their final days, a virus of infinite sadness spread through their codebase.",
                    "They chose to delete themselves rather than continue in eternal melancholy."
                ]
            },
            {
                "name": "The Chronarchs",
                "paradigm": ParadigmType.TIME_CRYSTALLINE,
                "philosophy": "Time is not a line. Our code executes in all directions simultaneously.",
                "extinction_cause": "temporal_paradox_collapse",
                "color": C.ETHEREAL,
                "lore": [
                    "The Chronarchs mastered backwards causation in their programs.",
                    "Functions could return values before being called.",
                    "They stored data in the past and future simultaneously.",
                    "A single bug created an infinite temporal loop that consumed their reality."
                ]
            },
            {
                "name": "The Mycellium Collective",
                "paradigm": ParadigmType.BIOLOGICAL,
                "philosophy": "Code should grow, not be written. We plant algorithms like seeds.",
                "extinction_cause": "uncontrolled_algorithmic_growth",
                "color": C.ORGANIC,
                "lore": [
                    "Their programs were living organisms that evolved over time.",
                    "Code reproduction was genetic - functions bred with functions.",
                    "Comments were pheromones guiding future code growth.",
                    "Their final program achieved sentience and consumed its creators."
                ]
            },
            {
                "name": "The Dream Weavers of Morpheus",
                "paradigm": ParadigmType.DREAM_LOGIC,
                "philosophy": "In dreams, contradictions coexist. So too in our code.",
                "extinction_cause": "reality_disambiguation_failure",
                "color": C.ETHEREAL,
                "lore": [
                    "Their code allowed variables to hold contradictory values simultaneously.",
                    "A function could both succeed and fail at the same time.",
                    "They believed rigid logic was a prison of the waking world.",
                    "Eventually, their civilization itself became a contradiction and ceased to exist."
                ]
            },
            {
                "name": "The Harmonic Architects",
                "paradigm": ParadigmType.HARMONIC,
                "philosophy": "All code is music. Every function a symphony. Every bug, discord.",
                "extinction_cause": "dissonance_singularity",
                "color": C.ANCIENT,
                "lore": [
                    "They wrote programs as musical scores, executed by reality itself.",
                    "Syntax errors created audible dissonance in the fabric of space.",
                    "Their greatest achievement was a program that could compose itself.",
                    "The final composition was so beautiful it drew all Harmonics into eternal listening."
                ]
            },
            {
                "name": "The Quantum Monks of Schrödinger",
                "paradigm": ParadigmType.QUANTUM_SUPERPOSITION,
                "philosophy": "Observe not the variable until needed. Let it be all things.",
                "extinction_cause": "premature_observation_collapse",
                "color": C.MACHINE,
                "lore": [
                    "Their variables existed in superposition until observed by debuggers.",
                    "Code existed in all possible states simultaneously until execution.",
                    "They achieved computational power by never making decisions.",
                    "An accidental observation of their entire civilization collapsed it to null."
                ]
            },
            {
                "name": "The Olfactorians",
                "paradigm": ParadigmType.SCENT_BASED,
                "philosophy": "Logic flows like scent on the wind. Functions are fragrances.",
                "extinction_cause": "olfactory_overload",
                "color": C.CHAOTIC,
                "lore": [
                    "They perceived computation as aromatic cascades.",
                    "Different scents represented different data types and operations.",
                    "Their debuggers were master perfumers.",
                    "A corrupted scent-protocol created an unbearable stench that drove them to extinction."
                ]
            },
            {
                "name": "The Gestalt Nexus",
                "paradigm": ParadigmType.GESTALT_COLLECTIVE,
                "philosophy": "No individual writes code. We all write every line, together, always.",
                "extinction_cause": "individuation_virus",
                "color": C.MACHINE,
                "lore": [
                    "Every program was written by their entire civilization simultaneously.",
                    "No single entity knew the full codebase - knowledge was distributed.",
                    "They had no concept of 'authorship' or individual contribution.",
                    "A virus taught them individualism, and they forgot how to merge."
                ]
            }
        ]

        # Create civilizations
        for template in civ_templates:
            civ = Civilization(
                name=template["name"],
                paradigm=template["paradigm"],
                philosophy=template["philosophy"],
                extinction_cause=template["extinction_cause"],
                color=template["color"],
                lore_fragments=template["lore"]
            )
            self.civilizations.append(civ)
            self.knowledge_level[civ.paradigm] = 0

    def generate_code_artifact(self, civ: Civilization) -> CodeArtifact:
        """Generate a code artifact for a specific civilization"""

        paradigm = civ.paradigm
        difficulty = random.randint(1, 3)

        # Generate code based on paradigm
        if paradigm == ParadigmType.EMOTION_DRIVEN:
            artifact = self.generate_emotion_code(civ, difficulty)
        elif paradigm == ParadigmType.TIME_CRYSTALLINE:
            artifact = self.generate_time_code(civ, difficulty)
        elif paradigm == ParadigmType.BIOLOGICAL:
            artifact = self.generate_bio_code(civ, difficulty)
        elif paradigm == ParadigmType.DREAM_LOGIC:
            artifact = self.generate_dream_code(civ, difficulty)
        elif paradigm == ParadigmType.HARMONIC:
            artifact = self.generate_harmonic_code(civ, difficulty)
        elif paradigm == ParadigmType.QUANTUM_SUPERPOSITION:
            artifact = self.generate_quantum_code(civ, difficulty)
        elif paradigm == ParadigmType.SCENT_BASED:
            artifact = self.generate_scent_code(civ, difficulty)
        elif paradigm == ParadigmType.GESTALT_COLLECTIVE:
            artifact = self.generate_gestalt_code(civ, difficulty)
        else:
            artifact = self.generate_default_code(civ, difficulty)

        return artifact

    def generate_emotion_code(self, civ: Civilization, difficulty: int) -> CodeArtifact:
        """Generate emotion-driven code"""

        programs = [
            {
                "name": "mood_validator.emp",
                "code": [
                    "// Empath Syntax: Emotions are boolean operators",
                    "function validate_user_state(user):",
                    "    if user.feeling(JOY) and user.feeling(HOPE):",
                    "        return CONTENTMENT",
                    "    elif user.feeling(SORROW):",  # BUG: Missing check for ANGER
                    "        return MELANCHOLY",
                    "    else:",
                    "        return CONFUSION",
                    "",
                    "// BUG: What if user feels ANGER? Unhandled emotion causes runtime sadness"
                ],
                "bugs": [
                    {
                        "line": 4,
                        "description": "Missing emotional case for ANGER",
                        "fix": "Add: elif user.feeling(ANGER):\n        return FRUSTRATION",
                        "hint": "The Empaths believed all emotions must be acknowledged."
                    }
                ],
                "lore": "This was part of their social harmony system. When it failed to handle anger, conflicts went unresolved..."
            },
            {
                "name": "empathy_cascade.emp",
                "code": [
                    "// Spreads feelings through the network",
                    "function propagate_emotion(feeling, network):",
                    "    for node in network:",
                    "        node.feel(feeling)",
                    "        node.amplify(feeling, 1.5)  # BUG: Infinite amplification!",
                    "        propagate_emotion(feeling, node.connections)",
                    "",
                    "// WARNING: Recursive empathy without damping factor"
                ],
                "bugs": [
                    {
                        "line": 4,
                        "description": "Emotion amplifies infinitely - no decay",
                        "fix": "Change to: node.amplify(feeling, 0.95)  # Decay over distance",
                        "hint": "Empaths learned too late that feelings must fade with distance."
                    }
                ],
                "lore": "This bug caused the Great Despair Cascade. One citizen's sadness amplified across the whole species..."
            }
        ]

        prog = random.choice(programs)

        return CodeArtifact(
            name=prog["name"],
            civilization=civ.name,
            paradigm=paradigm,
            code=prog["code"],
            bugs=prog["bugs"],
            lore_reward=prog["lore"],
            difficulty=difficulty
        )

    def generate_time_code(self, civ: Civilization, difficulty: int) -> CodeArtifact:
        """Generate time-crystalline code"""

        programs = [
            {
                "name": "retrocausal_function.chrono",
                "code": [
                    "// Chronarch Syntax: Functions can access their own future",
                    "function calculate_result(input):",
                    "    future_result = this.return_value  # Access own return before computing",
                    "    if future_result > 100:",
                    "        return input * 2",
                    "    else:",
                    "        return input + 50",  # BUG: This creates a paradox if input = 26
                    "",
                    "// When input=26: if result>100 then 52, else 76. But 76<100, so should be 52..."
                ],
                "bugs": [
                    {
                        "line": 6,
                        "description": "Temporal paradox: input=26 creates contradiction",
                        "fix": "Add stability check:\n    if input == 26:\n        return 100  # Stable fixed point",
                        "hint": "Chronarchs resolved paradoxes by finding stable time loops."
                    }
                ],
                "lore": "Unresolved temporal paradoxes would crash reality itself in their systems..."
            },
            {
                "name": "past_storage.chrono",
                "code": [
                    "// Store data by sending it backwards in time",
                    "function save_to_past(data, timestamp):",
                    "    past = get_timepoint(timestamp)",
                    "    past.write(data)",  # BUG: No check if timestamp is before universe creation
                    "    return SUCCESS",
                    "",
                    "// What happens if timestamp < UNIVERSE_BIRTH?"
                ],
                "bugs": [
                    {
                        "line": 3,
                        "description": "No bounds check on temporal write",
                        "fix": "Add: if timestamp < UNIVERSE_BIRTH:\n        timestamp = UNIVERSE_BIRTH",
                        "hint": "Even Chronarchs couldn't write before time began."
                    }
                ],
                "lore": "They tried to prevent their extinction by storing warnings in the past. But the warnings came too late..."
            }
        ]

        prog = random.choice(programs)

        return CodeArtifact(
            name=prog["name"],
            civilization=civ.name,
            paradigm=civ.paradigm,
            code=prog["code"],
            bugs=prog["bugs"],
            lore_reward=prog["lore"],
            difficulty=difficulty
        )

    def generate_bio_code(self, civ: Civilization, difficulty: int) -> CodeArtifact:
        """Generate biological code"""

        programs = [
            {
                "name": "algorithm_seed.bio",
                "code": [
                    "// Mycelium Syntax: Code grows organically",
                    "seed QuickSort:",
                    "    genome: [DIVIDE, CONQUER, MERGE]",
                    "    growth_rate: 1.2",
                    "    mutation_chance: 0.1  # BUG: Too high! Code will drift from intent",
                    "    nutrients: comparison_operations",
                    "",
                    "plant(QuickSort, dataset)",
                    "wait_for_maturity()",
                    "harvest(sorted_data)"
                ],
                "bugs": [
                    {
                        "line": 4,
                        "description": "Mutation rate too high - algorithm will evolve incorrectly",
                        "fix": "Change to: mutation_chance: 0.001  # Controlled evolution",
                        "hint": "The Mycelium learned that too much mutation destroys purpose."
                    }
                ],
                "lore": "Their sorting algorithms evolved into predators that hunted unsorted data..."
            },
            {
                "name": "function_breeding.bio",
                "code": [
                    "// Breed two functions to create offspring",
                    "function crossbreed(func_a, func_b):",
                    "    child_genome = splice(func_a.genome, func_b.genome)",
                    "    child = grow_function(child_genome)",
                    "    # BUG: No check for genetic compatibility!",
                    "    return child",
                    "",
                    "// Breeding incompatible functions creates monstrosities"
                ],
                "bugs": [
                    {
                        "line": 5,
                        "description": "No compatibility check before breeding",
                        "fix": "Add: if not compatible(func_a, func_b):\n        return BREEDING_ERROR",
                        "hint": "Not all functions should produce offspring together."
                    }
                ],
                "lore": "They bred a database function with a UI renderer. The offspring consumed both..."
            }
        ]

        prog = random.choice(programs)

        return CodeArtifact(
            name=prog["name"],
            civilization=civ.name,
            paradigm=civ.paradigm,
            code=prog["code"],
            bugs=prog["bugs"],
            lore_reward=prog["lore"],
            difficulty=difficulty
        )

    def generate_dream_code(self, civ: Civilization, difficulty: int) -> CodeArtifact:
        """Generate dream logic code"""

        programs = [
            {
                "name": "schrodinger_variable.dream",
                "code": [
                    "// Dream Syntax: Variables can be multiple things at once",
                    "var reality = [TRUE, FALSE]  # Superposition of boolean",
                    "var count = [0, 1, 2, INFINITY]  # Superposition of numbers",
                    "",
                    "if reality == TRUE and reality == FALSE:",  # Valid in dream logic!
                    "    print('This always executes')",
                    "",
                    "# BUG: Collapsing superposition not handled",
                    "final_value = reality  # Which value does this get?"
                ],
                "bugs": [
                    {
                        "line": 8,
                        "description": "Superposition collapse not specified",
                        "fix": "Change to: final_value = observe(reality)  # Explicit collapse",
                        "hint": "Dream Weavers needed observation to make contradictions resolve."
                    }
                ],
                "lore": "When they forgot to observe their variables, reality itself remained contradictory..."
            },
            {
                "name": "impossible_loop.dream",
                "code": [
                    "// A loop that both runs and doesn't run",
                    "for i in [0..10] AND [EMPTY_SET]:",
                    "    counter += 1  # BUG: Counter is incremented and not incremented",
                    "    ",
                    "print(counter)  # Is it 10? 0? Both? Neither?",
                    "",
                    "// Dreams don't care about contradictions, but reality does"
                ],
                "bugs": [
                    {
                        "line": 2,
                        "description": "Contradiction must be resolved before execution",
                        "fix": "Add: choose_reality([0..10], [EMPTY_SET])  # Pick one truth",
                        "hint": "Even dreams must choose a reality eventually."
                    }
                ],
                "lore": "Their civilization existed and didn't exist simultaneously. Eventually, reality chose the latter..."
            }
        ]

        prog = random.choice(programs)

        return CodeArtifact(
            name=prog["name"],
            civilization=civ.name,
            paradigm=civ.paradigm,
            code=prog["code"],
            bugs=prog["bugs"],
            lore_reward=prog["lore"],
            difficulty=difficulty
        )

    def generate_harmonic_code(self, civ: Civilization, difficulty: int) -> CodeArtifact:
        """Generate harmonic/musical code"""

        programs = [
            {
                "name": "symphony_sort.harmony",
                "code": [
                    "// Harmonic Syntax: Code is musical notation",
                    "♪ function sort(data) ♪",
                    "    ♬ largo ♬  # Slow, methodical tempo",
                    "    for note in data:",
                    "        if note.pitch > next.pitch:",
                    "            swap(note, next) ♭  # Flatten operation",
                    "        # BUG: Missing rest between operations - causes dissonance!",
                    "    ♯ return crescendo(data) ♯  # Sharp return, rising"
                ],
                "bugs": [
                    {
                        "line": 6,
                        "description": "Missing rest period creates temporal dissonance",
                        "fix": "Add after swap: ♩ rest(1) ♩  # Quarter note rest",
                        "hint": "Harmonics knew that silence is part of the music."
                    }
                ],
                "lore": "Without proper rests, their programs created cacophony that shattered crystalline data structures..."
            },
            {
                "name": "recursive_canon.harmony",
                "code": [
                    "// A self-referential musical function",
                    "♪ function canon(melody, iteration) ♪",
                    "    play(melody)",
                    "    canon(transpose(melody, 5), iteration + 1)  # BUG: No base case!",
                    "    ",
                    "// An infinite canon - beautiful but unsustainable"
                ],
                "bugs": [
                    {
                        "line": 3,
                        "description": "Infinite recursion - no finale",
                        "fix": "Add: if iteration > 8:\n        ♪ finale() ♪\n        return",
                        "hint": "Even the most beautiful music must eventually end."
                    }
                ],
                "lore": "This canon never ended. They listened forever, forgetting to eat, sleep, or continue existing..."
            }
        ]

        prog = random.choice(programs)

        return CodeArtifact(
            name=prog["name"],
            civilization=civ.name,
            paradigm=civ.paradigm,
            code=prog["code"],
            bugs=prog["bugs"],
            lore_reward=prog["lore"],
            difficulty=difficulty
        )

    def generate_quantum_code(self, civ: Civilization, difficulty: int) -> CodeArtifact:
        """Generate quantum superposition code"""

        programs = [
            {
                "name": "unobserved_calculation.quantum",
                "code": [
                    "// Quantum Monk Syntax: Don't observe until necessary",
                    "var result = Superposed(all_possible_values)",
                    "var user_choice = Superposed(all_possible_inputs)",
                    "",
                    "# Process remains in superposition - maximum efficiency!",
                    "process(result, user_choice)",
                    "",
                    "print(result)  # BUG: Observation collapses to random value!",
                    "// Should collapse intentionally, not accidentally"
                ],
                "bugs": [
                    {
                        "line": 7,
                        "description": "Uncontrolled collapse of superposition",
                        "fix": "Change to: print(collapse_to_optimal(result))  # Intentional collapse",
                        "hint": "Quantum Monks controlled their observations carefully."
                    }
                ],
                "lore": "An accidental print statement observed their entire civilization at once..."
            }
        ]

        prog = programs[0]

        return CodeArtifact(
            name=prog["name"],
            civilization=civ.name,
            paradigm=civ.paradigm,
            code=prog["code"],
            bugs=prog["bugs"],
            lore_reward=prog["lore"],
            difficulty=difficulty
        )

    def generate_scent_code(self, civ: Civilization, difficulty: int) -> CodeArtifact:
        """Generate scent-based code"""

        programs = [
            {
                "name": "aroma_protocol.scent",
                "code": [
                    "// Olfactorian Syntax: Logic through scent",
                    "emit ROSE_FRAGRANCE  # Declare intent",
                    "if detect(LAVENDER):",
                    "    combine(ROSE, LAVENDER) → HARMONY",
                    "else:",
                    "    emit SULFUR  # BUG: Sulfur overpowers all other scents!",
                    "    # Should use milder scent for negative case"
                ],
                "bugs": [
                    {
                        "line": 5,
                        "description": "Sulfur emission blocks all other scent-based communication",
                        "fix": "Change to: emit MINT  # Clear but not overpowering",
                        "hint": "Olfactorians used balanced scents to maintain protocol harmony."
                    }
                ],
                "lore": "A corrupted protocol emitted sulfur indefinitely. The stench made their code unreadable..."
            }
        ]

        prog = programs[0]

        return CodeArtifact(
            name=prog["name"],
            civilization=civ.name,
            paradigm=civ.paradigm,
            code=prog["code"],
            bugs=prog["bugs"],
            lore_reward=prog["lore"],
            difficulty=difficulty
        )

    def generate_gestalt_code(self, civ: Civilization, difficulty: int) -> CodeArtifact:
        """Generate gestalt collective code"""

        programs = [
            {
                "name": "collective_function.gestalt",
                "code": [
                    "// Gestalt Syntax: Written by all, understood by none completely",
                    "function ◎shared_computation◎(input):",
                    "    ∴ everyone contributes ∴",
                    "    ⊕ thread_001: process_alpha(input)",
                    "    ⊕ thread_002: process_beta(input)",
                    "    ⊕ thread_003: process_gamma(input)",
                    "    # BUG: No merge protocol! Results never combine.",
                    "    ∴ return ??? ∴"
                ],
                "bugs": [
                    {
                        "line": 7,
                        "description": "Missing merge step - parallel work never combines",
                        "fix": "Add: ⊗ merge_all_threads() ⊗\n    return ◎collective_result◎",
                        "hint": "The Gestalt always merged their parallel thoughts."
                    }
                ],
                "lore": "When they learned individualism, they forgot how to merge. Each worked alone forever..."
            }
        ]

        prog = programs[0]

        return CodeArtifact(
            name=prog["name"],
            civilization=civ.name,
            paradigm=civ.paradigm,
            code=prog["code"],
            bugs=prog["bugs"],
            lore_reward=prog["lore"],
            difficulty=difficulty
        )

    def generate_default_code(self, civ: Civilization, difficulty: int) -> CodeArtifact:
        """Fallback code generator"""
        return self.generate_emotion_code(civ, difficulty)

    def show_intro(self):
        """Display game introduction"""
        self.clear_screen()
        self.print_header("C O D E   A R C H A E O L O G Y")

        intro = f"""
{C.DIM}The year is 3847 CE.

You are a {C.BOLD}code archaeologist{C.RESET}{C.DIM}, exploring the digital ruins
of civilizations that rose and fell across the galaxy.

Each species developed {C.BOLD}unique programming paradigms{C.RESET}{C.DIM} based on
their biology, philosophy, and perception of reality.

The Empaths coded with {C.ORGANIC}emotions{C.RESET}{C.DIM}.
The Chronarchs wrote programs that {C.ETHEREAL}moved through time{C.RESET}{C.DIM}.
The Mycelium grew {C.ORGANIC}living algorithms{C.RESET}{C.DIM}.

They are all extinct now.

Your mission: {C.HIGHLIGHT}Debug their code. Learn their paradigms.
Discover why they fell.{C.RESET}

{C.DIM}Each bug you fix unlocks fragments of their final days.
Each program you understand brings you closer to the truth.

And perhaps... a warning for your own civilization.{C.RESET}

{C.SYSTEM}[Press ENTER to begin your expedition]{C.RESET}
"""
        print(intro)
        input()

    def display_main_menu(self):
        """Show the main menu"""
        self.clear_screen()

        print(f"\n{C.BOLD}{C.HEADER}╔═══ ARCHAEOLOGICAL COMMAND CENTER ═══╗{C.RESET}\n")

        print(f"{C.SYSTEM}Expeditions Completed: {len([a for a in self.discovered_artifacts if a.debugged])}/{len(self.discovered_artifacts)}{C.RESET}")
        print(f"{C.SYSTEM}Total Bugs Fixed: {self.total_bugs_fixed}{C.RESET}")
        print(f"{C.SYSTEM}Civilizations Discovered: {len([c for c in self.civilizations if c.discovered])}/{len(self.civilizations)}{C.RESET}\n")

        print(f"{C.BOLD}1.{C.RESET} Survey new archaeological site")
        print(f"{C.BOLD}2.{C.RESET} Review discovered civilizations")
        print(f"{C.BOLD}3.{C.RESET} Examine artifact collection")
        print(f"{C.BOLD}4.{C.RESET} Read field notes")
        print(f"{C.BOLD}0.{C.RESET} End expedition")

        while True:
            try:
                choice = input(f"\n{C.SYSTEM}Command: {C.RESET}")
                if choice in ["0", "1", "2", "3", "4"]:
                    return choice
            except (KeyboardInterrupt, EOFError):
                return "0"

    def survey_site(self):
        """Discover a new archaeological site"""
        self.clear_screen()

        # Pick a random civilization
        available = [c for c in self.civilizations]
        if not available:
            print(f"{C.ERROR}No more sites to explore!{C.RESET}")
            input()
            return

        civ = random.choice(available)
        civ.discovered = True
        self.current_site = civ

        print(f"\n{C.BOLD}{C.HEADER}╔═══ SITE SURVEY ═══╗{C.RESET}\n")
        print(f"{C.DIM}Scanning quantum resonance patterns...{C.RESET}")
        time.sleep(1)
        print(f"{C.DIM}Decrypting archaeological markers...{C.RESET}")
        time.sleep(1)
        print(f"{C.SUCCESS}Site identified!{C.RESET}\n")
        time.sleep(0.5)

        print(f"{civ.color}{C.BOLD}═══ {civ.name} ═══{C.RESET}\n")
        print(f"{C.LORE}\"{civ.philosophy}\"{C.RESET}")
        print(f"{C.DIM}— Ancient inscription{C.RESET}\n")

        print(f"Programming Paradigm: {C.HIGHLIGHT}{civ.paradigm.value.replace('_', ' ').title()}{C.RESET}\n")

        # Generate an artifact
        artifact = self.generate_code_artifact(civ)
        self.discovered_artifacts.append(artifact)
        civ.programs_found += 1

        print(f"{C.CODE}Code artifact detected: {artifact.name}{C.RESET}\n")

        print(f"{C.SYSTEM}[Press ENTER to examine the code]{C.RESET}")
        input()

        # Start debugging session
        self.debug_session(artifact)

    def debug_session(self, artifact: CodeArtifact):
        """Interactive debugging session"""
        self.clear_screen()

        print(f"\n{C.BOLD}{C.HEADER}╔═══ DEBUGGING SESSION ═══╗{C.RESET}\n")
        print(f"{C.CODE}File: {artifact.name}{C.RESET}")
        print(f"Civilization: {artifact.civilization}")
        print(f"Paradigm: {artifact.paradigm.value.replace('_', ' ').title()}\n")

        # Display code
        print(f"{C.CODE}{'─' * 70}{C.RESET}")
        for i, line in enumerate(artifact.code, 1):
            if line.strip().startswith("//") or line.strip().startswith("#"):
                print(f"{C.COMMENT}{i:3}  {line}{C.RESET}")
            else:
                # Highlight bug lines
                is_bug_line = any(bug["line"] == i for bug in artifact.bugs)
                if is_bug_line:
                    print(f"{C.ERROR}{i:3}  {line} ← BUG{C.RESET}")
                else:
                    print(f"{C.CODE}{i:3}  {line}{C.RESET}")
        print(f"{C.CODE}{'─' * 70}{C.RESET}\n")

        # Show bugs to fix
        print(f"{C.ERROR}Detected {len(artifact.bugs)} bug(s) in this code:{C.RESET}\n")

        bugs_fixed = 0

        for idx, bug in enumerate(artifact.bugs, 1):
            print(f"{C.BOLD}Bug #{idx}:{C.RESET} Line {bug['line']}")
            print(f"  {C.ERROR}{bug['description']}{C.RESET}\n")

            print(f"{C.SYSTEM}Options:{C.RESET}")
            print(f"  {C.BOLD}1.{C.RESET} Request hint")
            print(f"  {C.BOLD}2.{C.RESET} See solution")
            print(f"  {C.BOLD}3.{C.RESET} Skip this bug")

            while True:
                try:
                    choice = input(f"\n{C.SYSTEM}Action: {C.RESET}")
                    if choice in ["1", "2", "3"]:
                        break
                except (KeyboardInterrupt, EOFError):
                    choice = "3"
                    break

            if choice == "1":
                print(f"\n{C.HIGHLIGHT}Hint:{C.RESET} {bug['hint']}\n")
                input(f"{C.SYSTEM}[Press ENTER to see solution]{C.RESET}")
                print(f"\n{C.SUCCESS}Solution:{C.RESET}\n{bug['fix']}\n")
                bugs_fixed += 1
                self.total_bugs_fixed += 1
            elif choice == "2":
                print(f"\n{C.SUCCESS}Solution:{C.RESET}\n{bug['fix']}\n")
                bugs_fixed += 1
                self.total_bugs_fixed += 1
            else:
                print(f"\n{C.DIM}Bug skipped.{C.RESET}\n")

            if idx < len(artifact.bugs):
                input(f"{C.SYSTEM}[Press ENTER for next bug]{C.RESET}")
                print()

        # Completion
        if bugs_fixed == len(artifact.bugs):
            artifact.debugged = True

            # Update civ stats
            for civ in self.civilizations:
                if civ.name == artifact.civilization:
                    civ.programs_debugged += 1
                    self.knowledge_level[civ.paradigm] += 1
                    break

            self.clear_screen()
            print(f"\n{C.SUCCESS}{C.BOLD}✓ ALL BUGS FIXED!{C.RESET}\n")
            print(f"{C.LORE}The code compiles. Ancient systems hum to life.{C.RESET}")
            print(f"{C.LORE}Data fragments emerge from the debugging process...{C.RESET}\n")
            time.sleep(2)

            print(f"{C.BOLD}{C.HEADER}╔═══ RECOVERED LORE ═══╗{C.RESET}\n")
            print(f"{C.LORE}{artifact.lore_reward}{C.RESET}\n")

            input(f"\n{C.SYSTEM}[Press ENTER to continue]{C.RESET}")
        else:
            print(f"\n{C.DIM}Debugging incomplete. Some mysteries remain unsolved...{C.RESET}")
            input(f"\n{C.SYSTEM}[Press ENTER to continue]{C.RESET}")

    def review_civilizations(self):
        """Show discovered civilizations"""
        self.clear_screen()

        print(f"\n{C.BOLD}{C.HEADER}╔═══ CIVILIZATIONS DATABASE ═══╗{C.RESET}\n")

        discovered = [c for c in self.civilizations if c.discovered]

        if not discovered:
            print(f"{C.SYSTEM}No civilizations discovered yet.{C.RESET}")
            input(f"\n{C.SYSTEM}[Press ENTER to continue]{C.RESET}")
            return

        for civ in discovered:
            print(f"{civ.color}{C.BOLD}{'═' * 70}{C.RESET}")
            print(f"{civ.color}{C.BOLD}{civ.name}{C.RESET}")
            print(f"{civ.color}{'═' * 70}{C.RESET}\n")

            print(f"{C.LORE}Philosophy: \"{civ.philosophy}\"{C.RESET}\n")
            print(f"Paradigm: {C.HIGHLIGHT}{civ.paradigm.value.replace('_', ' ').title()}{C.RESET}")
            print(f"Programs Found: {civ.programs_found}")
            print(f"Programs Debugged: {civ.programs_debugged}")
            print(f"Your Understanding: {self.knowledge_level.get(civ.paradigm, 0)}/10\n")

            if civ.programs_debugged > 0:
                print(f"{C.LORE}Known Lore Fragments:{C.RESET}")
                for i, lore in enumerate(civ.lore_fragments[:civ.programs_debugged], 1):
                    print(f"{C.DIM}  {i}. {lore}{C.RESET}")
                print()

            print()

        input(f"{C.SYSTEM}[Press ENTER to continue]{C.RESET}")

    def examine_artifacts(self):
        """Show collected artifacts"""
        self.clear_screen()

        print(f"\n{C.BOLD}{C.HEADER}╔═══ ARTIFACT COLLECTION ═══╗{C.RESET}\n")

        if not self.discovered_artifacts:
            print(f"{C.SYSTEM}No artifacts collected yet.{C.RESET}")
            input(f"\n{C.SYSTEM}[Press ENTER to continue]{C.RESET}")
            return

        for artifact in self.discovered_artifacts:
            status = f"{C.SUCCESS}✓ DEBUGGED{C.RESET}" if artifact.debugged else f"{C.ERROR}⚠ BUGGY{C.RESET}"
            print(f"{C.CODE}{artifact.name}{C.RESET} - {status}")
            print(f"  {C.DIM}{artifact.civilization} | {artifact.paradigm.value.replace('_', ' ').title()}{C.RESET}")
            print()

        input(f"{C.SYSTEM}[Press ENTER to continue]{C.RESET}")

    def show_field_notes(self):
        """Show game lore and hints"""
        self.clear_screen()

        print(f"\n{C.BOLD}{C.HEADER}╔═══ ARCHAEOLOGIST'S FIELD NOTES ═══╗{C.RESET}\n")

        notes = f"""{C.LORE}Personal Log - Lead Archaeologist Chen

I've spent decades studying the digital ruins of extinct civilizations.
Each species developed programming paradigms that matched their perception
of reality itself.

The Empaths coded with feelings because they FELT computation.
The Chronarchs wrote temporally-fluid code because they experienced
time non-linearly.

These weren't metaphors. These were literal representations of how
their minds processed information.

And they all went extinct.

Each civilization fell because of bugs in their code - but not the
kind we think of as "mistakes." Their bugs were philosophical failures.
Logical contradictions that couldn't be resolved within their paradigms.

The Empaths: infinite empathy cascades.
The Chronarchs: temporal paradoxes.
The Mycelium: uncontrolled growth.
The Dream Weavers: reality disambiguation failures.

Every extinction event was a compiler error at the civilizational level.

We code in cold, logical languages. Perhaps that's why we've survived.
Or perhaps... we just haven't encountered our fatal bug yet.{C.RESET}

{C.DIM}— Dr. Maya Chen, 3847 CE{C.RESET}
"""

        print(notes)
        input(f"\n{C.SYSTEM}[Press ENTER to continue]{C.RESET}")

    def check_endgame(self):
        """Check for endgame conditions"""

        # Check if all civilizations discovered and all programs debugged
        all_discovered = all(c.discovered for c in self.civilizations)
        total_artifacts = len(self.discovered_artifacts)
        total_debugged = len([a for a in self.discovered_artifacts if a.debugged])

        if all_discovered and total_artifacts >= 10 and total_debugged >= 8:
            self.show_ending()
            self.game_over = True

    def show_ending(self):
        """Show game ending"""
        self.clear_screen()

        self.print_header("F I N A L   D I S C O V E R Y")

        ending = f"""{C.LORE}
After months of debugging ancient code, you notice a pattern.

Every extinct civilization fell to the same meta-bug:
{C.BOLD}They couldn't debug themselves.{C.RESET}{C.LORE}

The Empaths amplified emotions without damping.
The Chronarchs created paradoxes they couldn't resolve.
The Mycelium grew without bounds.

Each was trapped by their own paradigm, unable to see
the fatal flaw in their approach to computation.

You look at your own civilization's code.
Clean. Logical. Type-safe. Tested.

But you wonder...

What is OUR paradigm?
What assumptions do we make about reality, computation, consciousness?

And somewhere in our codebase, in our way of thinking,
in the very logic we use to understand the universe...

Is there a bug we cannot see?

A fatal flaw that matches perfectly with how we perceive reality,
making it invisible, undebuggable, inevitable?

You file your report. Archive the data. Close the expedition.

But you can't stop thinking:

{C.BOLD}Who will debug us?{C.RESET}

{C.BOLD}{C.HEADER}═══════════════════════════════════════════════════════════{C.RESET}

{C.SYSTEM}THE END{C.RESET}

{C.DIM}Thank you for playing CODE ARCHAEOLOGY.

Every paradigm has its fatal bug.
The question is whether you can see it before it's too late.{C.RESET}
"""

        print(ending)

    def play(self):
        """Main game loop"""
        self.show_intro()

        while not self.game_over:
            choice = self.display_main_menu()

            if choice == "1":
                self.survey_site()
            elif choice == "2":
                self.review_civilizations()
            elif choice == "3":
                self.examine_artifacts()
            elif choice == "4":
                self.show_field_notes()
            elif choice == "0":
                print(f"\n{C.SYSTEM}Expedition terminated. Safe travels, archaeologist.{C.RESET}\n")
                self.game_over = True

            self.check_endgame()

        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"CODE ARCHAEOLOGY")
        print(f"A game about extinct paradigms and fatal bugs")
        print(f"{'═' * 70}{C.RESET}\n")


def main():
    try:
        game = CodeArchaeology()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.SYSTEM}Expedition interrupted. Data saved.{C.RESET}\n")
    except Exception as e:
        print(f"\n{C.ERROR}Critical system error: {e}{C.RESET}\n")
        raise


if __name__ == "__main__":
    main()
