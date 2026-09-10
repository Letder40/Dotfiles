from pathlib import Path
import shutil
import subprocess

from .install_methods import curl_sh, git_clone_or_pull, pacman, pacman_required, install_with_deps
from .service import setup_service
from .gtk import configure_icon_theme
from .links import link_config, link_with_backup
from .config import config
from .output import fatal, log
from .sudo import cache_sudo, is_root


def _tmux_setup() -> None:
    if not install_with_deps("tmux", config["tmux"]):
        return

    link_config("tmux")
    log("tmux", "installing plugins")

    sh_tpm_script = subprocess.run(
        [
            "bash",
            Path("~/.tmux/plugins/tpm/scripts/install_plugins.sh").expanduser()
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if sh_tpm_script.returncode != 0:
        detail = sh_tpm_script.stdout.strip()
        log("error", f"TPM plugin installation failed: {detail or 'unknown error'}")
        return

    log("tmux", sh_tpm_script.stdout.strip() or "plugins are installed")


def _nvim_setup(repository_root: Path) -> None:
    log("neovim", "Installing neovim")

    if not pacman(["neovim"]):
        log("error", "neovim installation has failled")
        return

    is_success = git_clone_or_pull(
        "https://github.com/Letder40/nvim-config.git",
        repository_root / "nvim",
    )

    if not is_success:
        return

    link_config("nvim")


def _resolve_packages(entry: list[dict]) -> list[str]:
    """
    returns an array package of package names after handling these cases:
    + package can be ommitted
    + package can contain an * that indicates that the name of the package is the same as other
      field that can repeat the name, if the field is exec is the first token of exec

    Example:

    autostart = [
        { exec="fcitx5 -d", package="*" },
        { exec="volumeicon", package="*" },
        { exec="setxkbmap es" },
    ]

    returns [fcitx5, volumeicon] ignoring setxkbmap
    """

    packages = []

    for table in entry:
        package = table.get("package", None)

        if package is None:
            continue

        if package == "*":
            if "exec" in table:
                exec_field: str = table["exec"]
                package = exec_field.split()[0]
                packages.append(package)
            elif "name" in table:
                package = table["name"]
                packages.append(package)
            else:
                raise ValueError("cannot derive a package without an exec or name field")

        else:
            packages.append(package)

    return packages


def setup() -> None:
    if is_root():
        fatal("this script cannot be run as root")

    if shutil.which("sudo") is None:
        fatal("sudo is required to install packages and enable services")

    if shutil.which("pacman") is None:
        fatal("this configuration only supports Arch Linux")

    cache_sudo()

    home = Path.home()
    repository_root = Path(__file__).resolve().parent.parent

    base = config["packages"]["base"]
    packages = config["packages"]
    browser = config["preferences"]["browser"]
    terminal = config["preferences"]["terminal"]
    font = config["preferences"]["font"]
    icon_theme = config["preferences"]["icon_theme"]

    # base
    pacman_required(base["required"])
    pacman_required(base["system"])
    pacman_required(_resolve_packages(base["init"]["autostart"]))
    pacman_required(_resolve_packages(base["init"]["services"]))
    for service in base["init"]["services"]:
        setup_service(service["name"], service.get("user", False), required=True)

    for curl_target in config.get("curl", []):
        check_path = curl_target.get("check_path")
        curl_sh(
            curl_target["url"],
            params=curl_target.get("params", ""),
            check_path=Path(check_path) if check_path else None,
            required=curl_target.get("required", False),
        )

    for git_target in config.get("git", []):
        git_clone_or_pull(
            f"{git_target['src']}/{git_target['repo']}",
            Path(git_target["path"]),
            required=git_target.get("required", False),
        )

    # user packages
    pacman(_resolve_packages([browser]))
    pacman(_resolve_packages([terminal]))
    pacman(_resolve_packages([font]))
    pacman(_resolve_packages([icon_theme]))
    pacman(packages["utils"])
    pacman(packages["desktop"])
    pacman(packages["others"])
    pacman(_resolve_packages(packages["init"]["autostart"]))
    pacman(_resolve_packages(packages["init"]["services"]))
    for service in packages["init"]["services"]:
        setup_service(service["name"], service.get("user", False), service.get("required", False))

    configure_icon_theme(icon_theme["name"], home)

    link_with_backup(
        home / "media" / "wallpapers",
        repository_root / "wallpapers",
    )

    link_config("qtile")

    if terminal["name"] == "kitty":
        link_config("kitty")

    if config["preferences"]["neovim"]:
        _nvim_setup(repository_root)

    if config["preferences"]["zshrc"]:
        if install_with_deps("zshrc", config["zshrc"]):
            link_with_backup(
                home / ".zshrc",
                repository_root / "zsh" / "zshrc",
            )

    if "eza" in config["packages"]["utils"]:
        link_config("eza")

    if "rofi" in config["packages"]["others"]:
        link_config("rofi")

    if config["preferences"]["tmux"]:
        _tmux_setup()

    if config["preferences"]["animations"]:
        pacman(["picom"])
        link_config("picom")
