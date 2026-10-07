"""Turn enriched German entries into Anki notes with separate fields, packaged as .apkg.

The note type ("German Vocab") has one field per piece of information, so card
layout lives in Anki (edit it there) — the default templates are in anki/.
Note IDs are derived from the source word, so re-importing updates notes
instead of duplicating them.
"""

import hashlib
from pathlib import Path
from typing import Any

import genanki

from formatting import grammar_line, grammar_tags, headword

ANKI_DIR = Path(__file__).resolve().parent / "anki"
NOTE_TYPE_NAME = "German Vocab (vocab-extension)"

# Order = field order in Anki. The first field is the sort/duplicate-check field.
FIELD_NAMES = (
    "word_de",
    "article",
    "headword",
    "word_audio",
    "word_en",
    "pos",
    "grammar",
    "plural",
    "genitive",
    "praesens_3sg",
    "praeteritum",
    "partizip_2",
    "auxiliary",
    "perfekt",
    "separable",
    "reflexive",
    "comparative",
    "superlative",
    "definition_en",
    "definition_de",
    "example1_de",
    "example1_en",
    "example1_audio",
    "example2_de",
    "example2_en",
    "example2_audio",
    "source_word",
)
SOUND_FIELDS = ("word_audio", "example1_audio", "example2_audio")


def stable_id(name: str) -> int:
    """Deterministic 31-bit id, so re-imports hit the same note type / deck."""
    return int(hashlib.sha1(name.encode()).hexdigest()[:8], 16) >> 1


def example_fields(examples: list[dict[str, str]]) -> dict[str, str]:
    fields = {}
    for number in (1, 2):
        example = examples[number - 1] if len(examples) >= number else {"de": "", "en": ""}
        fields[f"example{number}_de"] = example["de"]
        fields[f"example{number}_en"] = example["en"]
    return fields


def to_note_record(entry: dict[str, Any], base_tags: list[str]) -> dict[str, Any]:
    """Flatten one enriched entry into note fields (+ bookkeeping keys for the pipeline)."""
    grammar_keys = (
        "article", "pos", "plural", "genitive", "praesens_3sg", "praeteritum",
        "partizip_2", "auxiliary", "perfekt", "comparative", "superlative",
    )
    return {
        "word": entry["word"],
        "tts_text": entry["tts_text"],
        "tags": [*base_tags, *grammar_tags(entry)],
        "entry": entry,
        "word_de": entry["lemma"],
        "headword": headword(entry),
        "word_en": entry["word_en"],
        "grammar": grammar_line(entry),
        **{key: entry[key] for key in grammar_keys},
        "separable": "trennbar" if entry["separable"] else "",
        "reflexive": "reflexiv" if entry["reflexive"] else "",
        "definition_en": entry["definition_en"],
        "definition_de": entry["definition_de"],
        **example_fields(entry["examples"]),
        "source_word": entry["word"],
    }


def audio_path_key(sound_field: str) -> str:
    """"example1_audio" → "example1_audio_relative_path" (key written by audio_component)."""
    return f"{sound_field}_relative_path"


def with_sound_fields(record: dict[str, Any]) -> dict[str, Any]:
    """Fill `*_audio` fields as `[sound:file.mp3]` from the audio component's path keys."""
    sounds = {}
    for field in SOUND_FIELDS:
        path = record.get(audio_path_key(field))
        sounds[field] = f"[sound:{path}]" if path else ""
    return {**record, **sounds}


def build_note_type() -> genanki.Model:
    return genanki.Model(
        stable_id(NOTE_TYPE_NAME),
        NOTE_TYPE_NAME,
        fields=[{"name": name} for name in FIELD_NAMES],
        templates=[
            {
                "name": "English → German",
                "qfmt": (ANKI_DIR / "front.html").read_text(encoding="utf-8"),
                "afmt": (ANKI_DIR / "back.html").read_text(encoding="utf-8"),
            }
        ],
        css=(ANKI_DIR / "style.css").read_text(encoding="utf-8"),
    )


def build_note(note_type: genanki.Model, record: dict[str, Any]) -> genanki.Note:
    return genanki.Note(
        model=note_type,
        fields=[str(record[name]) for name in FIELD_NAMES],
        tags=record["tags"],
        guid=genanki.guid_for("vocab-extension-de", record["word"]),
    )


def write_apkg(records: list[dict[str, Any]], deck_name: str, media_dir: Path, path: Path) -> int:
    """Write deck + note type + notes + audio into one .apkg; returns the number of notes."""
    note_type = build_note_type()
    deck = genanki.Deck(stable_id(deck_name), deck_name)
    for record in records:
        deck.add_note(build_note(note_type, record))

    referenced = {
        record[audio_path_key(field)]
        for record in records
        for field in SOUND_FIELDS
        if record.get(audio_path_key(field))
    }
    media_files = [str(media_dir / name) for name in sorted(referenced)]
    genanki.Package(deck, media_files=media_files).write_to_file(str(path))
    return len(deck.notes)
