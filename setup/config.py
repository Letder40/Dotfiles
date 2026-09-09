from pathlib import Path
import tomllib

config_path = Path.cwd() / "config.toml"

with open(config_path, "rb") as f:
    config = tomllib.load(f)
