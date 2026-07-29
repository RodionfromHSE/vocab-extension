# Pipeline Debugging

The scheduled macOS pipeline is a LaunchAgent named `com.rodionkhvorostov.vocab-extension`.
It runs the repository's `.venv/bin/python` and `run_pipeline.py` every day at 21:00.

Useful checks:

```bash
launchctl print "gui/$(id -u)/com.rodionkhvorostov.vocab-extension"
```

Read the pipeline logs:

```bash
less ~/Library/Logs/VocabExtension/pipeline.out.log
less ~/Library/Logs/VocabExtension/pipeline.err.log
```

The plist runs `run_pipeline.py` directly with the repo virtualenv Python. If the pipeline fails, check the last `ERROR in ...` block in the stdout log first; the stderr log usually contains the Python traceback for the failed stage.

On a successful Anki submission, the production config moves direct JSON inputs from `WORD_SAVER_SAVE_DIRECTORY` into its `old/` subdirectory. If a stage fails, or `archive_on_success` is set to `false`, the source files are preserved.

For manual reproduction:

```bash
cd /Users/rodionkhvorostov/Desktop/prog/other/study_tools/vocab-extension
.venv/bin/python run_pipeline.py
```

Current known failure pattern: the meta generator fails if `meta_generator/config.yaml` points to a model unsupported by its `base_url`. That produces entries with an `error` field instead of `example`, and the audio step cannot process them. Keep `api.model` and `api.base_url` compatible, then rerun the pipeline.

The plist contains the required launchd `EnvironmentVariables` (`HOME`, `PATH`, data paths, and API keys) and is installed with mode `0600`. Re-run `scripts/install_launch_agent.py` after rotating an API key.
