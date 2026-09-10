import subprocess
from os import getuid

from .output import fatal, log


def is_root() -> bool:
    return getuid() == 0


def cache_sudo() -> None:
    log("sudo", "caching credentials")
    result = subprocess.run(
        ["sudo", "-v"],
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        error = result.stderr.strip() or f"sudo exited with code {result.returncode}"
        fatal(f"could not cache sudo credentials: {error}")
