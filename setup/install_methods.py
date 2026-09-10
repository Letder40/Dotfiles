import shlex
import subprocess
from pathlib import Path

from .output import fatal, log
from .git import git_clone_or_pull


def pacman_has(package: str) -> bool:
    return subprocess.run(
        ["pacman", "-Qq", package],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def pacman(packages: list[str | None]) -> bool:
    packages = list(dict.fromkeys(package for package in packages if package))

    missing = []

    for package in packages:
        if not package:
            continue
        elif pacman_has(package):
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


def install_with_deps(name: str, deps: dict) -> bool:
    packages = [package.get("name", None) for package in deps.get("package", [])]
    success = pacman(packages)
    if not success:
        log("error - package", f"could not satisfy all dependencies of {name}")
        return False

    for dep in deps.get("curl", []):
        check_path = dep.get("check_path", None)
        if check_path is not None:
            check_path = Path(check_path)
        success = curl_sh(dep["url"], dep.get("params", ""), check_path)
        if not success:
            log("error - curl", f"could not satisfy all dependencies of {name}")
            return False

    for dep in deps.get("git", []):
        path = dep.get("path", None)
        if path is not None:
            path = Path(path)

        success = git_clone_or_pull(f"{dep["src"]}/{dep["repo"]}", path)
        if not success:
            log("error - git", f"could not satisfy all dependencies of {name}")
            return False

    return True
