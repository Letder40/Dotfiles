from pathlib import Path
import shlex
import subprocess

from libqtile import hook
from user_config import config


@hook.subscribe.startup_once
def autostart():
    if config["preferences"]["animations"]:
        config_path = Path.home() / ".config" / "picom" / "picom.conf"
        command = f"picom -b --config {config_path.absolute().as_posix()}"
        subprocess.Popen(shlex.split(command))

    for entry in config["packages"]["base"]["init"]["autostart"]:
        subprocess.Popen(shlex.split(entry["exec"]))

    for entry in config["packages"]["init"]["autostart"]:
        subprocess.Popen(shlex.split(entry["exec"]))
