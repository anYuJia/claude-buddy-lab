"""
Claude Buddy Lab - Command Line Interface

Usage:
    buddy preview                    # Preview current buddy
    buddy search --species owl       # Search for specific species
    buddy apply --salt <salt>        # Apply a salt
    buddy web                        # Start web interface
"""

import json
import sys
import os
from pathlib import Path

import click

from buddy_core import (
    DEFAULT_SALT,
    SPECIES,
    RARITIES,
    EYES,
    HATS,
    STAT_NAMES,
    roll_with_salt,
    render_sprite,
    render_face,
    search_salts,
    parse_min_stat,
    detect_user_id,
)


def get_user_id() -> str:
    """Detect user ID from Claude config."""
    user_id = detect_user_id()
    if user_id:
        return user_id
    return "anon"


def print_buddy(buddy: dict, salt: str, user_id: str):
    """Print buddy to console."""
    click.echo(f"\n{'='*50}")
    click.echo(f"Salt: {salt}")
    click.echo(f"User ID: {user_id}")
    click.echo(f"Species: {buddy['species'].capitalize()}")
    click.echo(f"Rarity: {buddy['rarity'].capitalize()}")
    click.echo(f"Eye: {buddy['eye']}")
    click.echo(f"Hat: {buddy['hat']}")
    click.echo(f"Shiny: {'Yes ✦' if buddy['shiny'] else 'No'}")
    click.echo(f"\nStats:")
    for stat, value in buddy["stats"].items():
        bar = "█" * (value // 5)
        click.echo(f"  {stat:12} {bar} {value}")
    click.echo(f"\nSprite:\n")
    for line in render_sprite(buddy):
        click.echo(line)
    click.echo(f"\nFace: {render_face(buddy)}")
    click.echo(f"{'='*50}\n")


@click.group()
@click.version_option(version="1.0.0")
def main():
    """Claude Buddy Lab - Search, preview, and customize your buddy."""
    pass


@main.command()
@click.option("--salt", default=DEFAULT_SALT, help="Salt to preview")
@click.option("--user-id", help="User ID (auto-detected if not provided)")
def preview(salt: str, user_id: str):
    """Preview a buddy for a given salt."""
    if not user_id:
        user_id = get_user_id()
        if user_id == "anon":
            click.echo("Warning: Could not detect user ID, using 'anon'")

    buddy = roll_with_salt(user_id, salt)
    print_buddy(buddy, salt, user_id)


@main.command()
@click.option("--species", type=click.Choice(SPECIES), help="Filter by species")
@click.option("--rarity", type=click.Choice(RARITIES), help="Filter by rarity")
@click.option("--eye", type=click.Choice(EYES), help="Filter by eye type")
@click.option("--hat", type=click.Choice(HATS), help="Filter by hat")
@click.option("--shiny", is_flag=True, help="Only show shiny buddies")
@click.option("--min-stat", help="Minimum stat (e.g., CHAOS:80)")
@click.option("--total", default=100000, help="Number of salts to search")
@click.option("--prefix", default="lab-", help="Salt prefix")
@click.option("--user-id", help="User ID (auto-detected if not provided)")
def search(
    species: str,
    rarity: str,
    eye: str,
    hat: str,
    shiny: bool,
    min_stat: str,
    total: int,
    prefix: str,
    user_id: str,
):
    """Search for buddies matching criteria."""
    if not user_id:
        user_id = get_user_id()
        if user_id == "anon":
            click.echo("Warning: Could not detect user ID, using 'anon'")

    filters = {
        "species": species,
        "rarity": rarity,
        "eye": eye,
        "hat": hat,
        "shiny": shiny,
    }

    if min_stat:
        try:
            filters["min_stat"] = parse_min_stat(min_stat)
        except ValueError as e:
            raise click.ClickException(str(e))

    click.echo(f"Searching for buddies...")
    click.echo(f"  User ID: {user_id}")
    click.echo(f"  Filters: {filters}")
    click.echo(f"  Max attempts: {total}")
    click.echo()

    matches = search_salts(
        user_id=user_id,
        total=total,
        prefix=prefix,
        filters=filters or None,
        max_matches=20,
    )

    if not matches:
        click.echo("No matches found. Try increasing --total or relaxing filters.")
        return

    click.echo(f"Found {len(matches)} matches:\n")

    for i, match in enumerate(matches, 1):
        buddy = match["buddy"]
        salt = match["salt"]
        click.echo(f"{i}. {buddy['rarity'].capitalize()} {buddy['species'].capitalize()}")
        click.echo(f"   Salt: {salt}")
        click.echo(f"   Eye: {buddy['eye']} | Hat: {buddy['hat']} | Shiny: {'✦' if buddy['shiny'] else ' '}")
        top_stat = max(buddy["stats"].items(), key=lambda x: x[1])
        click.echo(f"   Top stat: {top_stat[0]} {top_stat[1]}")
        click.echo()


@main.command()
@click.argument("salt")
def apply(salt: str):
    """
    Apply a salt to Claude Code binary.

    Note: This modifies your Claude Code installation.
    Use with caution and backup first.
    """
    click.echo("Applying salt is not yet implemented in this version.")
    click.echo("Please use the web interface: buddy web")


@main.command()
@click.option("--host", default="127.0.0.1", help="Host to bind to")
@click.option("--port", default=8080, help="Port to bind to")
@click.option("--open-browser", is_flag=True, help="Open browser automatically")
def web(host: str, port: int, open_browser: bool):
    """Start the web interface."""
    click.echo(f"Starting web interface at http://{host}:{port}")
    click.echo("Press Ctrl+C to stop")

    # Import flask here to avoid dependency if not using web
    try:
        from flask import Flask, send_from_directory, jsonify, request
    except ImportError:
        raise click.ClickException(
            "Flask is required for web mode. Install with: pip install flask"
        )

    app = Flask(__name__, static_folder="../public", static_url_path="")
    config_dir = Path(__file__).parent.parent / "config"
    config_dir.mkdir(exist_ok=True)
    state_file = config_dir / "state.json"

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/api/meta")
    def meta():
        try:
            detected_user_id = get_user_id()
        except click.ClickException:
            detected_user_id = None

        return jsonify({
            "species": SPECIES,
            "rarities": RARITIES,
            "eyes": EYES,
            "hats": HATS,
            "stats": STAT_NAMES,
            "defaultSalt": DEFAULT_SALT,
            "detectedUserId": detected_user_id,
        })

    @app.route("/api/preview", methods=["POST"])
    def preview_api():
        data = request.json
        user_id = data.get("userId") or get_user_id()
        salt = data.get("salt", DEFAULT_SALT)

        buddy = roll_with_salt(user_id, salt)
        sprite = render_sprite(buddy)
        face = render_face(buddy)

        return jsonify({
            "userId": user_id,
            "salt": salt,
            "buddy": buddy,
            "sprite": sprite,
            "face": face,
        })

    @app.route("/api/search", methods=["POST"])
    def search_api():
        data = request.json
        user_id = data.get("userId") or get_user_id()
        filters = {
            "species": data.get("species"),
            "rarity": data.get("rarity"),
            "eye": data.get("eye"),
            "hat": data.get("hat"),
            "shiny": data.get("shiny", False),
        }

        if data.get("minStat"):
            try:
                filters["min_stat"] = parse_min_stat(data["minStat"])
            except ValueError:
                pass

        total = data.get("total", 100000)
        prefix = data.get("prefix", "lab-")

        matches = search_salts(
            user_id=user_id,
            total=total,
            prefix=prefix,
            filters=filters or None,
            max_matches=20,
        )

        # Add sprite and face to each match
        for match in matches:
            match["sprite"] = render_sprite(match["buddy"])
            match["face"] = render_face(match["buddy"])

        return jsonify({
            "matches": matches,
            "searched": min(total, len(matches)),
        })

    import webbrowser
    import threading

    if open_browser:
        threading.Timer(1, lambda: webbrowser.open(f"http://{host}:{port}")).start()

    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()
