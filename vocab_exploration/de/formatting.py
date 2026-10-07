"""Human-readable formatting of enriched German entries (shared by markdown + cards)."""

from typing import Any

NO_PLURAL = "nur Singular"


def headword(entry: dict[str, Any]) -> str:
    """Noun with article ("der Bauch"), otherwise the lemma."""
    if entry["pos"] == "noun" and entry["article"]:
        return f"{entry['article']} {entry['lemma']}"
    return entry["lemma"]


def noun_forms(entry: dict[str, Any], with_genitive: bool = False) -> str:
    """"die Bäuche" or "nur Singular"; optionally "die Bäuche · Gen. des Bauchs"."""
    plural = entry["plural"] or NO_PLURAL
    if with_genitive and entry["genitive"]:
        return f"{plural} · Gen. {entry['genitive']}"
    return plural


def verb_forms(entry: dict[str, Any]) -> str:
    """"ruft an · rief an · hat angerufen" (Präsens · Präteritum · Perfekt)."""
    forms = (entry["praesens_3sg"], entry["praeteritum"], entry["perfekt"])
    return " · ".join(form for form in forms if form)


def adjective_forms(entry: dict[str, Any]) -> str:
    """"freundlicher · am freundlichsten"."""
    forms = (entry["comparative"], entry["superlative"])
    return " · ".join(form for form in forms if form)


def grammar_line(entry: dict[str, Any], with_genitive: bool = False) -> str:
    """One-line grammar summary for any POS; "" when there is nothing to show."""
    if entry["pos"] == "noun":
        return noun_forms(entry, with_genitive)
    if entry["perfekt"]:
        return verb_forms(entry)
    if entry["comparative"]:
        return adjective_forms(entry)
    return ""


def grammar_tags(entry: dict[str, Any]) -> list[str]:
    """Short tags such as ["verb", "trennbar", "reflexiv"]."""
    tags = [entry["pos"]]
    if entry["separable"]:
        tags.append("trennbar")
    if entry["reflexive"]:
        tags.append("reflexiv")
    return tags
