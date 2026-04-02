<div align="center">

# 🧪 Claude Buddy Lab

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Web_UI-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge)](LICENSE)

Every Claude Code user has a unique ASCII buddy companion in the terminal.
It's deterministically generated from `hash(userId + salt)` — different salts produce
entirely different species, rarities, stats, and appearances.
But this salt is hardcoded in the Claude Code binary, normally impossible to change.

**This tool provides a visual web interface to brute-force search millions of salt combinations,
live-preview the buddy each salt produces, and patch your chosen one into the binary with one click.**

Filter by species, rarity, eyes, hat, shiny status, and restore to the original buddy anytime.

[中文](README.md)

---

<img src="img/web-preview.png" width="720">

</div>

## Quick Start

```bash
git clone https://github.com/anYuJia/claude-buddy-lab.git
cd claude-buddy-lab
pip3 install flask
python3 cli.py --open
```

<div align="center">

| Search Results | In Claude Code |
|:---:|:---:|
| <img src="img/search-results.png" width="420"> | <img src="img/buddy-in-claude.png" width="260"> |

</div>

## How It Works

> Buddy = `hash(userId + salt)` — the salt is hardcoded in the Claude binary.

1. **Search** — iterate through millions of salts, filter matches by your criteria
2. **Preview** — view ASCII sprite, stat panel, rarity and shiny status in the web UI
3. **Patch** — locate the old salt bytes in the binary, replace with the new salt (same length)
4. **Sign** — automatically re-sign on macOS (`codesign`)
5. **Record** — original salt saved to `~/.claude-buddy-lab.json` for easy restoration

## API

```
GET  /api/meta       — metadata + binary status
GET  /api/binary     — current salt detection
POST /api/preview    — preview a buddy
POST /api/search     — search with filters
POST /api/apply      — patch binary
POST /api/restore    — revert to original
```

<div align="center">

---

MIT License

</div>
