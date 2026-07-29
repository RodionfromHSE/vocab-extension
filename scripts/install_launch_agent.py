#!/usr/bin/env python3
"""Install the per-user launchd agent for the vocabulary pipeline."""

from __future__ import annotations

import argparse
import os
import plistlib
from pathlib import Path

LABEL = "com.rodionkhvorostov.vocab-extension"
ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()
DEFAULT_DESTINATION = HOME / "Library" / "LaunchAgents" / f"{LABEL}.plist"


def required_environment(name: str, default: str | None = None) -> str:
    value = os.environ.get(name, default)
    if not value:
        raise SystemExit(f"Required environment variable is missing: {name}")
    if value != value.strip():
        raise SystemExit(
            f"Environment variable has leading/trailing whitespace: {name}"
        )
    return (
        str(Path(value).expanduser())
        if name.endswith(("_FOLDER", "_DIRECTORY"))
        else value
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "pipeline_config.yaml")
    parser.add_argument("--destination", type=Path, default=DEFAULT_DESTINATION)
    args = parser.parse_args()

    python = ROOT / ".venv" / "bin" / "python"
    config = args.config.expanduser().resolve()
    if not python.is_file():
        raise SystemExit(f"Virtualenv Python does not exist: {python}")
    if not config.is_file():
        raise SystemExit(f"Pipeline config does not exist: {config}")

    data_folder = required_environment(
        "VOCAB_EXTENSION_DATA_FOLDER", str(HOME / "Documents" / "vocab_extension_data")
    )
    word_saver = required_environment(
        "WORD_SAVER_SAVE_DIRECTORY", str(HOME / "Documents" / "word_saver")
    )
    Path(data_folder).mkdir(parents=True, exist_ok=True)
    Path(word_saver).mkdir(parents=True, exist_ok=True)
    environment = {
        "HOME": str(HOME),
        "PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin",
        "VOCAB_EXTENSION_DATA_FOLDER": data_folder,
        "WORD_SAVER_SAVE_DIRECTORY": word_saver,
        "NEBIUS_API_KEY": required_environment("NEBIUS_API_KEY"),
    }
    if os.environ.get("OPENAI_API_KEY"):
        environment["OPENAI_API_KEY"] = required_environment("OPENAI_API_KEY")

    log_dir = HOME / "Library" / "Logs" / "VocabExtension"
    log_dir.mkdir(parents=True, exist_ok=True)
    args.destination.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "Label": LABEL,
        "ProgramArguments": [
            str(python),
            str(ROOT / "run_pipeline.py"),
            "--config",
            str(config),
        ],
        "WorkingDirectory": str(ROOT),
        "EnvironmentVariables": environment,
        "StartCalendarInterval": {"Hour": 21, "Minute": 0},
        "ProcessType": "Background",
        "StandardOutPath": str(log_dir / "pipeline.out.log"),
        "StandardErrorPath": str(log_dir / "pipeline.err.log"),
    }
    with args.destination.open("wb") as stream:
        plistlib.dump(payload, stream, sort_keys=False)
    args.destination.chmod(0o600)
    print(f"Installed {LABEL} at {args.destination}")
    print(f"Pipeline config: {config}")


if __name__ == "__main__":
    main()
