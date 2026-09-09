from pathlib import Path
import subprocess
from libqtile import hook

from user_config import config

@hook.subscribe.startup_once
def autostart():
    if config["preferences"]["animations"]:
        config_path = Path.home() / ".config" / "picom" / "picom.conf"
        subprocess.Popen(["picom", "-b", "--config", config_path.absolute().as_posix()])

    for entry in config["packages"]["init"]:
        subprocess.Popen(entry["exec"].split())
