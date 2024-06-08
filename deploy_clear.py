from pyinfra.operations import files, python, server
from io import StringIO

from lib.generic import (
    bash_config,
    check_distro,
    fix_ownership,
    install_astrovim,
    install_mise,
    install_neovim,
    install_tools,
    setup_binary_tools,
)


def install_packages(packages=[]):
    server.shell(
        commands=f"swupd bundle-add {' '.join(packages)}",
        _sudo=True,
    )


def install_base_packages():
    install_packages(
        [
            "acl",
            "containers-basic",
            "cronie",
            "dev-utils",
            "docker-compose",
            "editors",
            "fuse",
            "network-basic",
            "NetworkManager",
            "openssh-server",
            "package-utils",
            "sysadmin-basic",
            "sysadmin-remote",
            "tzdata",
            "user-basic",
        ]
    )


def install_work_packages():
    install_packages(
        [
            "perl-basic",
            "python3-basic",
        ]
    )


def setup_kitty(user="leo", group="leo"):
    files.put(
        src="files/xterm-kitty",
        dest=f"/home/{user}/.terminfo/x/xterm-kitty",
        user=user,
        group=group,
        mode="644",
        _sudo=True,
    )
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
        groups=["wheel"],
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
    # check autoupdate enabled
    # see: https://docs.pyinfra.com/en/3.x/using-operations.html#operation-output
    status = server.shell(
        commands="sudo swupd autoupdate",
        _sudo=True,
    )

    def callback():
        assert status.stdout == "Enabled"

    python.call(function=callback)

    # enable automatic service restart after update
    services = [
        "NetworkManager",
        "dbus",
        "docker",
        "cronie",
        "containerd",
        "systemd-logind",
    ]
    server.shell(
        commands=f"clr-service-restart allow {' '.join(services)}",
        _sudo=True,
    )


def setup_server():
    check_distro(wanted="clear")

    # system
    install_base_packages()
    install_work_packages()
    setup_unattended_upgrades()

    # tools
    setup_binary_tools()

    # admin
    create_admin_user()
    bash_config(user="admin", group="admin")
    setup_kitty(user="admin", group="admin")
    fix_ownership(user="admin", group="admin")
    install_mise(user="admin")

    # install_neovim(user="admin")
    # install_astrovim(user="admin")

    # leo
    # setup_kitty(user="leo", group="leo")
    # bash_config(user="leo", group="leo")
    # fix_ownership(user="leo", group="leo")
    # install_ripgrep(user="leo")
    # install_neovim(user="leo")
    # install_astrovim(user="leo")


def test():
    check_distro(wanted="clear")
    install_tools(user="admin")
