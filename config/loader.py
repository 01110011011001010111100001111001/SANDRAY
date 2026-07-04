"""
SANDRAY

Module:
    config.loader

Purpose:
    Loads and validates the application configuration.
"""

from pathlib import Path

import yaml


BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_FILE = BASE_DIR / "config" / "config.yaml"


def load_config():
    """Load the application configuration."""

    if not CONFIG_FILE.exists():
        raise RuntimeError(
            f"Configuration file not found: {CONFIG_FILE}"
        )

    try:
        with CONFIG_FILE.open(
            "r",
            encoding="utf-8"
        ) as handle:
            cfg = yaml.safe_load(handle)

    except yaml.YAMLError as error:
        raise RuntimeError(
            f"Invalid configuration file: {error}"
        ) from error

    if not isinstance(cfg, dict):
        raise RuntimeError(
            "Configuration root must be a YAML mapping."
        )

    return cfg
