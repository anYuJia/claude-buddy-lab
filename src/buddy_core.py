"""
Claude Buddy Lab - Core Buddy Logic

Handles buddy generation, rendering, and search functionality.
Uses the same algorithm as Claude Code for consistent results.
"""

import hashlib
import json
import random
from pathlib import Path
from typing import Any

# Constants
RARITIES = ["common", "uncommon", "rare", "epic", "legendary"]
RARITY_WEIGHTS = {
    "common": 60,
    "uncommon": 25,
    "rare": 10,
    "epic": 4,
    "legendary": 1,
}
SPECIES = [
    "duck",
    "goose",
    "blob",
    "cat",
    "dragon",
    "octopus",
    "owl",
    "penguin",
    "turtle",
    "snail",
    "ghost",
    "axolotl",
    "capybara",
    "cactus",
    "robot",
    "rabbit",
    "mushroom",
    "chonk",
]
EYES = ["·", "✦", "×", "◉", "@", "°"]
HATS = ["none", "crown", "tophat", "propeller", "halo", "wizard", "beanie", "tinyduck"]
STAT_NAMES = ["DEBUGGING", "PATIENCE", "CHAOS", "WISDOM", "SNARK"]
RARITY_FLOOR = {
    "common": 5,
    "uncommon": 15,
    "rare": 25,
    "epic": 35,
    "legendary": 50,
}
DEFAULT_SALT = "friend-2026-401"

# ASCII sprite definitions for each species (3 frames for animation)
BODIES: dict[str, list[list[str]]] = {
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
    "none": "",
    "crown": "   \\^^^/    ",
    "tophat": "   [___]    ",
    "propeller": "    -+-     ",
    "halo": "   (   )    ",
    "wizard": "    /^\\     ",
    "beanie": "   (___)    ",
    "tinyduck": "    ,>      ",
}


def mulberry32(seed: int) -> callable:
    """Mulberry32 PRNG for deterministic random generation."""
    a = seed & 0xFFFFFFFF

    def rng() -> float:
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = ((a ^ (a >> 15)) * (1 | a)) & 0xFFFFFFFF
        t = ((t + ((t ^ (t >> 7)) * (61 | t))) ^ t) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) >> 0) / 4294967296

    return rng


def hash_string(s: str) -> int:
    """FNV-1a hash for string to number conversion."""
    # Use FNV-1a algorithm
    h = 2166136261
    for char in s:
        h ^= ord(char)
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def pick(rng: callable, arr: list) -> Any:
    """Pick a random element from array."""
    return arr[int(rng() * len(arr))]


def roll_rarity(rng: callable) -> str:
    """Roll for rarity based on weights."""
    total = sum(RARITY_WEIGHTS.values())
    roll = rng() * total
    for rarity in RARITIES:
        roll -= RARITY_WEIGHTS[rarity]
        if roll < 0:
            return rarity
    return "common"


def roll_stats(rng: callable, rarity: str) -> dict[str, int]:
    """Generate stats for a buddy."""
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


def roll_with_salt(user_id: str, salt: str) -> dict:
    """
    Generate a buddy from userId and salt.

    Args:
        user_id: User ID from Claude config
        salt: Salt string

    Returns:
        Buddy dictionary with species, rarity, stats, etc.
    """
    rng = mulberry32(hash_string(user_id + salt))
    rarity = roll_rarity(rng)

    return {
        "rarity": rarity,
        "species": pick(rng, SPECIES),
        "eye": pick(rng, EYES),
        "hat": "none" if rarity == "common" else pick(rng, HATS),
        "shiny": rng() < 0.01,
        "stats": roll_stats(rng, rarity),
        "inspirationSeed": int(rng() * 1e9),
    }


def render_sprite(bones: dict, frame: int = 0) -> list[str]:
    """
    Render buddy sprite for a specific frame.

    Args:
        bones: Buddy dictionary
        frame: Frame index (0-2)

    Returns:
        List of lines for the sprite
    """
    frames = BODIES[bones["species"]]
    body = [line.replace("{E}", bones["eye"]) for line in frames[frame % len(frames)]]
    lines = list(body)

    if bones["hat"] != "none" and not lines[0].strip():
        lines[0] = HAT_LINES[bones["hat"]]

    if not lines[0].strip() and all(not f[0].strip() for f in frames):
        lines.pop(0)

    return lines


def sprite_frame_count(species: str) -> int:
    """Get number of frames for a species."""
    return len(BODIES[species])


def render_blink_sprite(bones: dict, frame: int = 0) -> list[str]:
    """Render sprite with blinked eyes."""
    return [line.replace(bones["eye"], "-") for line in render_sprite(bones, frame)]


