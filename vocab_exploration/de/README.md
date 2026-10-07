# German vocabulary (de/)

Turns a plain German word list (`.txt`, one word or phrase per line) into an Anki deck. Each word gets grammar, its most common meaning (German + English definition), 1–2 natural example sentences with translations, and German audio.

---

## Run the full pipeline

Everything runs from the **repo root** (`vocab-extension/`) with one command. The result is one file, **`deck.apkg`**, which contains the note type (one Anki field per piece of information), the notes, and all the audio. Import it into Anki and you're done.

### 0. One-time setup

```bash
cd ~/Desktop/prog/other/study_tools/vocab-extension
uv pip install --python .venv/bin/python genanki beautifulsoup4   # genanki builds the .apkg; bs4 is only for eval/
source ~/.zshrc                                                    # exports FIREWORKS_API_KEY
echo ${FIREWORKS_API_KEY:+key is set}                             # should print "key is set"
```

The default card template uses `_LongSilence.mp3` from your Anki collection to stop autoplay after the word (it's already there). Only for option B in step 4 do you need the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on.

### 1. Check the config

[`pipeline_config.yaml`](pipeline_config.yaml) is already set up for `a1_b1_words_extra.txt`:

| key | current value | meaning |
|---|---|---|
| `input_txt` | `…/vocab_deduplication/data/de/common/a1_b1_words_extra.txt` | word list (1065 words, 59 of them phrases) |
| `run_name` | `a1_b1_words_extra` | all outputs and caches go to `data/runs/<run_name>/` |
| `meta.config_file` | `config.yaml` | model (`deepseek-v4p1-flash`), prompt, schema |
| `meta.workers` | `8` | parallel API requests |
| `audio.media_dir` | `data/runs/<run_name>/media` | where the mp3s are made (they're bundled into the .apkg) |
| `audio.filename_prefix` | `de_<run_name>_` | mp3 names, unique per run (`de_a1_b1_words_extra_word_audio_12.mp3`) |
| `cards.deck_name` | `German A1-B1` | Anki deck the notes go into |
| `cards.tags` | `german, a1_b1` | Anki tags; the word type (`noun`, `verb`, …) is added automatically |

For a new word list later, change only `input_txt` and `run_name`.

### 2. Dry run (10 words, ~$0.02, ~1 min)

```bash
.venv/bin/python vocab_exploration/de/pipeline.py --run-name dry_run --sample 10
```

Open `vocab_exploration/de/data/runs/dry_run/preview.md` and skim the 10 words. If you want to see the cards themselves, import `dry_run/deck.apkg` into Anki (step 4) and delete the test notes afterwards. Then delete the folder:

```bash
rm -rf vocab_exploration/de/data/runs/dry_run
```

### 3. Full run (~$2, ~40–50 min for 1065 words)

```bash
.venv/bin/python vocab_exploration/de/pipeline.py
```

What you'll see:

```
Run dir: …/vocab_exploration/de/data/runs/a1_b1_words_extra
[words] 1065 words
[meta] 0 cached, 1065 to generate (~$2.13)
[meta]: 100%|██████████| 1065/1065 [~20 min]
[cards] 1065 notes
[audio] 0 already voiced, 1065 to generate     ← three passes: word, example 1, example 2 (~20–30 min)
[export] 1065 notes → deck.apkg, preview.md (0 notes missing audio)
```

The run checks the API key and the input file before spending anything, and stops with a clear message if one is missing.

**If it crashes or you stop it (Ctrl-C), run the same command again.** Each finished word is saved right away (`meta_cache.jsonl`), and audio is only made for notes that don't have it yet. A rerun only does the missing work, and costs nothing if nothing is missing.

**If some words fail:** they're listed in `failed.json`, and the rest of the run continues. Run the command again to retry them.

### 4. Import into Anki

**A. Double-click / File → Import (recommended)**
1. Open `vocab_exploration/de/data/runs/a1_b1_words_extra/deck.apkg` (double-click, or Anki → **File → Import**).
2. Anki creates the deck **German A1-B1**, the note type **German Vocab (vocab-extension)**, and copies the audio.

**B. Via AnkiConnect, from the terminal**

```bash
.venv/bin/python vocab_exploration/de/pipeline.py --to-anki
```

Everything before the import is cached, so this only builds and imports the package. The script launches Anki if needed.

**Re-importing is safe.** Every note has a stable ID derived from its word, so importing a newer `deck.apkg` (e.g. after fixing some words) **updates** notes instead of duplicating them.

> ⚠️ **Once you've customized the card template in Anki**, set **"Update note types: Never"** in the import dialog when you re-import. Otherwise Anki may replace your template with the default one from the package. (Field contents still update.)

### 5. Starting over / other options

| want to… | do |
|---|---|
| regenerate everything from scratch | `rm -rf vocab_exploration/de/data/runs/a1_b1_words_extra` and run again |
| skip audio | add `--skip-audio` (the audio fields stay empty) |
| use a different word list | change `input_txt` + `run_name` in `pipeline_config.yaml`, or pass `--run-name` |
| use a different model | change `api.model` in `config.yaml` (models compared in `eval/report.md`) |
| change the *default* template shipped in the .apkg | edit `anki/front.html`, `anki/back.html`, `anki/style.css`, then rerun (only the export redoes work) |

---

## What you get

Everything lands in `data/runs/<run_name>/`:

| file | what it is |
|---|---|
| **`deck.apkg`** | Anki package: note type + deck + notes + audio |
| **`preview.md`** | readable page with all words (grammar, meaning, examples), for review |
| `cards_final.json` | exactly the field values that go into Anki, one record per note |
| `enriched.json` | raw model output, one entry per word |
| `failed.json` | words that failed, with the error (empty when all went well) |
| `media/` | the mp3s (also inside the .apkg) |
| `meta_cache.jsonl`, `cards*.json`, `audio_*` | intermediate files / caches |

### Anki fields

The note type **German Vocab (vocab-extension)** has one field per piece of information, so you design the card in Anki (**Tools → Manage Note Types → Cards**). Empty fields are truly empty, so `{{#field}}…{{/field}}` sections work.

| field | example (noun) | example (verb) |
|---|---|---|
| `word_de` *(sort field)* | Kleiderschrank | anrufen |
| `article` | der | |
| `headword` | der Kleiderschrank | anrufen |
| `word_audio` | `[sound:…word_audio_3.mp3]` (reads `headword`) | `[sound:…]` |
| `word_en` | wardrobe, closet | to call, to phone |
| `pos` | noun | verb |
| `grammar` | die Kleiderschränke *(or `nur Singular`)* | ruft an · rief an · hat angerufen |
| `plural`, `genitive` | die Kleiderschränke, des Kleiderschranks | |
| `praesens_3sg`, `praeteritum`, `partizip_2`, `auxiliary`, `perfekt` | | ruft an, rief an, angerufen, haben, hat angerufen |
| `separable`, `reflexive` | | `trennbar` / *(empty)* |
| `comparative`, `superlative` | *(adjectives: freundlicher, am freundlichsten)* | |
| `definition_en`, `definition_de` | a large piece of furniture… / ein großes Möbelstück… | |
| `example1_de`, `example1_en`, `example1_audio` | Meine Jacken hängen im Kleiderschrank. / My jackets… / `[sound:…]` | |
| `example2_de`, `example2_en`, `example2_audio` | second example (empty if the model gave only one) | |
| `source_word` | the line from your .txt | |

Tags: `german a1_b1 <pos>` (e.g. `german a1_b1 verb`).

### Default card (English → German)

| side | shows |
|---|---|
| **front** | `word_en` (no sound) · `definition_en` behind a click |
| **back** | front + **German word with article** · 🔊 word audio (**autoplays**) · grammar line · `trennbar`/`reflexiv` tags · example 1 and example 2, each with a 🔊 button (plays only on click) and its translation behind a click · `definition_de` behind a click |

Autoplay stops after the word because of `<div style="display:none">[sound:_LongSilence.mp3]</div>`, which sits right after the word audio (your trick). Example sounds after it only play when clicked.

### Model output per word

Every entry has the same keys. Fields that don't apply are `""` (or `false`). The shape is enforced by [`schema.json`](schema.json); an invalid answer is retried.

```json
{
  "word": "Bauch", "lemma": "Bauch", "pos": "noun",
  "article": "der", "plural": "die Bäuche", "genitive": "des Bauchs",
  "praesens_3sg": "", "praeteritum": "", "partizip_2": "", "auxiliary": "", "perfekt": "",
  "separable": false, "reflexive": false, "comparative": "", "superlative": "",
  "word_en": "stomach, belly",
  "definition_de": "der vordere Teil des Körpers zwischen Brust und Beinen",
  "definition_en": "the front part of the body between the chest and the legs",
  "examples": [{"de": "Mir tut der Bauch weh.", "en": "My stomach hurts."}],
  "tts_text": "der Bauch"
}
```

The model decides the word type (`pos`). Capitalization is passed only as a hint: "Bescheid geben" and "Rad fahren" are capitalized but aren't nouns, and "Angestellte" is `der/die`.

---

## Troubleshooting

| message | fix |
|---|---|
| `Preflight failed: FIREWORKS_API_KEY is not set` | `source ~/.zshrc` in the same terminal |
| words in `failed.json` | run the same command again (it retries only those). If a word keeps failing, its error message is in `failed.json`. |
| `[export] … N notes missing audio` | gTTS hiccup or rate limit: run the same command again (it retries only notes without audio) |
| `--to-anki`: AnkiConnect not reachable | open Anki manually and check the AnkiConnect add-on is installed, or just double-click `deck.apkg` |
| `ModuleNotFoundError: genanki` | `uv pip install --python .venv/bin/python genanki` |
| card template lost your changes after re-import | re-import with "Update note types: Never" (see step 4) |

---

## Files

- `pipeline.py`, `pipeline_config.yaml`: the full pipeline.
- `prompt.md`: model instructions + 5 examples built from Cambridge dictionary entries (Verkehr, fahren, anrufen, freundlich, Bescheid geben).
- `schema.json`: output shape.
- `config.yaml`: model settings (Fireworks, `deepseek-v4p1-flash`).
- `cards.py`: model output → Anki fields, note type, `.apkg`.
- `anki/front.html`, `anki/back.html`, `anki/style.css`: default card template baked into the `.apkg`.
- `formatting.py`: grammar lines / headwords (shared by cards and markdown).
- `render_markdown.py`: any enriched JSON → readable page (example: `samples/leftover_sample10.md`).
- `txt_to_json.py`, `audio_config.yaml`: standalone pieces, if you want to run `meta_generator` / `audio_component` by hand.
- `eval/`: how the model was chosen (below).

## Eval (model bake-off)

3 Fireworks models were compared on 25 test words. Grammar was checked against the Cambridge German–English dictionary, and quality was rated by the models grading each other blind (self-grades excluded). Result: `deepseek-v4p1-flash` is as good as `kimi-k3` at about 1/6 of the price. Details: [`eval/report.md`](eval/report.md).

To reproduce:

```bash
cd vocab_exploration/de
../../.venv/bin/python eval/build_eval_set.py path/to/a1_b1_words.txt  # → eval/eval_words.json + eval/gold.json (Cambridge)
../../.venv/bin/python eval/run_bakeoff.py                             # → eval/results/<model>.json
../../.venv/bin/python eval/judge.py                                   # → eval/judgments.json (cached in eval/judge_cache/)
../../.venv/bin/python eval/score.py                                   # → eval/report.md
```

Two caveats about using Cambridge as the reference:
- Cambridge lists only *irregular* verb forms, so grammar is scored only on the fields it provides.
- Its first meaning isn't always the most common one (e.g. `bloß` → "bare", `weg sein` → "out cold"). That's why the graders score "same meaning as Cambridge" and "most common meaning" separately.
