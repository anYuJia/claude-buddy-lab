#!/usr/bin/env python3
"""
Claude Buddy Lab - Search, preview, and apply custom buddies to Claude Code

Usage:
    python3 cli.py           # Start web interface
    python3 cli.py --open    # Start and open browser
"""

import json
import hashlib
import random
import re
import shutil
import subprocess
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


# ============== Binary Patching ==============
SALT_PATTERNS = [
    re.compile(rb'friend-\d{4}-\d+'),
    re.compile(rb'ccbf-\d{10}'),
    re.compile(rb'lab-\d{11}'),
]

STATE_FILE = Path.home() / ".claude-buddy-lab.json"


def find_claude_binary():
    result = shutil.which("claude")
    if not result:
        return None
    return str(Path(result).resolve())


def detect_binary_salt(binary_path=None):
    if not binary_path:
        binary_path = find_claude_binary()
    if not binary_path or not Path(binary_path).exists():
        return None
    data = Path(binary_path).read_bytes()
    for pattern in SALT_PATTERNS:
        m = pattern.search(data)
        if m:
            return {"salt": m.group(0).decode("ascii"), "length": len(m.group(0)), "filePath": binary_path}
    return None


def replace_salt_in_binary(search_salt, new_salt, binary_path):
    if len(search_salt) != len(new_salt):
        raise ValueError(f"Salt length mismatch: '{search_salt}' ({len(search_salt)}) vs '{new_salt}' ({len(new_salt)})")
    data = bytearray(Path(binary_path).read_bytes())
    search_bytes = search_salt.encode("utf-8")
    replace_bytes = new_salt.encode("utf-8")
    offsets = []
    pos = 0
    while True:
        idx = data.find(search_bytes, pos)
        if idx == -1:
            break
        offsets.append(idx)
        pos = idx + 1
    if not offsets:
        raise ValueError(f'Could not find "{search_salt}" in binary bytes.')
    for offset in offsets:
        data[offset:offset + len(replace_bytes)] = replace_bytes
    Path(binary_path).write_bytes(bytes(data))
    resign_binary(binary_path)
    return {"filePath": binary_path, "patchCount": len(offsets)}


def resign_binary(file_path):
    if sys.platform != "darwin":
        return
    try:
        subprocess.run(["codesign", "--force", "--sign", "-", file_path],
                       capture_output=True, check=True)
    except Exception as e:
        raise RuntimeError(f"Binary patch succeeded but macOS ad-hoc signing failed: {e}")


def read_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except:
            pass
    return {"version": 1, "binaries": {}}


def write_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def record_original_salt(binary_path, original_salt):
    state = read_state()
    if binary_path not in state.get("binaries", {}):
        state.setdefault("binaries", {})[binary_path] = {
            "originalSalt": original_salt,
            "recordedAt": __import__("datetime").datetime.now().isoformat(),
        }
        write_state(state)


def get_recorded_original_salt(binary_path):
    state = read_state()
    entry = state.get("binaries", {}).get(binary_path)
    return entry["originalSalt"] if entry else None


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


# ============== Web Server ==============
def start_web(args):
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

    @app.route("/api/meta", methods=["GET"])
    def meta():
        detected = detect_binary_salt()
        return jsonify({
            "species": SPECIES, "rarities": RARITIES, "eyes": EYES, "hats": HATS,
            "defaultSalt": DEFAULT_SALT, "detectedUserId": detect_user_id(),
            "binary": {
                "path": detected["filePath"],
                "currentSalt": detected["salt"],
                "saltLength": detected["length"],
                "originalSaltRecorded": get_recorded_original_salt(detected["filePath"]),
            } if detected else None,
        })

    @app.route("/api/preview", methods=["POST"])
    def preview_api():
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "JSON body required"}), 400
            uid = data.get("userId") or detect_user_id() or "anon"
            salt = data.get("salt", DEFAULT_SALT)
            buddy = roll_with_salt(uid, salt)
            return jsonify({
                "userId": uid, "salt": salt, "buddy": buddy,
                "sprite": render_sprite(buddy), "face": render_face(buddy),
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/search", methods=["POST"])
    def search_api():
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "JSON body required"}), 400
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
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/binary", methods=["GET"])
    def binary_api():
        detected = detect_binary_salt()
        if not detected:
            return jsonify({"binary": None})
        return jsonify({
            "binary": {
                "path": detected["filePath"],
                "currentSalt": detected["salt"],
                "saltLength": detected["length"],
                "originalSaltRecorded": get_recorded_original_salt(detected["filePath"]),
            }
        })

    @app.route("/api/apply", methods=["POST"])
    def apply_api():
        try:
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "error": "JSON body required"}), 400
            salt = data.get("salt")
            if not salt:
                return jsonify({"success": False, "error": "Salt required"}), 400

            binary_path = data.get("binaryPath") or find_claude_binary()
            if not binary_path:
                return jsonify({"success": False, "error": "Could not find claude binary."}), 400

            detected = detect_binary_salt(binary_path)
            if not detected:
                return jsonify({"success": False, "error": "Could not detect current salt in Claude Code binary."}), 400

            record_original_salt(detected["filePath"], detected["salt"])
            result = replace_salt_in_binary(detected["salt"], salt, detected["filePath"])
            return jsonify({
                "success": True,
                "filePath": result["filePath"],
                "patchCount": result["patchCount"],
                "oldSalt": detected["salt"],
                "newSalt": salt,
                "originalSaltRecorded": get_recorded_original_salt(detected["filePath"]),
            })

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/api/restore", methods=["POST"])
    def restore_api():
        try:
            data = request.get_json() or {}
            binary_path = data.get("binaryPath") or find_claude_binary()
            if not binary_path:
                return jsonify({"success": False, "error": "Could not find claude binary."}), 400

            original_salt = get_recorded_original_salt(binary_path)
            if not original_salt:
                return jsonify({"success": False, "error": "No recorded original salt found for this binary."}), 400

            detected = detect_binary_salt(binary_path)
            if not detected:
                return jsonify({"success": False, "error": "Could not detect current salt in binary."}), 400

            if detected["salt"] == original_salt:
                return jsonify({"success": True, "message": "Already at original salt.", "patchCount": 0})

            result = replace_salt_in_binary(detected["salt"], original_salt, detected["filePath"])
            return jsonify({
                "success": True,
                "filePath": result["filePath"],
                "patchCount": result["patchCount"],
                "previousSalt": detected["salt"],
                "restoredSalt": original_salt,
            })

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

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


def main():
    args = sys.argv[1:]
    if "-h" in args or "--help" in args:
        print("Claude Buddy Lab - Search, preview, and apply custom buddies\n")
        print("Usage: python3 cli.py [options]\n")
        print("Options:")
        print("  --open          Open browser automatically")
        print("  --port PORT     Server port (default: 8080)")
        print("  --host HOST     Server host (default: 127.0.0.1)")
        return
    start_web(args)


if __name__ == "__main__":
    main()
