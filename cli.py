#!/usr/bin/env python3
"""
Claude Buddy Lab - Search, preview, and customize your Claude Code buddy

Usage:
    python cli.py preview              # Preview current buddy
    python cli.py search --species owl # Search for specific species
    python cli.py web                  # Start web interface
    python cli.py interactive          # Interactive TUI mode
"""

import json
import hashlib
import random
import sys
import os
from pathlib import Path

# For interactive mode (using stdlib curses)
import curses

# ============== Constants ==============
RARITIES = ["common", "uncommon", "rare", "epic", "legendary"]
RARITY_WEIGHTS = {"common": 60, "uncommon": 25, "rare": 10, "epic": 4, "legendary": 1}
SPECIES = ["duck", "goose", "blob", "cat", "dragon", "octopus", "owl", "penguin",
           "turtle", "snail", "ghost", "axolotl", "capybara", "cactus", "robot",
           "rabbit", "mushroom", "chonk"]
EYES = ["·", "✦", "×", "◉", "@", "°"]
HATS = ["none", "crown", "tophat", "propeller", "halo", "wizard", "beanie", "tinyduck"]
STAT_NAMES = ["DEBUGGING", "PATIENCE", "CHAOS", "WISDOM", "SNARK"]
RARITY_FLOOR = {"common": 5, "uncommon": 15, "rare": 25, "epic": 35, "legendary": 50}
DEFAULT_SALT = "friend-2026-401"

