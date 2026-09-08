#!/usr/bin/python3
from sys import stderr, stdout
import tomllib
import subprocess
from pathlib import Path
from pwd import getpwnam
from datetime import datetime
import shutil
import os

def is_root() -> bool:
    return os.getuid() == 0


def is_installed(program: str) -> bool:
    return subprocess.run(
        ["pacman", "-Q", program],
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL
    ).returncode == 0


def install(programs: list[str]):
    for program in programs:
        if program == "":
            continue

        if is_installed(program):
            print(f"[unchanged] {program} was already installed")
            continue

        result = subprocess.run(
            ["pacman", "-S", "--noconfirm", program],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print(f"[error] Could not install {program}: {result.stderr.strip()}")
        else:
            print(f"[installed] {program}")


def main():
    if not is_root():
        print("You must be root in order to install the specified software")
        exit(1)

    if shutil.which("pacman") is None:
        print("This configuration is made and tested only for Arch Linux")
        exit(1)

    with open("./config.toml", "rb") as f:
        config = tomllib.load(f)

    # The following packages are are required by this config
    required = [
        "qtile",
        "lightdm",
        "lightdm-gtk-greeter",
        "zsh",
        "git",
        "wget",
        "zoxide",
        "fd",
        "ripgrep",
        "fzf",
        "thefuck",
        "zoxide",
        "pyenv",
        "zsh-syntax-highlighting"
    ]

    username = config["preferences"]["user"] 
    user = getpwnam(username)
    uid = user.pw_uid
    gid = user.pw_gid
    home = Path(user.pw_dir)

    install(required)
    install([package["package"] for package in config["packages"]["init"]])
    install(config["packages"]["others"])

    browser = config["preferences"]["browser"]
    install([browser])

    terminal = config["preferences"]["terminal"]
    install([terminal])

    def link_with_backup(link: Path, target: Path):
        if link.is_symlink():
            if not link.exists():
                name = link.name
                backup_path = link.with_name(f"{name}_{datetime.today().strftime('%Y-%m-%d_%H:%M:%S')}_bck")
                link.move(backup_path)
                print(f"[backup] {link} -> {backup_path}")

            elif link.is_symlink() and link.resolve() == target.resolve():
                print(f"[unchanged] {link} is already linked")
                return

        elif link.exists():
            name = link.name
            backup_path = link.with_name(f"{name}_{datetime.today().strftime('%Y-%m-%d_%H:%M:%S')}_bck")
            link.move(backup_path)
            print(f"[backup] {link} -> {backup_path}")

        else: 
            link.mkdir(parents=True, exist_ok=True)
            shutil.chown(link, uid, gid)


        link.symlink_to(target)
        print(f"[linked] {link} -> {target}")

         
    def link_config(name: str):
        config_dir = home / ".config"

        if not config_dir.exists():
            config_dir.mkdir(parents=True, exist_ok=True)
            shutil.chown(config_dir, uid, gid)

        config_path = home / ".config" / name
        target_path = Path.cwd() / name

        link_with_backup(config_path, target_path)


    def run_as_user(*args: str, cwd: Path | None = None):
        subprocess.run(
            args,
            check=True,
            cwd=cwd,
            preexec_fn=lambda: (
                os.setgid(gid),
                os.setuid(uid),
            )
        )

    wallpapers_dst = home / "media" / "wallpapers"
    link_with_backup(wallpapers_dst, Path.cwd() / "wallpapers")

    zsh_dst = home / ".zshrc"
    link_with_backup(zsh_dst, Path.cwd() / "zsh" / "zshrc")

    p10k_dst = home / ".p10k.zsh"
    link_with_backup(p10k_dst, Path.cwd() / "zsh" / "p10k.zsh")

    link_config("qtile")
    link_config("eza")

    if Path("/usr/share/icons/Papirus-Dark").exists():
        print("Downloading papirus dark theme")
        script = subprocess.Popen(["curl", "-fsSL", "https://git.io/papirus-icon-theme-install"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        subprocess.run(["sh"], stdin=script.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        with open(home / ".config" / "gtk-3.0" / "settings.ini", "w+") as f:
            f.write("[settings]\ngtk-icon-theme-name = Papirus-Dark")
            

    if terminal == 'kitty':
        install(["kitty"])
        link_config("kitty")

    if config["preferences"]["animations"]:
        install(["picom"])
        link_config("picom")

    if config["preferences"]["neovim"]:
        install(["neovim"])

        nvim_path = Path.cwd() / "nvim"
        if not nvim_path.exists():
            print("[git] clonando configuración")
            run_as_user("git", "clone", "https://github.com/Letder40/nvim-config.git", "nvim")
        else:
            print("[git] obteniendo cambios en la configuración")
            run_as_user("git", "pull", cwd=nvim_path)

        link_config("nvim")

if __name__ == '__main__':
    main()
