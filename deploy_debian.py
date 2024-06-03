from pyinfra.operations import apt, files, server
from io import StringIO
import glob

from lib.generic import bash_config, setup_tools, ping_google


def install_packages(packages=[]):
    apt.packages(
        name="base packages",
        packages=packages,
        update=True,
        _sudo=True,
    )


def install_base_packages():
    install_packages(["vim", "sudo", "kitty-terminfo"])


def install_work_packages():
    install_packages(
        [
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
        ]
    )


def install_ripgrep():
    deb_file = glob.glob(
        "ripgrep_*.deb",
        root_dir="tools",
    )[0]
    files.put(
        src=f"tools/{deb_file}",
        dest="/tmp",
        _sudo=True,
    )
    server.shell(
        commands=[
            f"dpkg -i /tmp/{deb_file}",
            f"rm /tmp/{deb_file}",
        ],
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
    # install_base_packages()
    # install_work_packages()
    # setup_unattended_upgrades()
    # setup_tools()
    install_ripgrep()
    create_admin_user()
    bash_config(user="leo", group="leo")
