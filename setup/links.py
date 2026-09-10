from datetime import datetime
from pathlib import Path

from .output import log


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent


def link_with_backup(link: Path, target: Path) -> None:
    link.parent.mkdir(parents=True, exist_ok=True)

    if link.is_symlink():
        if not link.exists():
            name = link.name
            backup_path = link.with_name(
                f"{name}_{datetime.today().strftime('%Y-%m-%d_%H:%M:%S')}_bck")
            link.replace(backup_path)
            log("backup", f"{link} -> {backup_path}")

        elif link.resolve() == target.resolve():
            log("unchanged", f"{link} is already linked")
            return

    elif link.exists():
        name = link.name
        backup_path = link.with_name(
            f"{name}_{datetime.today().strftime('%Y-%m-%d_%H:%M:%S')}_bck")
        link.replace(backup_path)
        log("backup", f"{link} -> {backup_path}")

    link.symlink_to(target)
    log("linked", f"{link} -> {target}")


def link_config(name: str) -> None:
    """
    this functions assumes that dst is .config and call link_with_backup
    """
    config_dir = Path.home() / ".config"

    if not config_dir.exists():
        config_dir.mkdir(parents=True, exist_ok=True)

    config_path = Path.home() / ".config" / name
    target_path = REPOSITORY_ROOT / name

    link_with_backup(config_path, target_path)
