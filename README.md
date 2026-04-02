<div align="center">

# 🧪 Claude Buddy Lab

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Web_UI-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge)](LICENSE)

**Search, preview, and apply custom buddies to Claude Code**

**Binary patching. One click. Done.**

[中文](README_CN.md)

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

This tool searches millions of salts, finds the one you want, and patches it in.

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
