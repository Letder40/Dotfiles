from pathlib import Path
import subprocess
import tomllib
from libqtile import hook

from user_config import config


@hook.subscribe.startup_once
def autostart():
    with open(Path.home() / ".config/qtile/config.toml", "rb") as f:
        config = tomllib.load(f)

    if config["preferences"]["animations"]:
        config_path = Path.home() / ".config" / "picom.conf"
        subprocess.Popen(["picom", "-b", "--config", config_path.absolute().as_posix()]) 

    for entry in config["packages"]["init"]:
        subprocess.run(["kill", "-9", entry["exec"].split()[0]]) 
        subprocess.Popen(entry["exec"].split()) 
