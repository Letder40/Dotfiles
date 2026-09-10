import subprocess

from .output import log, fatal


def setup_service(service: str, user: bool = False, required: bool = False):
    cmd = user \
        and f"systemctl enable --user --now {service}"\
        or f"sudo systemctl enable --now {service}"

    errcode = subprocess.run(
        cmd.split(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ).returncode

    if required and errcode != 0:
        fatal(f"service: {service} could not be enabled")
    elif errcode != 0:
        log("service", f"{service} could not be enabled")
    else:
        log("service", f"{service} started and enabled")
