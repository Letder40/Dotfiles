#!/usr/bin/python3
import tomllib
import subprocess


def is_root() -> bool:
    return subprocess.run(
        ["id", "-u"],
        stdout=subprocess.DEVNULL
    ).returncode == 0


def is_installed(program: str) -> bool:
    return subprocess.run(
        ["pacman", "-Q", program],
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL
    ).returncode == 0


def install(programs: list[str]):
    to_install: list[str] = []
    for program in programs:
        if not is_installed(program):
            to_install.append(program)
        else:
            print("[unchanged] " + program + " was already installed")

    if len(to_install) == 0:
        return

    with open("/tmp/pacman_stderr.tmp", "w+") as tmp:
        for program in to_install:
            if subprocess.run(
                ["pacman", "-S", "--noconfirm", program],
                stdout=subprocess.DEVNULL,
                stderr=tmp
            ).returncode != 0:
                tmp.seek(0)
                error: str = tmp.read().rstrip('\n')
                print(f"[error] Could not install {program}: {error}")
            else:
                print(f"[success] {program} has been installed")


if not is_installed("pacman"):
    print("This configuration is made and tested only for arch linux")
    exit(1)

if not is_root():
    print("You must be root in order to install the specified software")
    exit(1)

with open("./config/config.toml", "rb") as f:
    config = tomllib.load(f)

required = [
    "zsh",
    "qtile",
    "git",
    "wget",
    "curl",
    "lightdm",
    "lightdm-gtk-greeter"
]

install(required)
install(config["software"]["terminal_utils"])
install(config["software"]["terminal_utils"])
install(config["software"]["systray"])
install(config["software"]["others"])

preferences = []

nerdfont = f"ttf-{config["preferences"]["nerdfont"]}-nerd"
browser = config["preferences"]["browser"]
terminal = config["preferences"]["terminal"]
preferences.extend([terminal, browser, nerdfont])

if config["preferences"]["animations"]:
    preferences.append("picom")

if config["preferences"]["eza"]:
    preferences.append("eza")

if config["preferences"]["neovim"]:
    preferences.append("neovim")
    print("[git] clonando configuración")
    subprocess.run(["git", "clone", "https://github.com/Letder40/nvim-config.git"])

install(preferences)