def render_sprite_frames(bones: dict) -> list[list[str]]:
    """Render all frames for a buddy."""
    count = sprite_frame_count(bones["species"])
    return [render_sprite(bones, i) for i in range(count)]


def render_face(bones: dict) -> str:
    """
    Render buddy face as a single line.

    Args:
        bones: Buddy dictionary

    Returns:
        Face string
    """
    eye = bones["eye"]
    species = bones["species"]

    faces = {
        "duck": f"({eye}>",
        "goose": f"({eye}>",
        "blob": f"({eye}{eye})",
        "cat": f"={eye}ω{eye}=",
        "dragon": f"<{eye}~{eye}>",
        "octopus": f"~({eye}{eye})~",
        "owl": f"({eye})({eye})",
        "penguin": f"({eye}>)",
        "turtle": f"[{eye}_{eye}]",
        "snail": f"{eye}(@)",
        "ghost": f"/{eye}{eye}\\",
        "axolotl": f"}{eye}.{eye}{{",
        "capybara": f"({eye}oo{eye})",
        "cactus": f"|{eye}  {eye}|",
        "robot": f"[{eye}{eye}]",
        "rabbit": f"({eye}..{eye})",
        "mushroom": f"|{eye}  {eye}|",
        "chonk": f"({eye}.{eye})",
    }

    return faces.get(species, species)


def generate_salt(prefix: str, index: int, length: int) -> str:
    """
    Generate salt with prefix and index.

    Args:
        prefix: Salt prefix
        index: Index number
        length: Total salt length

    Returns:
        Generated salt string
    """
    if len(prefix) > length:
        raise ValueError(f"Salt prefix length {len(prefix)} exceeds target length {length}")
    suffix_length = max(0, length - len(prefix))
    return prefix + str(index).zfill(suffix_length)[-suffix_length:]


def parse_min_stat(value: str) -> dict[str, Any] | None:
    """
    Parse min stat filter from CLI argument.

    Args:
        value: e.g., "CHAOS:80"

    Returns:
        Dictionary with name and threshold, or None
    """
    if not value:
        return None

    parts = value.split(":")
    raw_name = parts[0] if len(parts) > 0 else ""
    raw_threshold = parts[1] if len(parts) > 1 else ""

    name = raw_name.strip().upper()
    threshold = float(raw_threshold) if raw_threshold else 0

    if name not in STAT_NAMES or not (0 < threshold <= 100):
        raise ValueError(f"Invalid min stat value: {value}")

    return {"name": name, "threshold": int(threshold)}


def matches_filters(result: dict, filters: dict) -> bool:
    """
    Check if buddy matches search filters.

    Args:
        result: Buddy dictionary
        filters: Search filters

    Returns:
        True if matches all filters
    """
    if filters.get("species") and result["species"] != filters["species"]:
        return False
    if filters.get("rarity") and result["rarity"] != filters["rarity"]:
        return False
    if filters.get("eye") and result["eye"] != filters["eye"]:
        return False
    if filters.get("hat") and result["hat"] != filters["hat"]:
        return False
    if filters.get("shiny") and not result["shiny"]:
        return False
    if filters.get("min_stat"):
        min_stat = filters["min_stat"]
        if result["stats"][min_stat["name"]] < min_stat["threshold"]:
            return False
    return True


def search_salts(
    user_id: str,
    total: int = 100000,
    prefix: str = "lab-",
    length: int = len(DEFAULT_SALT),
    filters: dict | None = None,
    max_matches: int = 20,
) -> list[dict]:
    """
    Search for salts that produce matching buddies.

    Args:
        user_id: User ID
        total: Number of salts to try
        prefix: Salt prefix
        length: Salt length
        filters: Search filters
        max_matches: Maximum matches to return

    Returns:
        List of {salt, buddy} dictionaries
    """
    filters = filters or {}
    matches = []

    for i in range(total):
        salt = generate_salt(prefix, i, length)
        result = roll_with_salt(user_id, salt)
        if matches_filters(result, filters):
            matches.append({"salt": salt, "buddy": result})
            if len(matches) >= max_matches:
                break

    return matches


def detect_user_id() -> str | None:
    """
    Detect user ID from Claude config file.

    Returns:
        User ID if found, None otherwise
    """
    home = Path.home()
    candidates = [
        home / ".claude" / ".config.json",
        home / ".claude.json",
    ]

    for candidate in candidates:
        if candidate.exists():
            try:
                with open(candidate, "r") as f:
                    config = json.load(f)

                user_id = (
                    config.get("oauthAccount", {}).get("accountUuid")
                    or config.get("userID")
                )
                if user_id:
                    return user_id
            except (json.JSONDecodeError, IOError):
                continue

    return None
