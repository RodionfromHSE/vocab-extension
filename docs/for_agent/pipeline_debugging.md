# Pipeline Debugging

The scheduled macOS pipeline is a LaunchAgent named `com.example.run_word_addition_pipeline`.
It runs `/Users/Rodion.Khvorostov/Scripts/run_word_addition_pipeline.zsh` every day at 21:00.

Useful checks:

```bash
launchctl print "gui/$(id -u)/com.example.run_word_addition_pipeline"
```

Read the pipeline logs:

```bash
less /tmp/run_word_addition_pipeline.out
less /tmp/run_word_addition_pipeline.err
```

The shell script runs `run_pipeline.py` with the repo virtualenv Python. If the pipeline fails, check the last `ERROR in ...` block in `/tmp/run_word_addition_pipeline.out` first; `/tmp/run_word_addition_pipeline.err` usually contains the Python traceback for the failed stage.

For manual reproduction:

```bash
cd /Users/Rodion.Khvorostov/Desktop/Prog/Other/vocab_extension
.venv/bin/python run_pipeline.py
```

Current known failure pattern: the meta generator fails if `meta_generator/config.yaml` points to a model unsupported by its `base_url`. That produces entries with an `error` field instead of `example`, and the audio step cannot process them. Keep `api.model` and `api.base_url` compatible, then rerun the pipeline.

To verify model availability without running the full pipeline, list Nebius models with the LaunchAgent key from the plist and check that `api.model` is present in the returned IDs.