# ============== ASCII Sprites ==============
BODIES = {
    "duck": [
        ["            ", "    __      ", "  <({E} )___  ", "   (  ._>   ", "    `--´    "],
        ["            ", "    __      ", "  <({E} )___  ", "   (  ._>   ", "    `--´~   "],
        ["            ", "    __      ", "  <({E} )___  ", "   (  .__>  ", "    `--´    "],
    ],
    "goose": [
        ["            ", "     ({E}>    ", "     ||     ", "   _(__)_   ", "    ^^^^    "],
        ["            ", "    ({E}>     ", "     ||     ", "   _(__)_   ", "    ^^^^    "],
        ["            ", "     ({E}>>   ", "     ||     ", "   _(__)_   ", "    ^^^^    "],
    ],
    "blob": [
        ["            ", "   .----.   ", "  ( {E}  {E} )  ", "  (      )  ", "   `----´   "],
        ["            ", "  .------.  ", " (  {E}  {E}  ) ", " (        ) ", "  `------´  "],
        ["            ", "    .--.    ", "   ({E}  {E})   ", "   (    )   ", "    `--´    "],
    ],
    "cat": [
        ["            ", "   /\\_/\\    ", "  ( {E}   {E})  ", "  (  ω  )   ", '  (")_(")   '],
        ["            ", "   /\\_/\\    ", "  ( {E}   {E})  ", "  (  ω  )   ", '  (")_(")~  '],
        ["            ", "   /\\-/\\    ", "  ( {E}   {E})  ", "  (  ω  )   ", '  (")_(")   '],
    ],
    "dragon": [
        ["            ", "  /^\\  /^\\  ", " <  {E}  {E}  > ", " (   ~~   ) ", "  `-vvvv-´  "],
        ["            ", "  /^\\  /^\\  ", " <  {E}  {E}  > ", " (        ) ", "  `-vvvv-´  "],
        ["   ~    ~   ", "  /^\\  /^\\  ", " <  {E}  {E}  > ", " (   ~~   ) ", "  `-vvvv-´  "],
    ],
    "octopus": [
        ["            ", "   .----.   ", "  ( {E}  {E} )  ", "  (______)  ", "  /\\/\\/\\/\\  "],
        ["            ", "   .----.   ", "  ( {E}  {E} )  ", "  (______)  ", "  \\/\\/\\/\\/  "],
        ["     o      ", "   .----.   ", "  ( {E}  {E} )  ", "  (______)  ", "  /\\/\\/\\/\\  "],
    ],
    "owl": [
        ["            ", "   /\\  /\\   ", "  (({E})({E}))  ", "  (  ><  )  ", "   `----´   "],
        ["            ", "   /\\  /\\   ", "  (({E})({E}))  ", "  (  ><  )  ", "   .----.   "],
        ["            ", "   /\\  /\\   ", "  (({E})(-))  ", "  (  ><  )  ", "   `----´   "],
    ],
    "penguin": [
        ["            ", "  .---.     ", "  ({E}>{E})     ", " /(   )\\    ", "  `---´     "],
        ["            ", "  .---.     ", "  ({E}>{E})     ", " |(   )|    ", "  `---´     "],
        ["  .---.     ", "  ({E}>{E})     ", " /(   )\\    ", "  `---´     ", "   ~ ~      "],
    ],
    "turtle": [
        ["            ", "   _,--._   ", "  ( {E}  {E} )  ", " /[______]\\ ", "  ``    ``  "],
        ["            ", "   _,--._   ", "  ( {E}  {E} )  ", " /[______]\\ ", "   ``  ``   "],
        ["            ", "   _,--._   ", "  ( {E}  {E} )  ", " /[======]\\ ", "  ``    ``  "],
    ],
    "snail": [
        ["            ", " {E}    .--.  ", "  \\  ( @ )  ", "   \\_`--´   ", "  ~~~~~~~   "],
        ["            ", "  {E}   .--.  ", "  |  ( @ )  ", "   \\_`--´   ", "  ~~~~~~~   "],
        ["            ", " {E}    .--.  ", "  \\  ( @  ) ", "   \\_`--´   ", "   ~~~~~~   "],
    ],
    "ghost": [
        ["            ", "   .----.   ", "  / {E}  {E} \\  ", "  |      |  ", "  ~`~``~`~  "],
        ["            ", "   .----.   ", "  / {E}  {E} \\  ", "  |      |  ", "  `~`~~`~`  "],
        ["    ~  ~    ", "   .----.   ", "  / {E}  {E} \\  ", "  |      |  ", "  ~~`~~`~~  "],
    ],
    "axolotl": [
        ["            ", "}~(______)~{", "}~({E} .. {E})~{", "  ( .--. )  ", "  (_/  \\_)  "],
        ["            ", "~}(______){~", "~}({E} .. {E}){~", "  ( .--. )  ", "  (_/  \\_)  "],
        ["            ", "}~(______)~{", "}~({E} .. {E})~{", "  (  --  )  ", "  ~_/  \\_~  "],
    ],
    "capybara": [
        ["            ", "  n______n  ", " ( {E}    {E} ) ", " (   oo   ) ", "  `------´  "],
        ["            ", "  n______n  ", " ( {E}    {E} ) ", " (   Oo   ) ", "  `------´  "],
        ["    ~  ~    ", "  u______n  ", " ( {E}    {E} ) ", " (   oo   ) ", "  `------´  "],
    ],
    "cactus": [
        ["            ", " n  ____  n ", " | |{E}  {E}| | ", " |_|    |_| ", "   |    |   "],
        ["            ", "    ____    ", " n |{E}  {E}| n ", " |_|    |_| ", "   |    |   "],
        [" n        n ", " |  ____  | ", " | |{E}  {E}| | ", " |_|    |_| ", "   |    |   "],
    ],
    "robot": [
        ["            ", "   .[||].   ", "  [ {E}  {E} ]  ", "  [ ==== ]  ", "  `------´  "],
        ["            ", "   .[||].   ", "  [ {E}  {E} ]  ", "  [ -==- ]  ", "  `------´  "],
        ["     *      ", "   .[||].   ", "  [ {E}  {E} ]  ", "  [ ==== ]  ", "  `------´  "],
    ],
    "rabbit": [
        ["            ", "   (\\__/)   ", "  ( {E}  {E} )  ", " =(  ..  )= ", '  (")__(")  '],
        ["            ", "   (|__/)   ", "  ( {E}  {E} )  ", " =(  ..  )= ", '  (")__(")  '],
        ["            ", "   (\\__/)   ", "  ( {E}  {E} )  ", " =( .  . )= ", '  (")__(")  '],
    ],
    "mushroom": [
        ["            ", " .-o-OO-o-. ", "(__________)", "   |{E}  {E}|   ", "   |____|   "],
        ["            ", " .-O-oo-O-. ", "(__________)", "   |{E}  {E}|   ", "   |____|   "],
        ["   . o  .   ", " .-o-OO-o-. ", "(__________)", "   |{E}  {E}|   ", "   |____|   "],
    ],
    "chonk": [
        ["            ", "  /\\    /\\  ", " ( {E}    {E} ) ", " (   ..   ) ", "  `------´  "],
        ["            ", "  /\\    /|  ", " ( {E}    {E} ) ", " (   ..   ) ", "  `------´  "],
        ["            ", "  /\\    /\\  ", " ( {E}    {E} ) ", " (   ..   ) ", "  `------´~ "],
    ],
}

