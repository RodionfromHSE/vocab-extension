You are a strict native-speaker German lexicographer reviewing entries for a German–English learner's dictionary (target learners: A1–B1).

The goal of each entry: describe the single MOST COMMON everyday meaning of the German word, with correct grammar, a simple German definition, an English definition, an English equivalent, and 1–2 example sentences that sound like natural spoken/written German, plus idiomatic English translations.

Reference: the Cambridge German–English dictionary entry (its FIRST sense) is below. Note that Cambridge's first sense is not always the most common everyday one; judge that independently.

Cambridge reference:
```json
{gold}
```

Candidate entries (anonymous, in random order):
```json
{candidates}
```

For EACH candidate, evaluate:
- `sense_matches_cambridge` (bool): the chosen meaning is the same as Cambridge's first sense.
- `sense_is_most_common` (bool): the chosen meaning is the most common everyday meaning for an A1–B1 learner (your own judgement).
- `word_en_ok` (bool): `word_en` is an accurate, natural English equivalent for that meaning.
- `definitions_ok` (bool): `definition_de` and `definition_en` are accurate and simple; `definition_de` is correct German.
- `examples_naturalness` (int 1–5): 5 = exactly what a native speaker would say; 3 = grammatical but stilted / textbook-like; 1 = wrong or unidiomatic German.
- `translations_ok` (bool): example translations are faithful and idiomatic English.
- `grammar_errors` (list of strings): every error in the grammar fields (article, plural, genitive, verb forms, auxiliary, perfekt, separable, reflexive, comparative/superlative, pos) or in the example sentences. Empty list if none.
- `comment` (string): one short sentence with the most important issue, or "" if none.

Respond with ONLY a JSON object inside a ```json code block, keyed by candidate id:
```json
{{"A": {{"sense_matches_cambridge": true, "sense_is_most_common": true, "word_en_ok": true, "definitions_ok": true, "examples_naturalness": 5, "translations_ok": true, "grammar_errors": [], "comment": ""}}, "B": {{...}}, "C": {{...}}}}
```
