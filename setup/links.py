from pathlib import Path
from datetime import datetime
import shutil

from .user import home, uid, gid


def link_with_backup(link: Path, target: Path):
    if link.is_symlink():
        if not link.exists():
            name = link.name
            backup_path = link.with_name(
                f"{name}_{datetime.today().strftime('%Y-%m-%d_%H:%M:%S')}_bck")
            link.replace(backup_path)
            print(f"[backup] {link} -> {backup_path}")

        elif link.is_symlink() and link.resolve() == target.resolve():
            print(f"[unchanged] {link} is already linked")
            return

    elif link.exists():
        name = link.name
        backup_path = link.with_name(
            f"{name}_{datetime.today().strftime('%Y-%m-%d_%H:%M:%S')}_bck")
        link.move(backup_path)
        print(f"[backup] {link} -> {backup_path}")

    link.symlink_to(target)
    print(f"[linked] {link} -> {target}")


def hard_link(link: Path, target: Path):
    if link.exists():
        return

    link.hardlink_to(target)


def link_config(name: str):
    """
    this functions assumes that dst is .config and call link_with_backup
    """
    config_dir = home / ".config"

    if not config_dir.exists():
        config_dir.mkdir(parents=True, exist_ok=True)
        shutil.chown(config_dir, uid, gid)

    config_path = home / ".config" / name
    target_path = Path.cwd() / name

    link_with_backup(config_path, target_path)
