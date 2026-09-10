import configparser
import os
from pathlib import Path
import re
import shutil
import subprocess

from .output import log

class CaseSensitveConfigParser(configparser.ConfigParser):
    """
    preserve casing:

    GTK section names are case-sensitive. Migrate the invalid section that
    older versions of this setup wrote while retaining any other settings.

    The parser is case insensitive by default, so this overwrite the method
    optionxform that transform the field to lowercase and make it case sensitive

    Maybe this will be deleted in the future, if i remember to do it...
    """
    def optionxform(self, optionstr: str) -> str:
        return optionstr

def _write_gtk_settings(path: Path, icon_theme: str) -> None:
    settings = CaseSensitveConfigParser()

    if path.exists():
        settings.read(path)

    if settings.has_section("settings"):
        if not settings.has_section("Settings"):
            settings.add_section("Settings")

        for key, value in settings.items("settings"):
            if not settings.has_option("Settings", key):
                settings.set("Settings", key, value)

        settings.remove_section("settings")

    if not settings.has_section("Settings"):
        settings.add_section("Settings")

    settings.set("Settings", "gtk-icon-theme-name", icon_theme)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w") as config_file:
        settings.write(config_file)

    log("updated", path)


def _write_xsettings(path: Path, icon_theme: str) -> None:
    setting = f'Net/IconThemeName "{icon_theme}"'
    contents = path.read_text().strip() if path.exists() else ""
    pattern = re.compile(r"^\s*Net/IconThemeName\s+.*$", re.MULTILINE)

    if pattern.search(contents):
        contents = pattern.sub(setting, contents)
    else:
        contents = f"{contents}\n{setting}\n" if contents else f"{setting}\n"

    path.write_text(contents)
    log("updated", path)


def _kill_xsettingsd() -> None:
    result = subprocess.run(
        ["pkill", "-HUP", "-u", str(os.getuid()), "-x", "xsettingsd"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if result.returncode == 0:
        log("reloaded", "xsettingsd")
        return

    if result.returncode != 1:
        return

    # The installer is often rerun from an existing Qtile session, before the
    # newly-installed daemon has had a chance to be started by startup_once.
    if os.environ.get("DISPLAY") and shutil.which("xsettingsd"):
        subprocess.Popen(
            ["xsettingsd"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        log("started", "xsettingsd")


def configure_icon_theme(icon_theme: str, home: Path | None = None) -> None:
    home = home or Path.home()

    for gtk_version in ("gtk-3.0", "gtk-4.0"):
        _write_gtk_settings(
            home / ".config" / gtk_version / "settings.ini",
            icon_theme,
        )

    _write_xsettings(home / ".xsettingsd", icon_theme)
    _kill_xsettingsd()
