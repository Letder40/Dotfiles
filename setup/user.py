from pathlib import Path

from pwd import getpwnam
from .config import config

username = config["preferences"]["user"]
user = getpwnam(username)
uid = user.pw_uid
gid = user.pw_gid
home = Path(user.pw_dir)
