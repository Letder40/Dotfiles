import shlex
import subprocess
from pathlib import Path

from .output import fatal, log


def pacman_has(package: str) -> bool:
    return subprocess.run(
        ["pacman", "-Qq", package],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def pacman(packages: list[str]) -> bool:
    packages = list(dict.fromkeys(package for package in packages if package))

    missing = []

    for package in packages:
        if pacman_has(package):
            log("unchanged", f"{package} is already installed")
        else:
            missing.append(package)

    if not missing:
        return True

    log("pacman", f"installing {len(missing)} package(s): {', '.join(missing)}")

    result = subprocess.run(
        ["sudo", "pacman", "-S", "--needed", "--noconfirm", *missing],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        error = result.stderr.strip() or f"pacman exited with code {result.returncode}"
        log("error", f"package installation failed: {error}")
        return False

    for package in missing:
        log("installed", package)

    return True


def pacman_required(packages: list[str]) -> None:
    if not pacman(packages):
        fatal("could not install all required packages")


def curl_sh(
    url: str,
    params: str = "",
    check_path: Path | None = None,
    required: bool = False,
) -> bool:
    if check_path is not None:
        check_path = check_path.expanduser()

        if check_path.exists():
            log("unchanged", f"{check_path} already exists")
            return True

    log("download", url)

    curl = subprocess.run(
        ["curl", "-fsSL", url],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if curl.returncode != 0:
        error = curl.stderr.strip() or f"curl exited with code {curl.returncode}"
        message = f"could not download {url}: {error}"

        if required:
            fatal(message)

        log("error", message)
        return False

    result = subprocess.run(
        ["sh", "-c", curl.stdout, "", *shlex.split(params)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        error = result.stderr.strip() or f"installer exited with code {result.returncode}"
        message = f"installation from {url} failed: {error}"

        if required:
            fatal(message)

        log("error", message)
        return False

    log("installed", url)
    return True


def git_clone_or_pull(url: str, dst: Path, required: bool = False) -> bool:
    dst = dst.expanduser()

    if not dst.exists():
        log("git", f"cloning {url} -> {dst}")

        result = subprocess.run(
            ["git", "clone", "--depth", "1", url, str(dst)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            error = result.stderr.strip() or f"git exited with code {result.returncode}"
            message = f"could not clone {url}: {error}"

            if required:
                fatal(message)

            log("error", message)
            return False

        log("cloned", f"{url} -> {dst}")
        return True

    if not (dst / ".git").exists():
        message = f"{dst} exists but is not a git repository"

        if required:
            fatal(message)

        log("error", message)
        return False

    log("git", f"updating {dst}")

    result = subprocess.run(
        ["git", "pull", "--ff-only"],
        cwd=dst,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        error = result.stderr.strip() or f"git exited with code {result.returncode}"
        message = f"could not update {dst}: {error}"

        if required:
            fatal(message)

        log("error", message)
        return False

    log("updated", str(dst))
    return True
