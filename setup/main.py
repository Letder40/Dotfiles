#!/usr/bin/python3
from pathlib import Path
import shutil

from .pacman import install
from .sudo import is_root
from .links import link_config, link_with_backup, hard_link
from .user import home
from .git import git_clone_or_pull

from .required import required
from .config import config_path, config


def setup():
    if not is_root():
        print("You must be root in order to install the specified software")
        exit(1)

    if shutil.which("pacman") is None:
        print("This configuration is made and tested only for Arch Linux")
        exit(1)

    hard_link(config_path, Path.cwd() / "qtile" / "config.toml")

    install(required)
    install([package["package"] for package in config["packages"]["init"]])
    install(config["packages"]["others"])

    with open(home / ".config" / "gtk-3.0" / "settings.ini", "w+") as f:
        f.write("[settings]\ngtk-icon-theme-name = Papirus-Dark")

    browser = config["preferences"]["browser"]
    install([browser])

    terminal = config["preferences"]["terminal"]
    install([terminal])

    link_with_backup(
        home / "media" / "wallpapers",
        Path.cwd() / "wallpapers"
    )

    link_with_backup(
        home / ".zshrc",
        Path.cwd() / "zsh" / "zshrc"
    )

    link_with_backup(
        home / "p10k.zsh",
        Path.cwd() / "zsh" / "p10k.zsh"
    )

    link_config("qtile")
    link_config("eza")

    if terminal == 'kitty':
        install(["kitty"])
        link_config("kitty")

    if config["preferences"]["animations"]:
        install(["picom"])
        link_config("picom")

    if config["preferences"]["neovim"]:
        install(["neovim"])
        git_clone_or_pull(
            Path.cwd() / "nvim",
            "https://github.com/Letder40/nvim-config.git"
        )
        link_config("nvim")
