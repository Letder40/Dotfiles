import os
import subprocess
from pathlib import Path

from .output import log, fatal


GIT_TIMEOUT_SECONDS = 60


def _run_git(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["GIT_TERMINAL_PROMPT"] = "0"
    environment["GIT_SSH_COMMAND"] = "ssh -oBatchMode=yes -oConnectTimeout=10"

    return subprocess.run(
        ["git", "-c", "http.lowSpeedLimit=1000", "-c", "http.lowSpeedTime=15", *command],
        cwd=cwd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        timeout=GIT_TIMEOUT_SECONDS,
        env=environment,
    )


def _failure(message: str, required: bool) -> bool:
    if required:
        fatal(message)

    log("error", message)
    return False


def git_clone_or_pull(url: str, dst: Path, required: bool = False) -> bool:
    dst = dst.expanduser()

    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        log("git", f"cloning {url} -> {dst}")

        try:
            result = _run_git(["clone", "--depth", "1", url, str(dst)])
        except subprocess.TimeoutExpired:
            return _failure(
                f"could not clone {url}: timed out after {GIT_TIMEOUT_SECONDS} seconds",
                required,
            )

        if result.returncode != 0:
            error = result.stderr.strip() or f"git exited with code {result.returncode}"
            message = f"could not clone {url}: {error}"

            return _failure(message, required)

        log("cloned", f"{url} -> {dst}")
        return True

    if not (dst / ".git").exists():
        message = f"{dst} exists but is not a git repository"

        return _failure(message, required)

    log("git", f"updating {dst}")

    try:
        result = _run_git(["pull", "--ff-only"], cwd=dst)
    except subprocess.TimeoutExpired:
        return _failure(
            f"could not update {dst}: timed out after {GIT_TIMEOUT_SECONDS} seconds",
            required,
        )

    if result.returncode != 0:
        error = result.stderr.strip() or f"git exited with code {result.returncode}"
        message = f"could not update {dst}: {error}"

        return _failure(message, required)

    log("updated", str(dst))
    return True
