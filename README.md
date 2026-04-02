# \ud83e\uddea Claude Buddy Lab

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Search, preview, and customize your Claude Code buddy companion**

Claude Buddy Lab is a tool for Claude Code users to search, preview, and customize their AI companion pet (buddy). Find the perfect buddy with your preferred species, rarity, and stats!

---

## \ud83c\udf1f Features

- **\ud83d\udd0d Search**: Find buddies by species, rarity, eye type, hat, or stats
- **\ud83d\udc41\ufe0f Preview**: See ASCII art preview of your buddy before applying
- **\ud83c\udfa8 Shiny Hunting**: Filter for rare shiny buddies (1% chance)
- **\ud83d\udcbb Web Interface**: Beautiful browser-based UI
- **\ud83d\ude80 CLI**: Command-line interface for quick searches
- **\ud83d\udd12 Safe**: Auto-detects your user ID, non-destructive preview

---

## \ud83d\ude80 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/claude-buddy-lab.git
cd claude-buddy-lab

# Install with pip
pip install -e .

# Or install dependencies directly
pip install -r requirements.txt
```

### Web Interface (Recommended)

```bash
# Start the web server
buddy web

# Or run directly
python -m src.cli web
```

Then open http://127.0.0.1:8080 in your browser.

### CLI Commands

```bash
# Preview current buddy
buddy preview

# Preview with custom salt
buddy preview --salt friend-2026-401

# Search for specific species
buddy search --species owl --rarity epic

# Search for shiny buddies
buddy search --shiny --total 1000000

# Search with minimum stat requirement
buddy search --species dragon --min-stat CHAOS:80

# Full help
buddy --help
buddy search --help
```

---

## \ud83c\udfae Usage

### Web Interface

1. **Auto-detection**: The page automatically detects your Claude user ID
2. **Preview**: Click "Preview Buddy" to see your current companion
3. **Search**: Set filters (species, rarity, etc.) and click "Search"
4. **Apply**: Click "Preview This" on any result to see it in detail

### CLI Examples

```bash
# Find all legendary dragons
buddy search --species dragon --rarity legendary

# Find a shiny with high CHAOS stat
buddy search --shiny --min-stat CHAOS:90 --total 2000000

# Find cat with specific eye type
buddy search --species cat --eye '\u2726' --rarity rare
```

### Available Options

| Option | Values | Description |
|--------|--------|-------------|
| `--species` | duck, goose, blob, cat, dragon, octopus, owl, penguin, turtle, snail, ghost, axolotl, capybara, cactus, robot, rabbit, mushroom, chonk | Filter by species |
| `--rarity` | common, uncommon, rare, epic, legendary | Filter by rarity |
| `--eye` | \u00b7, \u2726, \u00d7, \u25c9, @, \u00b0 | Filter by eye type |
| `--hat` | none, crown, tophat, propeller, halo, wizard, beanie, tinyduck | Filter by hat |
| `--shiny` | (flag) | Only show shiny buddies (1% chance) |
| `--min-stat` | STAT:value | Minimum stat value (e.g., CHAOS:80) |
| `--total` | number | Number of salts to search (default: 100000) |
| `--prefix` | string | Salt prefix (default: lab-) |

---

## \ud83e\udde0 How It Works

### Buddy Generation Algorithm

Each buddy is deterministically generated from your `userId + salt` combination:

```
userId (from ~/.claude/.config.json)
   +
salt (default: 'friend-2026-401')
   \u2193
SHA-like hash \u2192 PRNG seed
   \u2193
Roll for: rarity \u2192 species \u2192 eye \u2192 hat \u2192 shiny \u2192 stats
```

### Rarity Distribution

| Rarity | Weight | Min Stats |
|--------|--------|-----------|
| Common | 60% | 5 |
| Uncommon | 25% | 15 |
| Rare | 10% | 25 |
| Epic | 4% | 35 |
| Legendary | 1% | 50 |

### Stats

Each buddy has 5 stats (0-100):
- **DEBUGGING**: Bug-fixing prowess
- **PATIENCE**: Tolerance for slow developers
- **CHAOS**: Mischief level
- **WISDOM**: Code review insight
- **SNARK**: Sarcasm intensity

---

## \u2753 FAQ

### Why do I get different results than others with the same salt?

Results depend on `userId + salt`, not just the salt. Different users have different userIds, so the same salt produces different buddies.

### How do I apply a buddy to Claude Code?

Currently, this tool is for preview and search only. To apply a buddy, you would need to modify the Claude Code binary directly (not recommended).

### Can I share my buddy with others?

Share your `userId` and `salt` so others can see the same buddy with their own userId.

### What if I can't find any matches?

Try:
1. Increasing `--total` (more search attempts)
2. Relaxing filters (remove some constraints)
3. Searching for more common species/rarities

---

## \ud83d\udcbb Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
ruff check src/
```

---

## \ud83d\udee3\ufe0f Roadmap

- [ ] Binary modification for applying buddies
- [ ] State management for tracking original salt
- [ ] Restore functionality
- [ ] More search filters (stat combinations, etc.)
- [ ] Export/import buddy configurations
- [ ] Community buddy showcase

---

## \ud83d\udcdd License

MIT License - see [LICENSE](LICENSE) for details.

---

## \ud83d\ude4f Acknowledgments

- Claude Code team for the original buddy feature
- ASCII art inspired by terminal culture

---

**Built with \u2764\ufe0f using Python + Flask**
