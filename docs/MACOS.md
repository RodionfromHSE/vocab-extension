# macOS LaunchAgent

The vocabulary pipeline is installed as the per-user LaunchAgent
`com.rodionkhvorostov.vocab-extension` and runs daily at 21:00.

launchd does not inherit an interactive shell's environment. The installer
therefore writes the required string values into the plist's
`EnvironmentVariables` dictionary: `HOME`, `PATH`,
`VOCAB_EXTENSION_DATA_FOLDER`, `WORD_SAVER_SAVE_DIRECTORY`, and
`FIREWORKS_API_KEY` (plus `NEBIUS_API_KEY` and `OPENAI_API_KEY` when set).
This follows the
macOS `launchd.plist(5)` contract:
https://keith.github.io/xcode-man-pages/launchd.plist.5.html

The installed plist contains API keys, so the installer sets its permissions
to `0600`. Reinstall it whenever a key or path changes.

## Install

Create the project environment and export the API variables in the shell used
for installation. Then run:

```bash
cd /Users/rodionkhvorostov/Desktop/prog/other/study_tools/vocab-extension
.venv/bin/python scripts/install_launch_agent.py
plutil -lint ~/Library/LaunchAgents/com.rodionkhvorostov.vocab-extension.plist
```

Load or reload the service with launchctl's modern bootstrap commands:

```bash
launchctl bootout "gui/$(id -u)/com.rodionkhvorostov.vocab-extension" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" ~/Library/LaunchAgents/com.rodionkhvorostov.vocab-extension.plist
```

## Test and inspect

Trigger it immediately, independently of the calendar schedule:

```bash
launchctl kickstart -k "gui/$(id -u)/com.rodionkhvorostov.vocab-extension"
launchctl print "gui/$(id -u)/com.rodionkhvorostov.vocab-extension"
```

Logs are written to:

```text
~/Library/Logs/VocabExtension/pipeline.out.log
~/Library/Logs/VocabExtension/pipeline.err.log
```

The plist uses absolute paths for the virtualenv Python, repository script,
working directory, pipeline config, and logs. Anki must be installed and the
AnkiConnect add-on (code `2055492159`) must be available; the pipeline opens
Anki and waits for the API when it is not already running.
