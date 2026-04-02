# 🧪 Claude Buddy Lab

**Search, preview, and customize your Claude Code buddy companion**

---

## 🚀 Quick Start

```bash
# Clone and run directly - no installation needed!
git clone https://github.com/yourusername/claude-buddy-lab.git
cd claude-buddy-lab

# Preview your current buddy
python3 cli.py preview

# Start interactive terminal interface
python3 cli.py interactive

# Start web interface
python3 cli.py web
```

That's it! No pip install required.

---

## 💻 Usage

### CLI Commands

```bash
# Preview current buddy (auto-detects user ID)
python3 cli.py preview

# Preview with custom salt
python3 cli.py preview --salt my-custom-salt

# Interactive terminal interface (NEW!)
python3 cli.py interactive

# Controls in interactive mode:
#   n/→  Next buddy
#   p/←  Previous buddy
#   r    Re-roll
#   c    Change filters
#   a    Apply salt
#   q    Quit

# Search for specific species
python3 cli.py search --species owl --rarity epic

# Search for shiny buddies
python3 cli.py search --shiny --total 1000000

# Search with minimum stat
python3 cli.py search --species dragon --min-stat CHAOS:80

# Start web interface
python3 cli.py web

# Web interface with auto-open browser
python3 cli.py web --open
```

### Options

| Option | Values | Description |
|--------|--------|-------------|
| `--species` | duck, goose, blob, cat, dragon, octopus, owl, penguin, turtle, snail, ghost, axolotl, capybara, cactus, robot, rabbit, mushroom, chonk | Filter by species |
| `--rarity` | common, uncommon, rare, epic, legendary | Filter by rarity |
| `--eye` | ·, ✦, ×, ◉, @, ° | Filter by eye type |
| `--hat` | none, crown, tophat, propeller, halo, wizard, beanie, tinyduck | Filter by hat |
| `--shiny` | (flag) | Only show shiny buddies (1% chance) |
| `--min-stat` | STAT:value | Minimum stat value (e.g., CHAOS:80) |
| `--total` | number | Number of salts to search (default: 100000) |

---

## 🌐 Web Interface

```bash
python3 cli.py web
# Open http://127.0.0.1:8080
```

Features:
- Auto-detects your Claude user ID
- Visual preview with ASCII art
- Interactive search with filters
- Results gallery

---

## 🔧 Requirements

- Python 3.8+
- Flask (optional, for web mode): `pip3 install flask`

---

## 📁 Files

```
claude-buddy-lab/
├── cli.py          # Main script (run this!)
├── public/
│   └── index.html  # Web interface
├── README.md
├── LICENSE
└── .gitignore
```

---

## ❓ FAQ

**Q: Why do I get different results than others with the same salt?**

A: Results depend on `userId + salt`. Different users have different userIds.

**Q: How do I apply a buddy to Claude Code?**

A: This tool is for preview/search only. Applying requires binary modification (not included).

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

**Built with ❤️ using Python**
