from pyinfra.operations import apt, files, server
from io import StringIO
import glob

from lib.generic import (
    bash_config,
    check_distro,
    fix_ownership,
    install_astrovim,
    install_mise,
    install_tools,
    setup_binary_tools,
)


def install_packages(packages=[], name=""):
    apt.packages(
        name=f"install packages: {name}",
        packages=packages,
        update=True,
        _sudo=True,
    )


def install_base_packages():
    install_packages(
        [
            "vim",
            "sudo",
            "kitty-terminfo",
        ],
        name="base",
    )


def install_work_packages():
    install_packages(
        [
            # utils
            "curl",
            "gnupg",
            "wget",
            "htop",
            # dev
            "acl",
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
            # node: too old on Debian! use mise instead
            # "nodejs",
        ],
        name="work",
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
    check_distro(wanted="debian")

    # system
    install_base_packages()
    install_work_packages()
    setup_unattended_upgrades()

    # tools
    setup_binary_tools()

    # admin
    create_admin_user()
    bash_config(user="admin", group="admin")
    fix_ownership(user="admin", group="admin")
    install_mise(user="admin")
    install_tools(user="admin")
    install_astrovim(user="admin")

    # leo
    bash_config(user="leo", group="leo")
    fix_ownership(user="leo", group="leo")
    install_mise(user="leo")
    install_tools(user="leo")
    install_astrovim(user="leo")


def test():
    check_distro(wanted="debian")
    # install_base_packages()
    # install_work_packages()
    setup_binary_tools()
    # bash_config(user="leo", group="leo")
    # fix_ownership(user="leo", group="leo")
    # install_mise(user="leo")
    # install_tools(user="leo")
    # install_astrovim(user="leo")
