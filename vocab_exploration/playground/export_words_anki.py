#!/usr/bin/env python3
# export_anki_deck.py
import argparse, json, re, html, sys
from typing import Any, Dict, List
import requests

def invoke(url: str, version: int, action: str, **params) -> Any:
    r = requests.post(url, json={"action": action, "version": version, "params": params})
    r.raise_for_status()
    data = r.json()
    if data.get("error"):
        raise RuntimeError(f"AnkiConnect error on {action}: {data['error']}")
    return data["result"]

def strip_html(s: str) -> str:
    if s is None:
        return ""
    # remove scripts/styles, tags, collapse whitespace, unescape entities
    s = re.sub(r"(?is)<(script|style).*?>.*?</\1>", "", s)
    s = re.sub(r"(?s)<[^>]+>", "", s)
    s = html.unescape(s)
    s = s.replace("\xa0", " ")
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()

def get_fields(c: Dict[str, Any]) -> Dict[str, Any]:
    try:
        front = c["fields"]["Front"]["value"]
        back = c["fields"]["Back"]["value"]
        return {
            "front": strip_html(front),
            "back": strip_html(back)
        }
    except KeyError:
        return {
            "front": None,
            "back": None
        }

def export_deck(url: str, version: int, deck_name: str) -> List[Dict[str, Any]]:
    # Quote the deck name safely for the browser query language
    q = f'deck:"{deck_name.replace(chr(34), r"\"")}"'
    card_ids = invoke(url, version, "findCards", query=q)
    if not card_ids:
        return []

    # cardsInfo returns rendered question/answer (HTML) + metadata
    cards = invoke(url, version, "cardsInfo", cards=card_ids)

    out = []
    for c in cards:
        front_and_back = get_fields(c)
        out.append({
            "deck": c.get("deckName"),
            "card_id": c.get("cardId"),
            "note_id": c.get("noteId"),
            "model": c.get("modelName"),
            "front": front_and_back["front"],
            "back": front_and_back["back"]
        })
    return out

def main():
    ap = argparse.ArgumentParser(description="Export all cards in an Anki deck as JSON (front/back text).")
    ap.add_argument("deck", help='Deck name, e.g. "Default" or "My::Subdeck"')
    ap.add_argument("-o", "--output", help="Write to file (default: stdout)")
    ap.add_argument("--url", default="http://localhost:8765", help="AnkiConnect URL (default: %(default)s)")
    ap.add_argument("--version", type=int, default=6, help="AnkiConnect API version (default: %(default)s)")
    args = ap.parse_args()

    try:
        data = export_deck(args.url, args.version, args.deck)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
