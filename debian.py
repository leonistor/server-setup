# run from fish shell:
# set -x PYTHONPATH "."; pyinfra inventory/test.py debian.install_base_packages

from pyinfra import logger
from pyinfra.api.deploy import deploy
from pyinfra.operations import apt, files, server
from io import StringIO


# TODO: extract to package lists, call one fn
def install_base_packages():
    apt.packages(
        name="base packages",
        packages=["vim", "sudo", "kitty-terminfo"],
        update=True,
        _sudo=True,
    )


def install_packages():
    apt.packages(
        name="util and dev packages",
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


def bash_config(user="leo", group="leo"):
    sources = ["profile", "bashrc", "bash_aliases"]
    for source in sources:
        files.put(
            src=f"files/{source}",
            dest=f"/home/{user}/.{source}",
            force=True,
            user=user,
            group=group,
            mode="600",
            _sudo=True,
        )


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


def create_admin_user():
    server.user(
        name="create admin user",
        user="admin",
        password="$1$LWxAxY4C$24Xr5YWtD5v4.SYdF.IHM1",
        present=True,
        create_home=True,
        system=True,
        shell="/bin/bash",
        groups=[
            "cdrom",
            "floppy",
            "audio",
            "dip",
            "video",
            "plugdev",
            "users",
            "netdev",
        ],
        unique=True,
        _sudo=True,
    )
    files.put(
        src=StringIO("admin    ALL=(ALL:ALL) ALL"),
        dest="/etc/sudoers.d/admin",
        user="root",
        group="root",
        mode="440",
        _sudo=True,
    )


@deploy("admin user")
def setup_admin():
    create_admin_user()
    bash_config(user="admin", group="admin")


@deploy("setup server")
def setup_server():
    install_base_packages()
    install_packages()
    setup_tools()
    create_admin_user()
    bash_config(user="leo", group="leo")


# TODO: test new functionality
# TODO: npmrc and .local/bin
