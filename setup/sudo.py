from pathlib import Path
from subprocess import run
from os import getuid, setuid, setgid

from .user import gid, uid


def is_root() -> bool:
    return getuid() == 0


def run_as_user(*args: str, cwd: Path | None = None):
    if not is_root():
        return

    run(
        args,
        check=True,
        cwd=cwd,
        preexec_fn=lambda: (
            setgid(gid),
            setuid(uid),
        )
    )
