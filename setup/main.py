#!/usr/bin/python3
from pathlib import Path
import shutil

from .install_methods import curl_sh, git_clone_or_pull, pacman, pacman_required
from .gtk import configure_icon_theme
from .links import link_config, link_with_backup
from .config import config
from .output import fatal, log
from .sudo import cache_sudo, is_root


def setup() -> None:
    if is_root():
        fatal("this script cannot be run as root")

    if shutil.which("sudo") is None:
        fatal("sudo is required to install packages")

    if shutil.which("pacman") is None:
        fatal("this configuration only supports Arch Linux")

    cache_sudo()

    home = Path.home()
    repository_root = Path(__file__).resolve().parent.parent

    pacman_required(config["packages"]["required"])
    pacman([package["package"] for package in config["packages"]["autostart"]])
    pacman(config["packages"]["desktop"])

    browser = config["preferences"]["browser"]
    pacman([browser])

    terminal = config["preferences"]["terminal"]
    pacman([terminal])

    for curl_target in config["curl"]:
        check_path = curl_target.get("check_path")
        curl_sh(
            curl_target["url"],
            params=curl_target.get("params", ""),
            check_path=Path(check_path) if check_path else None,
            required=curl_target.get("required", False),
        )

    for git_target in config["git"]:
        git_clone_or_pull(
            f"{git_target['src']}/{git_target['repo']}",
            Path(git_target["path"]),
            required=git_target.get("required", False),
        )

    configure_icon_theme(config["preferences"]["icon_theme"], home)

    link_with_backup(
        home / "media" / "wallpapers",
        repository_root / "wallpapers",
    )

    link_with_backup(
        home / ".zshrc",
        repository_root / "zsh" / "zshrc",
    )

    link_with_backup(
        home / ".p10k.zsh",
        repository_root / "zsh" / "p10k.zsh",
    )

    link_config("qtile")
    link_config("eza")

    if terminal == "kitty":
        link_config("kitty")

    if config["preferences"]["animations"]:
        pacman(["picom"])
        link_config("picom")

    if config["preferences"]["neovim"]:
        pacman(["neovim"])
        git_clone_or_pull(
            "https://github.com/Letder40/nvim-config.git",
            repository_root / "nvim",
        )
        link_config("nvim")
