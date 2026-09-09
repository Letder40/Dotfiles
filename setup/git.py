from pathlib import Path

from .sudo import run_as_user


def git_clone_or_pull(dst: Path, url: str):
    if not dst.exists():
        print("[git] clonning configuration")
        cmd = f"git clone {url} {dst.absolute().as_posix()}"
        run_as_user(cmd.split())
    else:
        print("[git] obteniendo cambios en la configuración")
        run_as_user("git", "pull", cwd=dst.absolute().as_posix())
