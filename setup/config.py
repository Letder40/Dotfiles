from pathlib import Path
import tomllib

config_path = Path(__file__).resolve().parent.parent / "config.toml"

with open(config_path, "rb") as f:
    config = tomllib.load(f)