HAT_LINES = {
    "none": "", "crown": "   \\^^^/    ", "tophat": "   [___]    ",
    "propeller": "    -+-     ", "halo": "   (   )    ", "wizard": "    /^\\     ",
    "beanie": "   (___)    ", "tinyduck": "    ,>      ",
}


# ============== Core Functions ==============
def mulberry32(seed):
    a = seed & 0xFFFFFFFF
    def rng():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = ((a ^ (a >> 15)) * (1 | a)) & 0xFFFFFFFF
        t = ((t + ((t ^ (t >> 7)) * (61 | t))) ^ t) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) >> 0) / 4294967296
    return rng


def hash_string(s):
    h = 2166136261
    for c in s:
        h ^= ord(c)
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def pick(rng, arr):
    return arr[int(rng() * len(arr))]


def roll_rarity(rng):
    total = sum(RARITY_WEIGHTS.values())
    roll = rng() * total
    for r in RARITIES:
        roll -= RARITY_WEIGHTS[r]
        if roll < 0:
            return r
    return "common"


def roll_stats(rng, rarity):
    floor_val = RARITY_FLOOR[rarity]
    peak = pick(rng, STAT_NAMES)
    dump = pick(rng, STAT_NAMES)
    while dump == peak:
        dump = pick(rng, STAT_NAMES)
    stats = {}
    for name in STAT_NAMES:
        if name == peak:
            stats[name] = min(100, floor_val + 50 + int(rng() * 30))
        elif name == dump:
            stats[name] = max(1, floor_val - 10 + int(rng() * 15))
        else:
            stats[name] = floor_val + int(rng() * 40)
    return stats


def roll_with_salt(user_id, salt):
    rng = mulberry32(hash_string(user_id + salt))
    rarity = roll_rarity(rng)
    return {
        "rarity": rarity,
        "species": pick(rng, SPECIES),
        "eye": pick(rng, EYES),
        "hat": "none" if rarity == "common" else pick(rng, HATS),
        "shiny": rng() < 0.01,
        "stats": roll_stats(rng, rarity),
    }


def render_sprite(bones, frame=0):
    frames = BODIES[bones["species"]]
    body = [line.replace("{E}", bones["eye"]) for line in frames[frame % len(frames)]]
    lines = list(body)
    if bones["hat"] != "none" and not lines[0].strip():
        lines[0] = HAT_LINES[bones["hat"]]
    if not lines[0].strip() and all(not f[0].strip() for f in frames):
        lines.pop(0)
    return lines


def render_face(bones):
    eye = bones["eye"]
    species = bones["species"]
    faces = {
        "duck": f"({eye}>", "goose": f"({eye}>", "blob": f"({eye}{eye})",
        "cat": f"={eye}ω{eye}=", "dragon": f"<{eye}~{eye}>", "octopus": f"~({eye}{eye})~",
        "owl": f"({eye})({eye})", "penguin": f"({eye}>)", "turtle": f"[{eye}_{eye}]",
        "snail": f"{eye}(@)", "ghost": f"/{eye}{eye}\\", "axolotl": "}}"+eye+"."+eye+"{{",
        "capybara": f"({eye}oo{eye})", "cactus": f"|{eye}  {eye}|", "robot": f"[{eye}{eye}]",
        "rabbit": f"({eye}..{eye})", "mushroom": f"|{eye}  {eye}|", "chonk": f"({eye}.{eye})",
    }
    return faces.get(species, species)


def detect_user_id():
    home = Path.home()
    for candidate in [home / ".claude" / ".config.json", home / ".claude.json"]:
        if candidate.exists():
            try:
                config = json.loads(candidate.read_text())
                return config.get("oauthAccount", {}).get("accountUuid") or config.get("userID")
            except:
                continue
    return None


def generate_salt(prefix, index, length):
    if len(prefix) > length:
        raise ValueError(f"Prefix too long")
    return prefix + str(index).zfill(length - len(prefix))


