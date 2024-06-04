import click
from distro import LinuxDistribution
from pyinfra.operations import cargo, files, server
from pyinfra import logger
from io import StringIO

from pyinfra import host  # type: ignore
from pyinfra.facts.server import LinuxName


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
    # rootless npm setup
    files.directory(
        path=f"/home/{user}/.npm-packages",
        present=True,
        user=user,
        group=group,
        mode="755",
        _sudo=True,
    )
    files.put(
        src=StringIO(f"prefix=/home/{user}/.npm-packages"),
        dest=f"/home/{user}/.npmrc",
        user=user,
        group=group,
        mode="644",
        _sudo=True,
    )
    # user binaries
    files.directory(
        path=f"/home/{user}/.local/bin",
        present=True,
        user=user,
        group=group,
        mode="755",
        _sudo=True,
    )


def setup_tools():
    logger.info("DO NOT FORGET:")
    logger.info("run scripts/get-tools.sh for latest binaries")
    files.sync(
        name="tools binaries",
        src="tools",
        dest="/usr/local/bin",
        exclude=[".gitkeep", "*.deb"],
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


def install_neovim(user="leo"):
    """
    Install neovim latest version using
    [bob](https://github.com/MordechaiHadad/bob)
    """
    cargo.packages(name="bob-nvim", latest=True)
    server.shell(
        commands="bob use stable",
        _sudo_user=user,
        _use_sudo_login=True,
        _sudo=True,
        _ignore_errors=True,
    )
    # simlink to binary
    files.link(
        path=f"/home/{user}/.local/bin/nvim",
        target=f"/home/{user}/.local/share/bob/nvim-bin/nvim",
        user=user,
    )


def install_astrovim(user="leo"):
    # [astrovim](https://github.com/astrovim/astrovim)
    server.script(
        src="files/clean-nvim.sh",
        _sudo_user=user,
        _use_sudo_login=True,
        _sudo=True,
        _ignore_errors=True,
    )
    server.shell(
        commands=[
            "git clone --depth 1 https://github.com/AstroNvim/template ~/.config/nvim",
            "rm -rf ~/.config/nvim/.git",
            "nvim --headless +q",
        ],
        _sudo_user=user,
        _use_sudo_login=True,
        _sudo=True,
        _ignore_errors=True,
    )


def check_distro(wanted):
    try:
        assert wanted in ["debian", "clear"], "Distro must be one of 'debian' or 'clear"

        distro = host.get_fact(LinuxName)
        if distro == "Debian":
            assert wanted == "debian", f"cannot run {wanted} on Debian"
        elif distro == "Clear Linux OS":
            assert wanted == "clear", f"cannot run {wanted} on Clear Linux OS"
        else:
            assert 1 == 0, f"unknown distro {distro}"
    except AssertionError as err:
        logger.error(
            msg=click.style(f"ERROR: {err}", fg="red", bold=True),
            exc_info=True,
        )
        exit(1)


def ping_google():
    server.shell(commands="ping -c 3 google.com")
