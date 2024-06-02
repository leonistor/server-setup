from pyinfra.operations import apt, files, server
from pyinfra import logger
from io import StringIO

from lib.generic import bash_config, setup_tools, ping_google


def install_packages(packages=[]):
    server.shell(
        commands=f"swupd bundle-add {' '.join(packages)}",
        _sudo=True,
    )


def install_base_packages():
    install_packages(
        [
            "containers-basic",
            "cronie",
            "dev-utils",
            "dev-utils-dev",
            "docker-compose",
            "editors",
            "fuse",
            "neovim",
            "network-basic",
            "NetworkManager",
            "openssh-server",
            "os-core-update",
            "package-utils",
            "perl-basic",
            "python3-basic",
            "sysadmin-basic",
            "sysadmin-remote",
            "telemetrics",
            "tzdata",
            "user-basic",
        ]
    )


def install_work_packages():
    install_packages(
        [
            "go-basic",
            "nodejs-basic",
            "kernel-native",
            "machine-learning-basic",
            "os-clr-on-clr",
        ]
    )


def _install_ripgrep():
    return


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


def setup_admin():
    create_admin_user()
    bash_config(user="admin", group="admin")


def setup_unattended_upgrades():
    # using https://wiki.debian.org/UnattendedUpgrades
    install_packages(["unattended-upgrades", "apt-listchanges"])
    server.shell(
        commands="echo unattended-upgrades unattended-upgrades/enable_auto_updates boolean true | debconf-set-selections",
        _sudo=True,
    )
    server.shell(
        commands="dpkg-reconfigure -f noninteractive unattended-upgrades",
        _sudo=True,
    )


def setup_server():
    install_base_packages()
    # install_packages()
    # setup_unattended_upgrades()
    # setup_tools()
    # create_admin_user()
    # bash_config(user="admin", group="admin")
    # bash_config(user="leo", group="leo")
