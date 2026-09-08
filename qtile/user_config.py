from pathlib import Path
import tomllib

with open(Path.home() / ".config/qtile/config.toml", "rb") as f:
    config = tomllib.load(f)