def matches_filters(result, filters):
    for key in ["species", "rarity", "eye", "hat"]:
        if filters.get(key) and result[key] != filters[key]:
            return False
    if filters.get("shiny") and not result["shiny"]:
        return False
    if filters.get("min_stat"):
        ms = filters["min_stat"]
        if result["stats"][ms["name"]] < ms["threshold"]:
            return False
    return True


def search_salts(user_id, total=100000, prefix="lab-", filters=None, max_matches=20):
    filters = filters or {}
    matches = []
    for i in range(total):
        salt = generate_salt(prefix, i, len(DEFAULT_SALT))
        result = roll_with_salt(user_id, salt)
        if matches_filters(result, filters):
            matches.append({"salt": salt, "buddy": result})
            if len(matches) >= max_matches:
                break
    return matches


def parse_min_stat(value):
    if not value:
        return None
    parts = value.split(":")
    name = parts[0].strip().upper()
    threshold = int(parts[1]) if len(parts) > 1 else 0
    if name not in STAT_NAMES or not (0 < threshold <= 100):
        raise ValueError(f"Invalid: {value}")
    return {"name": name, "threshold": threshold}


# ============== CLI Functions ==============
def print_buddy(buddy, salt, user_id):
    print(f"\n{'='*50}")
    print(f"Salt: {salt}")
    print(f"User ID: {user_id}")
    print(f"Species: {buddy['species'].capitalize()}")
    print(f"Rarity: {buddy['rarity'].capitalize()}")
    print(f"Eye: {buddy['eye']}")
    print(f"Hat: {buddy['hat']}")
    print(f"Shiny: {'Yes ✦' if buddy['shiny'] else 'No'}")
    print(f"\nStats:")
    for stat, value in buddy["stats"].items():
        bar = "█" * (value // 5)
        print(f"  {stat:12} {bar} {value}")
    print(f"\nSprite:\n")
    for line in render_sprite(buddy):
        print(line)
    print(f"\nFace: {render_face(buddy)}")
    print(f"{'='*50}\n")


def cmd_preview(args):
    salt = get_arg(args, "--salt", DEFAULT_SALT)
    user_id = get_arg(args, "--user-id") or detect_user_id() or "anon"
    buddy = roll_with_salt(user_id, salt)
    print_buddy(buddy, salt, user_id)


def cmd_search(args):
    user_id = get_arg(args, "--user-id") or detect_user_id() or "anon"
    filters = {
        "species": get_arg(args, "--species"),
        "rarity": get_arg(args, "--rarity"),
        "eye": get_arg(args, "--eye"),
        "hat": get_arg(args, "--hat"),
        "shiny": "--shiny" in args,
    }
    if "--min-stat" in args:
        idx = args.index("--min-stat")
        if idx + 1 < len(args):
            try:
                filters["min_stat"] = parse_min_stat(args[idx + 1])
            except ValueError as e:
                print(f"Error: {e}")
                return

    total = int(get_arg(args, "--total", "100000"))
    prefix = get_arg(args, "--prefix", "lab-")

    print(f"Searching... (User: {user_id}, Attempts: {total})")
    matches = search_salts(user_id, total, prefix, filters)

    if not matches:
        print("No matches found. Try increasing --total or relaxing filters.")
        return

    print(f"\nFound {len(matches)} matches:\n")
    for i, m in enumerate(matches, 1):
        b = m["buddy"]
        top = max(b["stats"].items(), key=lambda x: x[1])
        print(f"{i}. {b['rarity']} {b['species']} | Salt: {m['salt']}")
        print(f"   Eye: {b['eye']} | Hat: {b['hat']} | Shiny: {'✦' if b['shiny'] else ' '}")
        print(f"   Top: {top[0]} {top[1]}\n")


def cmd_web(args):
    host = get_arg(args, "--host", "127.0.0.1")
    port = int(get_arg(args, "--port", "8080"))
    print(f"Starting web server at http://{host}:{port}")
    print("Press Ctrl+C to stop\n")

    try:
        from flask import Flask, send_from_directory, jsonify, request
    except ImportError:
        print("Flask required: pip3 install flask")
        return

    app = Flask(__name__, static_folder="public", static_url_path="")

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/api/meta")
    def meta():
        return jsonify({
            "species": SPECIES, "rarities": RARITIES, "eyes": EYES, "hats": HATS,
            "defaultSalt": DEFAULT_SALT, "detectedUserId": detect_user_id(),
        })

    @app.route("/api/preview", methods=["POST"])
    def preview_api():
        data = request.json
        uid = data.get("userId") or detect_user_id() or "anon"
        salt = data.get("salt", DEFAULT_SALT)
        buddy = roll_with_salt(uid, salt)
        return jsonify({
            "userId": uid, "salt": salt, "buddy": buddy,
            "sprite": render_sprite(buddy), "face": render_face(buddy),
        })

    @app.route("/api/search", methods=["POST"])
    def search_api():
        data = request.json
        uid = data.get("userId") or detect_user_id() or "anon"
        filters = {k: data.get(k) for k in ["species", "rarity", "eye", "hat"]}
        filters["shiny"] = data.get("shiny", False)
        if data.get("minStat"):
            try:
                filters["min_stat"] = parse_min_stat(data["minStat"])
            except:
                pass
        matches = search_salts(uid, data.get("total", 100000), data.get("prefix", "lab-"), filters)
        for m in matches:
            m["sprite"] = render_sprite(m["buddy"])
            m["face"] = render_face(m["buddy"])
        return jsonify({"matches": matches, "searched": len(matches)})

    import webbrowser, threading
    if "--open" in args:
        threading.Timer(1, lambda: webbrowser.open(f"http://{host}:{port}")).start()
    app.run(host=host, port=port, debug=False)


def get_arg(args, flag, default=None):
    if flag in args:
        idx = args.index(flag)
        if idx + 1 < len(args):
            return args[idx + 1]
    return default


# ============== Interactive TUI (curses) ==============
class InteractiveBuddyViewer:
    def __init__(self, user_id):
        self.user_id = user_id
        self.salt_index = 0
        self.prefix = "lab-"
        self.filters = {
            "species": None,
            "rarity": None,
            "eye": None,
            "hat": None,
            "shiny": False,
            "min_stat": None,
        }
        self.history = []  # List of (salt, buddy) tuples
        self.history_index = -1
        self.message = ""

    def generate_next(self):
        """Generate next buddy matching filters"""
        max_attempts = 50000
        for i in range(max_attempts):
            salt = generate_salt(self.prefix, self.salt_index, len(DEFAULT_SALT))
            buddy = roll_with_salt(self.user_id, salt)
            self.salt_index += 1

            if matches_filters(buddy, self.filters):
                return salt, buddy
        return None, None

    def draw_main_screen(self, stdscr, salt, buddy):
        """Draw main preview screen"""
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Title
        title = "🧪 Claude Buddy Lab - Interactive Mode "
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(0, max(0, (width - len(title)) // 2), title[:width-1])
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

        # Divider
        stdscr.addstr(1, 0, "=" * min(60, width-1))

        # Buddy info
        row = 3
        info_lines = [
            f"Salt: {salt}",
            f"Species: {buddy['species'].capitalize()}  |  Rarity: {buddy['rarity'].capitalize()}",
            f"Eye: {buddy['eye']}  |  Hat: {buddy['hat']}  |  Shiny: {'✦ Yes' if buddy['shiny'] else 'No'}",
        ]
        for line in info_lines:
            if row < height - 10:
                stdscr.addstr(row, 2, line[:width-3])
                row += 1

        # Stats
        row += 1
        stdscr.addstr(row, 2, "Stats:", curses.A_BOLD)
        row += 1
        for stat, value in buddy["stats"].items():
            if row < height - 10:
                bar_len = value // 5
                bar = "█" * bar_len
                stat_line = f"  {stat:12} {bar} {value}"
                stdscr.addstr(row, 2, stat_line[:width-3])
                row += 1

        # Sprite
        row += 1
        stdscr.addstr(row, 2, "Sprite:", curses.A_BOLD)
        row += 1
        sprite_lines = render_sprite(buddy)
        color = curses.color_pair(3) if buddy['shiny'] else curses.color_pair(2)
        stdscr.attron(color)
        for line in sprite_lines:
            if row < height - 8:
                stdscr.addstr(row, 4, line[:width-5])
                row += 1
        stdscr.attroff(color)

        # Face
        row += 1
        if row < height - 6:
            stdscr.addstr(row, 2, f"Face: {render_face(buddy)}", curses.color_pair(3))

        # History position
        row += 2
        if self.history:
            pos_info = f"[{self.history_index + 1}/{len(self.history)} in history]"
            stdscr.addstr(row, 2, pos_info, curses.color_pair(4))

        # Message
        if self.message:
            stdscr.addstr(row + 1, 2, self.message, curses.color_pair(5) | curses.A_BOLD)
            self.message = ""

        # Controls
        row = height - 3
        controls = " n/→:Next  p/←:Prev  r:Re-roll  c:Filters  a:Apply  s:Show salt  q:Quit "
        stdscr.attron(curses.color_pair(6) | curses.A_REVERSE)
        stdscr.addstr(row, 0, controls.center(width)[:width-1])
        stdscr.attroff(curses.color_pair(6) | curses.A_REVERSE)

        stdscr.refresh()

    def draw_filters_screen(self, stdscr):
        """Draw filter configuration screen"""
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        title = " Configure Filters "
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(0, max(0, (width - len(title)) // 2), title[:width-1])
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(1, 0, "=" * min(60, width-1))

        row = 4
        stdscr.addstr(row, 2, "Current filters:", curses.A_BOLD)
        row += 2

        # Display current filters
        filter_display = []
        for k, v in self.filters.items():
            if v:
                if k == "min_stat":
                    filter_display.append(f"{v['name']}>={v['threshold']}")
                elif k == "shiny":
                    filter_display.append("shiny ✦")
                else:
                    filter_display.append(str(v))

        if filter_display:
            stdscr.addstr(row, 4, ", ".join(filter_display)[:width-5])
        else:
            stdscr.addstr(row, 4, "(none)", curses.color_pair(4))
        row += 2

        # Instructions
        stdscr.addstr(row, 2, "Press number keys to toggle filters:", curses.A_BOLD)
        row += 2

        stdscr.addstr(row, 4, "1. Species (duck)")
        stdscr.addstr(row, 14, "2. Rarity (common)" if not self.filters['rarity'] else f"2. Rarity ({self.filters['rarity']})")
        row += 1
        stdscr.addstr(row, 4, "3. Shiny only: " + ("ON ✦" if self.filters['shiny'] else "OFF"))
        row += 1
        stdscr.addstr(row, 4, "4. Clear all filters")
        row += 2

        stdscr.addstr(row, 2, "Press ENTER to save and return", curses.A_BOLD)
        row += 1
        stdscr.addstr(row, 2, "Press ESC to cancel", curses.color_pair(4))

        # Filters hint
        row += 2
        stdscr.addstr(row, 2, "Species:", curses.A_BOLD)
        row += 1
        species_str = ", ".join(SPECIES[:9])
        stdscr.addstr(row, 4, species_str[:width-6], curses.color_pair(4))
        row += 1
        species_str = ", ".join(SPECIES[9:])
        stdscr.addstr(row, 4, species_str[:width-6], curses.color_pair(4))

        stdscr.refresh()

    def run_filter_config(self, stdscr):
        """Run filter configuration interaction"""
        curses.echo()
        curses.curs_set(1)

        while True:
            self.draw_filters_screen(stdscr)
            key = stdscr.getch()

            if key == 27:  # ESC
                break
            elif key == 10 or key == curses.KEY_ENTER:  # Enter
                # Reset salt index when filters change
                self.salt_index = 0
                self.history = []
                self.history_index = -1
                break
            elif key == ord('1'):
                # Cycle species
                if not self.filters['species']:
                    self.filters['species'] = SPECIES[0]
                else:
                    idx = (SPECIES.index(self.filters['species']) + 1) % len(SPECIES)
                    self.filters['species'] = SPECIES[idx]
            elif key == ord('2'):
                # Cycle rarity
                if not self.filters['rarity']:
                    self.filters['rarity'] = RARITIES[0]
                else:
                    idx = (RARITIES.index(self.filters['rarity']) + 1) % len(RARITIES)
                    self.filters['rarity'] = RARITIES[idx]
            elif key == ord('3'):
                # Toggle shiny
                self.filters['shiny'] = not self.filters['shiny']
            elif key == ord('4'):
                # Clear all
                self.filters = {
                    "species": None,
                    "rarity": None,
                    "eye": None,
                    "hat": None,
                    "shiny": False,
                    "min_stat": None,
                }

        curses.noecho()
        curses.curs_set(0)

    def apply_salt(self, salt):
        """Apply salt to Claude config"""
        home = Path.home()
        config_paths = [
            home / ".claude" / ".config.json",
            home / ".claude.json",
        ]

        config_path = None
        for p in config_paths:
            if p.exists():
                config_path = p
                break

        if not config_path:
            self.message = "ERROR: Claude config not found!"
            return

        try:
            # Backup
            backup_path = config_path.with_suffix(config_path.suffix + '.bak')
            backup_path.write_text(config_path.read_text())

            # Read and update
            config = json.loads(config_path.read_text())

            if 'buddy' not in config:
                config['buddy'] = {}
            config['buddy']['salt'] = salt

            config_path.write_text(json.dumps(config, indent=2))
            self.message = f"✓ Salt applied! Backup: {backup_path.name}"

        except Exception as e:
            self.message = f"ERROR: {e}"

    def run(self, stdscr):
        """Main curses loop"""
        # Setup colors
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)      # Title
        curses.init_pair(2, curses.COLOR_GREEN, -1)     # Sprite normal
        curses.init_pair(3, curses.COLOR_YELLOW, -1)    # Sprite shiny / face
        curses.init_pair(4, curses.COLOR_WHITE, -1)     # Info
        curses.init_pair(5, curses.COLOR_RED, -1)       # Error
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Controls

        curses.noecho()
        curses.curs_set(0)
        stdscr.timeout(100)  # Non-blocking input

        # Generate first buddy
        salt, buddy = self.generate_next()
        if not salt:
            self.message = "Could not generate buddy with current filters"
            return

        self.history.append((salt, buddy))
        self.history_index = 0

        while True:
            self.draw_main_screen(stdscr, salt, buddy)

            key = stdscr.getch()

            if key == ord('q'):
                # Quit
                break
            elif key in (ord('n'), curses.KEY_RIGHT):
                # Next
                salt, buddy = self.generate_next()
                if salt:
                    self.history = self.history[:self.history_index + 1]
                    self.history.append((salt, buddy))
                    self.history_index += 1
            elif key in (ord('p'), curses.KEY_LEFT):
                # Previous
                if self.history_index > 0:
                    self.history_index -= 1
                    salt, buddy = self.history[self.history_index]
            elif key == ord('r'):
                # Re-roll
                salt, buddy = self.generate_next()
                if salt:
                    self.history = self.history[:self.history_index + 1]
                    self.history.append((salt, buddy))
                    self.history_index += 1
            elif key == ord('c'):
                # Change filters
                self.run_filter_config(stdscr)
                # Generate new with updated filters
                salt, buddy = self.generate_next()
                if salt:
                    self.history = []
                    self.history.append((salt, buddy))
                    self.history_index = 0
            elif key == ord('a'):
                # Apply
                self.apply_salt(salt)
            elif key == ord('s'):
                # Show salt
                self.message = f"Salt: {salt}"


def cmd_interactive(args):
    """Start interactive TUI mode"""
    user_id = get_arg(args, "--user-id") or detect_user_id() or "anon"
    viewer = InteractiveBuddyViewer(user_id)
    curses.wrapper(viewer.run)


def print_help():
    print("""Claude Buddy Lab - Search, preview, and customize your Claude Code buddy

Usage: python cli.py <command> [options]

Commands:
  preview      Preview a buddy for a given salt
  search       Search for buddies matching criteria
  web          Start web interface
  interactive  Start interactive TUI mode

Examples:
  python cli.py preview
  python cli.py preview --salt my-salt
  python cli.py search --species owl --rarity epic
  python cli.py search --shiny --total 500000
  python cli.py web --open
  python cli.py interactive
""")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help", "help"]:
        print_help()
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "preview":
        cmd_preview(args)
    elif cmd == "search":
        cmd_search(args)
    elif cmd == "web":
        cmd_web(args)
    elif cmd == "interactive":
        cmd_interactive(args)
    else:
        print(f"Unknown command: {cmd}")
        print_help()


if __name__ == "__main__":
    main()
