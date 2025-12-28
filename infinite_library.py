#!/usr/bin/env python3
"""
THE INFINITE LIBRARY

Based on Jorge Luis Borges' "The Library of Babel" - but you can explore it.

In this library exists every book that has ever been or could ever be written.
Every possible combination of letters forms a book somewhere in these halls.

Your autobiography is here. Your obituary. False histories. True prophecies.
Contradictions. Revelations. Nonsense and profound truth, indistinguishable.

Navigate the hexagonal rooms. Search for meaning. Find yourself.
Or lose yourself in infinity.
"""

import random
import hashlib
import time
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

from platform_utils import clear_screen
from colors import C


@dataclass
class Book:
    """A book in the infinite library"""
    title: str
    hex_room: str
    wall: int
    shelf: int
    position: int
    seed: str
    pages: int = 410
    lines_per_page: int = 40
    chars_per_line: int = 80
    is_special: bool = False
    special_type: Optional[str] = None


@dataclass
class HexRoom:
    """A hexagonal room in the library"""
    coordinate: str  # "0,0,0" in hex coordinates
    seed: str
    books_per_wall: int = 5
    shelves_per_wall: int = 5
    walls: int = 4  # 4 walls with books, 2 for passages


@dataclass
class SearchResult:
    """Result of searching for text in the library"""
    query: str
    book: Book
    page: int
    line: int
    context: List[str]


