#!/usr/bin/env python3
"""Scrape the first sense of German words from Cambridge German–English.

Fetches through Cambridge's direct search (handles umlauts, ß and phrases),
caches HTML in `cache/`, and parses grammar + the first sense into gold JSON.
"""

import argparse
import json
import re
import time
import urllib.parse
from pathlib import Path
from typing import Any

import httpx
from bs4 import BeautifulSoup, Tag

EVAL_DIR = Path(__file__).resolve().parent
CACHE_DIR = EVAL_DIR / "cache"
SEARCH_URL = "https://dictionary.cambridge.org/search/direct/?datasetsearch=german-english&q="
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130 Safari/537.36"
)
REQUEST_DELAY_SECONDS = 1.0
GENDER_TO_ARTICLE = {
    "masculine": "der",
    "feminine": "die",
    "neuter": "das",
    "masculine-feminine": "der/die",
}

EMPTY_GRAMMAR = {
    "article": "",
    "uncountable": False,
    "genitive": "",
    "plural": "",
    "praesens_3sg": "",
    "praeteritum": "",
    "partizip_2": "",
}


def clean(text: str) -> str:
    """Collapse whitespace and drop spaces before punctuation."""
    text = re.sub(r"\s+", " ", text).strip()
    return re.sub(r"\s+([,.!?;:])", r"\1", text)


def cache_path(query: str) -> Path:
    slug = re.sub(r"[^\w-]+", "_", query.lower()).strip("_")
    return CACHE_DIR / f"{slug}.html"


def fetch_html(query: str) -> str:
    """Return the Cambridge page for a query, using the on-disk cache."""
    path = cache_path(query)
    if path.exists():
        return path.read_text(encoding="utf-8")

    url = SEARCH_URL + urllib.parse.quote(query)
    response = httpx.get(
        url, headers={"User-Agent": USER_AGENT}, follow_redirects=True, timeout=30
    )
    response.raise_for_status()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(response.text, encoding="utf-8")
    time.sleep(REQUEST_DELAY_SECONDS)
    return response.text


def parse_inflections(head: Tag) -> dict[str, str]:
    """Map Cambridge inflection labels (e.g. 'nominative plural') to forms."""
    forms: dict[str, str] = {}
    for group in head.select(".inf-group"):
        label = " ".join(lab.get_text(strip=True) for lab in group.select(".lab"))
        form = group.select_one(".inf")
        if form and label not in forms:
            forms[label] = clean(form.get_text())
    return forms


def parse_head(head: Tag) -> dict[str, Any]:
    """Parse headword, POS, gender and inflections from an entry header."""
    pos = head.select_one(".pos")
    grams = [clean(g.get_text()) for g in head.select(".gc")]
    gender = next((g for g in grams if g in GENDER_TO_ARTICLE), "")
    forms = parse_inflections(head)
    return {
        "headword": clean(head.select_one(".di-title").get_text()),
        "pos": clean(pos.get_text()) if pos else "",
        "article": GENDER_TO_ARTICLE.get(gender, ""),
        "uncountable": "uncountable" in grams,
        "genitive": forms.get("genitive singular", ""),
        "plural": forms.get("nominative plural", ""),
        "praesens_3sg": forms.get("3rd singular present", ""),
        "praeteritum": forms.get("3rd singular preterit", ""),
        "partizip_2": forms.get("past participle", ""),
    }


def parse_examples(def_block: Tag) -> list[dict[str, str]]:
    examples = []
    for example in def_block.select(".examp"):
        german = example.select_one(".eg")
        english = example.select_one(".trans")
        examples.append(
            {
                "de": clean(german.get_text()) if german else "",
                "en": clean(english.get_text()) if english else "",
            }
        )
    return examples


def parse_translations(def_block: Tag) -> list[str]:
    """Return English translations that belong to the sense, not to examples."""
    body = def_block.select_one(".def-body")
    if body is None:
        return []
    direct = body.find_all("span", class_="trans", recursive=False)
    translations = [clean(span.get_text()) for span in direct]
    return [t for t in translations if t and t != ","]


def parse_sense(def_block: Tag) -> dict[str, Any]:
    """Parse one Cambridge sense (definition block)."""
    definition = def_block.select_one(".def")
    info = def_block.select_one(".def-info")
    info_text = clean(info.get_text(" ")) if info else ""
    return {
        "definition_de": clean(definition.get_text()) if definition else "",
        "translations_en": parse_translations(def_block),
        "perfekt_mit_sein": "Perfekt mit sein" in info_text,
        "sense_info": info_text.replace("●", "").strip(),
        "examples": parse_examples(def_block),
    }


def find_phrase_block(dictionary: Tag, query: str) -> Tag | None:
    """Find a phrase block whose title contains every word of the query."""
    query_words = set(query.lower().split())
    for block in dictionary.select(".phrase-block"):
        title = block.select_one(".phrase-title")
        title_words = set(clean(title.get_text()).lower().replace("/", " ").split())
        if query_words <= title_words:
            return block
    return None


def find_dictionary(soup: BeautifulSoup, name: str) -> Tag | None:
    """Return the dictionary block whose attribution mentions `name`."""
    for dictionary in soup.select(".pr.dictionary"):
        if name in dictionary.get_text() and dictionary.select_one(".def-block"):
            return dictionary
    return None


def parse_password_page(dictionary: Tag, query: str) -> dict[str, Any]:
    """PASSWORD entries only carry English translations (no German grammar)."""
    translations = [clean(t.get_text()) for t in dictionary.select(".def-block .trans")]
    return {
        "query": query,
        "found": True,
        "source": "password",
        "match": "translation_only",
        "headword": clean(dictionary.select_one(".di-title").get_text()),
        "translations_en": list(dict.fromkeys(t for t in translations if t)),
    }


def parse_global_page(dictionary: Tag, query: str) -> dict[str, Any]:
    """Parse grammar and the first sense of the best-matching GLOBAL entry."""
    head = parse_head(dictionary.select_one(".di-head"))
    exact = head["headword"].lower() == query.lower()
    phrase_block = None if exact else find_phrase_block(dictionary, query)
    sense_source = phrase_block or dictionary
    first_def_block = sense_source.select_one(".def-block")

    match = "exact" if exact else "phrase" if phrase_block else "approximate"
    if phrase_block:
        phrase_title = clean(phrase_block.select_one(".phrase-title").get_text())
        head = {**EMPTY_GRAMMAR, "headword": phrase_title, "pos": "phrase"}

    return {
        "query": query,
        "found": True,
        "source": "global",
        "match": match,
        **head,
        **parse_sense(first_def_block),
    }


def parse_page(html: str, query: str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")
    if dictionary := find_dictionary(soup, "GLOBAL German–English"):
        return parse_global_page(dictionary, query)
    if dictionary := find_dictionary(soup, "PASSWORD German–English"):
        return parse_password_page(dictionary, query)
    return {"query": query, "found": False}


def scrape(query: str) -> dict[str, Any]:
    return parse_page(fetch_html(query), query)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("words", nargs="*", help="Words/phrases to look up")
    parser.add_argument("--input", type=Path, help="JSON list of {'word': ...}")
    parser.add_argument("--output", type=Path, help="Where to write gold JSON")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    words = list(args.words)
    if args.input:
        words += [entry["word"] for entry in json.loads(args.input.read_text())]

    results = [scrape(word) for word in words]
    payload = json.dumps(results, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
        print(f"Wrote {len(results)} entries to {args.output}")
    else:
        print(payload)


if __name__ == "__main__":
    main()
