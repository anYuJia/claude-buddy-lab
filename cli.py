#!/usr/bin/env python3
"""
Claude Buddy Lab - Search, preview, and customize your Claude Code buddy

Usage:
    python cli.py preview              # Preview current buddy
    python cli.py search --species owl # Search for specific species
    python cli.py web                  # Start web interface
"""

import json
import hashlib
import random
import sys
import os
from pathlib import Path

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

    @app.route("/api/apply", methods=["POST"])
    def apply_api():
        data = request.json
        salt = data.get("salt")
        if not salt:
            return jsonify({"success": False, "error": "Salt required"})

        # Find Claude config
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
            return jsonify({"success": False, "error": "Claude config not found"})

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
            return jsonify({"success": True, "backup": str(backup_path)})

        except Exception as e:
            return jsonify({"success": False, "error": str(e)})

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


def print_help():
    print("""Claude Buddy Lab - Search, preview, and customize your Claude Code buddy

Usage: python cli.py <command> [options]

Commands:
  preview      Preview a buddy for a given salt
  search       Search for buddies matching criteria
  web          Start web interface

Examples:
  python cli.py preview
  python cli.py preview --salt my-salt
  python cli.py search --species owl --rarity epic
  python cli.py search --shiny --total 500000
  python cli.py web --open
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
    else:
        print(f"Unknown command: {cmd}")
        print_help()


if __name__ == "__main__":
    main()
