# Claude Buddy Lab

**Search, preview, and apply custom buddies to Claude Code — with binary patching.**

[中文文档](README_CN.md)

<p align="center">
  <img src="img/web-preview.png" width="720" alt="Web UI">
</p>

## Features

- **Binary Patching** — Directly patches the Claude Code binary. No config file hacks.
- **Search** — Brute-force millions of salts to find the exact buddy you want.
- **Live Preview** — ASCII sprite, stats, rarity, shiny — all visible before applying.
- **One-Click Apply** — Apply from the web UI. Original salt recorded for restoration.
- **Bilingual** — Auto-detects browser language (English / Chinese).
- **Restore** — Revert to default buddy at any time.

## Screenshots

| Web UI | Search Results | In Claude Code |
|:---:|:---:|:---:|
| ![Web UI](img/web-preview.png) | ![Search](img/search-results.png) | ![Buddy](img/buddy-in-claude.png) |

## Quick Start

```bash
git clone https://github.com/anYuJia/claude-buddy-lab.git
cd claude-buddy-lab
pip3 install flask

# Start (auto-open browser)
python3 cli.py --open
```

Open http://127.0.0.1:8080 — search for your dream buddy, preview it, click **Apply**.

### Options

```bash
python3 cli.py                # Start server
python3 cli.py --open         # Start and open browser
python3 cli.py --port 9090    # Custom port
python3 cli.py --host 0.0.0.0 # Listen on all interfaces
```

## How It Works

Claude Code's buddy is determined by `hash(userId + salt)`. The salt (`friend-2026-401`, 15 chars) is hardcoded in the binary.

This tool:
1. **Searches** millions of salt values to find one that produces your desired buddy
2. **Patches** the binary — replaces the old salt bytes with the new one (same length)
3. **Re-signs** the binary on macOS (`codesign`)
4. **Records** the original salt to `~/.claude-buddy-lab.json` for restoration

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/meta` | Metadata + binary status |
| GET | `/api/binary` | Current binary salt |
| POST | `/api/preview` | Preview buddy for userId + salt |
| POST | `/api/search` | Search salts with filters |
| POST | `/api/apply` | Patch binary with new salt |
| POST | `/api/restore` | Restore original salt |

## Requirements

- Python 3.8+
- Flask: `pip3 install flask`
- Claude Code installed

## License

MIT
