import sys


def log(status: str, message: object) -> None:
    normalized_message = " ".join(str(message).splitlines()).strip()
    print(f"[{status}] {normalized_message}")


def fatal(message: object) -> None:
    log("fatal", message)
    sys.exit(1)
