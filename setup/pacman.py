import subprocess


def is_installed(program: str) -> bool:
    cmd = f"pacman -Q {program}"
    return subprocess.run(
        cmd.split(),
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

        cmd = f"pacman -S --noconfirm {program}"
        result = subprocess.run(
            cmd.split(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print(f"[error] Could not install {
                  program}: {result.stderr.strip()}")
        else:
            print(f"[installed] {program}")