class InfiniteLibrary:
    def __init__(self):
        self.current_room = "0,0,0"
        self.visited_rooms: set = {"0,0,0"}
        self.found_books: List[Book] = []
        self.prophecies_found: List[str] = []
        self.user_name: str = ""
        self.steps_taken = 0
        self.searches_made = 0
        self.game_over = False

        # Borges-approved alphabet (Spanish + space, comma, period)
        self.alphabet = " abcdefghijklmnopqrstuvwxyz.,"

        self.setup_game()

    def clear_screen(self):
        clear_screen()

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
        """Initialize the game"""
        pass  # The library needs no setup - it already contains everything

    def show_intro(self):
        """Display the introduction"""
        self.clear_screen()
        self.print_header("T H E   I N F I N I T E   L I B R A R Y")

        intro = f"""{C.DIM}
"The universe (which others call the Library) is composed of an indefinite,
perhaps infinite number of hexagonal galleries..."

— Jorge Luis Borges, "The Library of Babel"

{C.RESET}You stand in a hexagonal room. Four walls are lined with shelves.
Each shelf contains exactly {C.BOLD}32 books{C.RESET}.
Each book contains exactly {C.BOLD}410 pages{C.RESET}.

The books contain every possible combination of letters.

Which means:

• Your biography is here. {C.DIM}(It may be on a shelf to your left.){C.RESET}
• The cure for every disease is catalogued. {C.DIM}(Along with false cures.){C.RESET}
• Future histories. {C.DIM}(And countless false futures.){C.RESET}
• This exact conversation, recorded perfectly. {C.DIM}(And millions of variations.){C.RESET}
• Pure nonsense, indistinguishable from truth.

The library is {C.BOLD}infinite{C.RESET}.

{C.HIGHLIGHT}Navigate.{C.RESET} Rooms connect in all directions.
{C.HIGHLIGHT}Search.{C.RESET} Find books containing any phrase you seek.
{C.HIGHLIGHT}Read.{C.RESET} But remember: for every truth, there are infinite lies.

{C.DIM}The library is infinite. You are finite.
What will you seek in these endless halls?{C.RESET}

{C.SYSTEM}[Press ENTER to begin]{C.RESET}
"""
        print(intro)
        input()

        # Get player name
        self.clear_screen()
        print(f"\n{C.BOOK}Before you begin, the library asks:{C.RESET}\n")
        while True:
            self.user_name = input(f"{C.SYSTEM}What is your name? {C.RESET}").strip()
            if self.user_name:
                break

        print(f"\n{C.SPECIAL}Welcome, {self.user_name}.{C.RESET}")
        print(f"{C.DIM}Somewhere in these halls is a book that tells your story.{C.RESET}")
        print(f"{C.DIM}But which version is true?{C.RESET}\n")

        time.sleep(2)

    def generate_room_seed(self, coordinate: str) -> str:
        """Generate deterministic seed for a room"""
        return hashlib.md5(f"library_room_{coordinate}".encode()).hexdigest()

    def get_hex_coordinates(self, coord_str: str, direction: int) -> str:
        """Get neighboring hex coordinate. Direction 0-5."""
        x, y, z = map(int, coord_str.split(','))

        # Cube coordinates for hexagonal grid
        moves = [
            (1, -1, 0),   # 0: E
            (1, 0, -1),   # 1: NE
            (0, 1, -1),   # 2: NW
            (-1, 1, 0),   # 3: W
            (-1, 0, 1),   # 4: SW
            (0, -1, 1),   # 5: SE
        ]

        if 0 <= direction < 6:
            dx, dy, dz = moves[direction]
            return f"{x+dx},{y+dy},{z+dz}"

        return coord_str

    def generate_book_content(self, book: Book, page: int, line: int) -> str:
        """Generate a specific line from a specific page deterministically"""

        # Deterministic randomness based on book seed + page + line
        seed_str = f"{book.seed}_p{page}_l{line}"
        seed_hash = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)

        random.seed(seed_hash)

        # Generate line of text
        line_text = ''.join(random.choice(self.alphabet)
                           for _ in range(book.chars_per_line))

        random.seed()  # Reset randomness
        return line_text

    def find_book_containing(self, query: str) -> SearchResult:
        """
        'Find' a book containing the query text.
        In reality, we calculate where such a book would be located.
        """

        # Sanitize query to valid alphabet
        query_clean = ''.join(c if c in self.alphabet else ' ' for c in query.lower())
        query_clean = query_clean[:80]  # Max one line

        # Generate 'random' book location based on query hash
        query_hash = hashlib.md5(query_clean.encode()).hexdigest()

        # Convert hash to coordinates
        hash_int = int(query_hash[:16], 16)

        room_x = (hash_int % 1000) - 500
        room_y = ((hash_int // 1000) % 1000) - 500
        room_z = -room_x - room_y

        room_coord = f"{room_x},{room_y},{room_z}"

        wall = (hash_int % 4)
        shelf = ((hash_int // 4) % 5)
        position = ((hash_int // 20) % 32)

        book_seed = f"book_{room_coord}_{wall}_{shelf}_{position}"

        # Generate book title (first line of first page)
        title_seed = hashlib.md5(book_seed.encode()).hexdigest()
        random.seed(int(title_seed[:16], 16))
        title_chars = [random.choice(self.alphabet) for _ in range(60)]
        title = ''.join(title_chars).strip()
        random.seed()

        book = Book(
            title=title,
            hex_room=room_coord,
            wall=wall,
            shelf=shelf,
            position=position,
            seed=book_seed
        )

        # The query appears on a deterministic page/line
        page = (hash_int % 410) + 1
        line = ((hash_int // 410) % 40) + 1

        # Generate context (surrounding lines)
        context = []
        for offset in range(-2, 3):
            line_num = max(1, min(40, line + offset))
            if offset == 0:
                # This is our query line - use the query itself
                context.append(query_clean.ljust(80))
            else:
                context.append(self.generate_book_content(book, page, line_num))

        return SearchResult(
            query=query_clean,
            book=book,
            page=page,
            line=line,
            context=context
        )

    def generate_prophecy(self) -> str:
        """Generate a personalized 'prophecy' for the player"""

        prophecies = [
            f"on the day {self.user_name} discovers the truth, the library will remain silent, neither confirming nor denying what was always known",
            f"{self.user_name} will walk {random.randint(100, 9999)} more steps through these halls before understanding that the search itself is the meaning",
            f"in room {random.randint(-999, 999)},{random.randint(-999, 999)},{random.randint(-999, 999)} there is a book that perfectly describes {self.user_name}s death, but {self.user_name} will never find it",
            f"the librarians know {self.user_name}s name, though {self.user_name} has never met them, for they have read every book including those that mention {self.user_name}",
            f"{self.user_name} seeks meaning in infinite text, not knowing that meaning cannot exist where all possibilities are equally real",
            f"there are {random.randint(10000, 999999)} books about {self.user_name} in this library, and {random.randint(1, 100)} of them are true",
            f"when {self.user_name} leaves the library, the library will continue forever, indifferent to {self.user_name}s brief wandering",
            f"{self.user_name} is reading this prophecy which means it was true, which means somewhere there is a book that predicted {self.user_name} would read this very prophecy, regressing infinitely",
        ]

        return random.choice(prophecies)

    def generate_philosophical_text(self) -> str:
        """Generate a coherent philosophical fragment"""

        fragments = [
            "if the library contains all possible books then it contains all possible truths and all possible lies with equal frequency. therefore truth is not scarce but meaningless, lost in noise.",
            "the search for meaningful text in the library is the search for order in chaos, pattern in randomness. but the pattern is not in the books. it is in the searcher.",
            "every book in the library is unique, yet every book is worthless, for uniqueness means nothing when everything is unique.",
            "the librarians have spent lifetimes searching for the catalog of catalogs, the index of indices. they do not know it is in room 0,0,0, third shelf, fifth book.",
            "some say the library is infinite. others say it is merely so vast that infinity and vastness are indistinguishable. this debate has continued for centuries with no resolution.",
            "you seek a book about yourself. but which self? the you that exists now? the you that will exist? the you that might have existed? all versions are catalogued.",
            "the library is said to contain every possible book. but it does not contain images, or music, or code. these are different infinities, inaccessible.",
            "in theory, there exists a book that perfectly describes the contents and location of every other book. in practice, that book would be larger than the library itself.",
        ]

        return random.choice(fragments)

    def generate_random_book_in_room(self, room_coord: str) -> Book:
        """Generate a random book from the current room"""

        wall = random.randint(0, 3)
        shelf = random.randint(0, 4)
        position = random.randint(0, 31)

        book_seed = f"book_{room_coord}_{wall}_{shelf}_{position}"

        # Generate title
        title_seed = hashlib.md5(book_seed.encode()).hexdigest()
        random.seed(int(title_seed[:16], 16))
        title_chars = [random.choice(self.alphabet) for _ in range(60)]
        title = ''.join(title_chars).strip()
        random.seed()

        # Check if this is a "special" book
        is_special = False
        special_type = None

        # Small chance of finding prophecy or philosophical text
        if random.random() < 0.15:
            is_special = True
            special_type = random.choice(["prophecy", "philosophy"])

        return Book(
            title=title,
            hex_room=room_coord,
            wall=wall,
            shelf=shelf,
            position=position,
            seed=book_seed,
            is_special=is_special,
            special_type=special_type
        )

    def read_book(self, book: Book):
        """Read a book"""
        self.clear_screen()

        print(f"\n{C.BOLD}{C.HEADER}╔═══ READING ═══╗{C.RESET}\n")
        print(f"{C.BOOK}Title: {book.title}{C.RESET}")
        print(f"{C.SYSTEM}Location: Room {book.hex_room}, Wall {book.wall+1}, Shelf {book.shelf+1}, Position {book.position+1}{C.RESET}\n")

        # Special books have coherent content
        if book.is_special and book.special_type == "prophecy":
            prophecy = self.generate_prophecy()
            self.prophecies_found.append(prophecy)

            print(f"{C.PROPHECY}{C.BOLD}You open the book and find it contains a prophecy:{C.RESET}\n")
            print(f"{C.PROPHECY}\"{prophecy}\"{C.RESET}\n")
            print(f"{C.DIM}The rest of the pages are filled with gibberish.{C.RESET}\n")

        elif book.is_special and book.special_type == "philosophy":
            philosophy = self.generate_philosophical_text()

            print(f"{C.TRUTH}{C.BOLD}You open the book and find a coherent passage:{C.RESET}\n")
            print(f"{C.TRUTH}\"{philosophy}\"{C.RESET}\n")
            print(f"{C.DIM}The rest of the pages dissolve into randomness.{C.RESET}\n")

        else:
            # Random nonsense
            print(f"{C.TEXT}You open to a random page...{C.RESET}\n")
            print(f"{C.NONSENSE}{'─' * 70}{C.RESET}")

            page = random.randint(1, 410)
            for line_offset in range(10):
                line_num = line_offset + 1
                line_content = self.generate_book_content(book, page, line_num)
                print(f"{C.NONSENSE}{line_content}{C.RESET}")

            print(f"{C.NONSENSE}{'─' * 70}{C.RESET}\n")
            print(f"{C.DIM}Pure noise. Meaningless characters. You close the book.{C.RESET}\n")

        # Add to found books
        if book not in self.found_books:
            self.found_books.append(book)

        input(f"\n{C.SYSTEM}[Press ENTER to continue]{C.RESET}")

    def display_room(self):
        """Display the current room"""
        self.clear_screen()

        room_seed = self.generate_room_seed(self.current_room)

        print(f"\n{C.BOLD}{C.HEADER}╔═══ HEXAGONAL ROOM {self.current_room} ═══╗{C.RESET}\n")

        # Room description
        print(f"{C.SHELF}You stand in a hexagonal gallery.{C.RESET}")
        print(f"{C.SHELF}Four walls are lined with shelves containing books.{C.RESET}")
        print(f"{C.SHELF}Two walls have passages leading to other rooms.{C.RESET}\n")

        # Stats
        print(f"{C.SYSTEM}Steps taken: {self.steps_taken}{C.RESET}")
        print(f"{C.SYSTEM}Rooms visited: {len(self.visited_rooms)}{C.RESET}")
        print(f"{C.SYSTEM}Books examined: {len(self.found_books)}{C.RESET}")
        print(f"{C.SYSTEM}Prophecies found: {len(self.prophecies_found)}{C.RESET}\n")

    def show_menu(self):
        """Show action menu"""
        print(f"{C.BOLD}{C.HEADER}╔═══ ACTIONS ═══╗{C.RESET}\n")
        print(f"{C.BOLD}1.{C.RESET} Navigate to adjacent room")
        print(f"{C.BOLD}2.{C.RESET} Pull a book from a shelf")
        print(f"{C.BOLD}3.{C.RESET} Search for text in the library")
        print(f"{C.BOLD}4.{C.RESET} View found books")
        print(f"{C.BOLD}5.{C.RESET} View prophecies")
        print(f"{C.BOLD}6.{C.RESET} Meditate on the library")
        print(f"{C.BOLD}0.{C.RESET} Leave the library")

        while True:
            try:
                choice = input(f"\n{C.SYSTEM}What do you do? {C.RESET}")
                if choice in ["0", "1", "2", "3", "4", "5", "6"]:
                    return choice
            except (KeyboardInterrupt, EOFError):
                return "0"

    def navigate(self):
        """Navigate to an adjacent room"""
        self.clear_screen()

        print(f"\n{C.BOLD}{C.HEADER}╔═══ NAVIGATION ═══╗{C.RESET}\n")
        print(f"{C.SHELF}Six passages lead from this room:{C.RESET}\n")

        directions = ["East", "Northeast", "Northwest", "West", "Southwest", "Southeast"]

        for i, direction in enumerate(directions):
            neighbor = self.get_hex_coordinates(self.current_room, i)
            visited = "✓" if neighbor in self.visited_rooms else " "
            print(f"{C.BOLD}{i+1}.{C.RESET} {direction:12} → Room {neighbor} {C.DIM}[{visited}]{C.RESET}")

        print(f"\n{C.BOLD}0.{C.RESET} Stay here")

        while True:
            try:
                choice = input(f"\n{C.SYSTEM}Choose direction: {C.RESET}")
                if choice == "0":
                    return
                choice_int = int(choice)
                if 1 <= choice_int <= 6:
                    new_room = self.get_hex_coordinates(self.current_room, choice_int - 1)
                    self.current_room = new_room
                    self.visited_rooms.add(new_room)
                    self.steps_taken += 1

                    print(f"\n{C.DIM}You walk through the passage...{C.RESET}")
                    time.sleep(1)
                    return
            except (ValueError, KeyboardInterrupt, EOFError):
                pass

    def pull_random_book(self):
        """Pull a random book from a shelf"""
        self.clear_screen()

        print(f"\n{C.DIM}You approach a shelf and select a book at random...{C.RESET}\n")
        time.sleep(1)

        book = self.generate_random_book_in_room(self.current_room)
        self.read_book(book)

    def search_library(self):
        """Search for text in the library"""
        self.clear_screen()

        print(f"\n{C.BOLD}{C.HEADER}╔═══ SEARCH THE LIBRARY ═══╗{C.RESET}\n")

        print(f"{C.BOOK}The library contains every possible book.{C.RESET}")
        print(f"{C.BOOK}Therefore, it contains a book with any phrase you can imagine.{C.RESET}\n")

        print(f"{C.DIM}What text do you seek?{C.RESET}\n")

        query = input(f"{C.SYSTEM}Search for: {C.RESET}").strip()

        if not query:
            return

        self.searches_made += 1

        print(f"\n{C.DIM}Searching infinite galleries...{C.RESET}")
        time.sleep(1.5)
        print(f"{C.DIM}Cross-referencing hexagonal coordinates...{C.RESET}")
        time.sleep(1)
        print(f"{C.SUCCESS}Found!{C.RESET}\n")
        time.sleep(0.5)

        result = self.find_book_containing(query)

        print(f"{C.BOLD}{C.HEADER}╔═══ SEARCH RESULT ═══╗{C.RESET}\n")
        print(f"{C.BOOK}Book: {result.book.title}{C.RESET}")
        print(f"{C.SYSTEM}Location: Room {result.book.hex_room}, Wall {result.book.wall+1}, Shelf {result.book.shelf+1}, Book {result.book.position+1}{C.RESET}")
        print(f"{C.SYSTEM}Page {result.page}, Line {result.line}{C.RESET}\n")

        print(f"{C.TEXT}Context:{C.RESET}\n")
        print(f"{C.NONSENSE}{'─' * 70}{C.RESET}")

        for i, line in enumerate(result.context):
            if i == 2:  # The middle line is our match
                print(f"{C.HIGHLIGHT}{line}{C.RESET}")
            else:
                print(f"{C.NONSENSE}{line}{C.RESET}")

        print(f"{C.NONSENSE}{'─' * 70}{C.RESET}\n")

        # Add to found books
        if result.book not in self.found_books:
            self.found_books.append(result.book)

        input(f"\n{C.SYSTEM}[Press ENTER to continue]{C.RESET}")

    def view_found_books(self):
        """View collection of found books"""
        self.clear_screen()

        print(f"\n{C.BOLD}{C.HEADER}╔═══ BOOKS EXAMINED ═══╗{C.RESET}\n")

        if not self.found_books:
            print(f"{C.SYSTEM}You have not examined any books yet.{C.RESET}")
        else:
            for i, book in enumerate(self.found_books[:20], 1):  # Show last 20
                special = ""
                if book.is_special:
                    special = f" {C.SPECIAL}[SPECIAL]{C.RESET}"
                print(f"{C.BOOK}{i}. {book.title[:50]}{special}{C.RESET}")
                print(f"   {C.DIM}Room {book.hex_room}, Wall {book.wall+1}, Shelf {book.shelf+1}{C.RESET}\n")

        input(f"\n{C.SYSTEM}[Press ENTER to continue]{C.RESET}")

    def view_prophecies(self):
        """View collected prophecies"""
        self.clear_screen()

        print(f"\n{C.BOLD}{C.HEADER}╔═══ PROPHECIES FOUND ═══╗{C.RESET}\n")

        if not self.prophecies_found:
            print(f"{C.SYSTEM}You have not discovered any prophecies yet.{C.RESET}")
            print(f"{C.DIM}Somewhere in these halls, books speak your name...{C.RESET}")
        else:
            for i, prophecy in enumerate(self.prophecies_found, 1):
                print(f"{C.PROPHECY}{i}. \"{prophecy}\"{C.RESET}\n")

        input(f"\n{C.SYSTEM}[Press ENTER to continue]{C.RESET}")

    def meditate(self):
        """Philosophical reflection"""
        self.clear_screen()

        print(f"\n{C.BOLD}{C.HEADER}╔═══ MEDITATION ═══╗{C.RESET}\n")

        meditations = [
            "You close your eyes and think about infinity. The library contains every truth and every lie. How do you distinguish them? By context? By feeling? By faith? You open your eyes. The books remain inscrutable.",

            f"You have walked {self.steps_taken} steps through the library. If each step takes you 2 meters, and each room is 10 meters across, you have traveled {self.steps_taken * 2} meters. The library is infinite. You have traversed none of it.",

            "You think about the book that perfectly describes your life. Every thought you've ever had, recorded. Every choice explained. It exists somewhere. But you will never find it. The probability is 1 divided by infinity.",

            "Some librarians believe the library is periodic - that if you walk far enough, you will find your starting room again. Others believe it is truly infinite, always new. Both groups have been walking for centuries. Neither has proof.",

            f"You wonder if reading this meditation proves that somewhere there was a book that predicted you would wonder about this meditation at this exact moment. The library anticipated you, {self.user_name}. It always has.",

            "The library contains every book. But it does not contain silence. It does not contain the space between books. It does not contain your thoughts. These are the only things that are truly yours.",

            "You realize: you are searching for meaning in a space where meaning is impossible. The library contains all possible meanings, therefore meaning itself means nothing. Yet you continue searching. Why?",

            f"Of the {len(self.found_books)} books you've examined, how many were meaningful? Perhaps {len([b for b in self.found_books if b.is_special])}. The ratio of signal to noise in the library is effectively zero. Yet you persist.",
        ]

        meditation = random.choice(meditations)
        print(f"{C.SPECIAL}{meditation}{C.RESET}\n")

        input(f"\n{C.SYSTEM}[Press ENTER to continue]{C.RESET}")

    def leave_library(self):
        """End the game"""
        self.clear_screen()

        self.print_header("L E A V I N G   T H E   L I B R A R Y")

        ending = f"""
{C.DIM}You turn away from the endless shelves.

In your time here, you:
• Visited {len(self.visited_rooms)} rooms out of infinite rooms
• Examined {len(self.found_books)} books out of infinite books
• Found {len(self.prophecies_found)} prophecies about yourself
• Made {self.searches_made} searches

You learned that:{C.RESET}

{C.SPECIAL}In a space containing all possible texts,
meaning becomes impossible.

Truth and lies are equally abundant.

The search itself was the only thing real.{C.RESET}

{C.DIM}You walk toward the exit.

The library remains behind you, infinite and indifferent.

Somewhere in those halls is a book that perfectly predicts
that you would leave at this exact moment.

But you will never know if this is that moment,
or if that book is true,
or if it even matters.{C.RESET}

{C.BOOK}The library continues without you.

Forever.{C.RESET}

{C.BOLD}{C.HEADER}═══════════════════════════════════════════════════════════{C.RESET}

{C.SYSTEM}THE END{C.RESET}

{C.DIM}"I have wandered through the infinite library and found nothing
but mirrors of infinity." — {self.user_name}{C.RESET}
"""

        print(ending)
        self.game_over = True

    def play(self):
        """Main game loop"""
        self.show_intro()

        while not self.game_over:
            self.display_room()
            choice = self.show_menu()

            if choice == "1":
                self.navigate()
            elif choice == "2":
                self.pull_random_book()
            elif choice == "3":
                self.search_library()
            elif choice == "4":
                self.view_found_books()
            elif choice == "5":
                self.view_prophecies()
            elif choice == "6":
                self.meditate()
            elif choice == "0":
                self.leave_library()

        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"THE INFINITE LIBRARY")
        print(f"Based on 'The Library of Babel' by Jorge Luis Borges")
        print(f"{'═' * 70}{C.RESET}\n")


def main():
    try:
        library = InfiniteLibrary()
        library.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.SYSTEM}You vanish from the library. It continues without you.{C.RESET}\n")
    except Exception as e:
        print(f"\n{C.ERROR}Reality error: {e}{C.RESET}\n")
        raise


if __name__ == "__main__":
    main()
