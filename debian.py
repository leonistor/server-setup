# run from fish shell:
# set -x PYTHONPATH "."; pyinfra inventory/test.py debian.install_base_packages

from pyinfra import logger
from pyinfra.api.deploy import deploy
from pyinfra.operations import apt, files, server
from io import StringIO


@deploy("Install common base packages")
def install_base_packages():
    apt.packages(
        packages=["vim", "sudo", "kitty-terminfo"],
        update=True,
        _sudo=True,
    )


@deploy("Install base packages")
def install_packages():
    apt.packages(
        packages=[
            # utils
            "curl",
            "gnupg",
            "wget",
            "htop",
            # dev
            "build-essential",
            "autoconf",
            "automake",
            "gdb",
            "git",
            "libssl-dev",
            "libffi-dev",
            "zlib1g-dev",
            # python
            "python3-pip",
            "python3-venv",
            "python3-dev",
            # node
            "nodejs",
        ],
        update=True,
        _sudo=True,
    )


def _bash_config(user="leo", group="leo"):
    sources = ["profile", "bashrc", "bash_aliases"]
    for source in sources:
        files.put(
            src=f"files/{source}",
            dest=f".{source}.sh",
            force=True,
            user=user,
            group=group,
        )


@deploy("Setup bash")
def setup_bash(user="leo", group="leo"):
    _bash_config(user, group)
    files.directory(path=".local/bin", present=True, recursive=True)


@deploy("Setup tools")
def setup_tools():
    logger.info("DO NOT FORGET:")
    logger.info("run scripts/get-tools.sh for latest binaries")
    files.sync(
        name="tools binaries",
        src="tools",
        dest="/usr/local/bin",
        user="root",
        group="root",
        mode="755",
        delete=False,
        _sudo=True,
    )
    files.put(
        name="lf config",
        src=StringIO("set hidden true"),
        dest="/etc/lf/lfrc",
        user="root",
        group="root",
        _sudo=True,
    )


@deploy("admin user")
def admin_user():
    server.user(
        user="admin",
        password="$1$LWxAxY4C$24Xr5YWtD5v4.SYdF.IHM1",
        present=True,
        create_home=True,
        system=True,
        unique=True,
        _sudo=True,
    )
