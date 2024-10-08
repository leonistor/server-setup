import click
from pyinfra.operations import files, server
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
    # user binaries
    files.directory(
        path=f"/home/{user}/.local/bin",
        present=True,
        user=user,
        group=group,
        mode="755",
        _sudo=True,
    )


def setup_binary_tools():
    """Binary tools not available with mise"""
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
        if distro in ["Debian", "Ubuntu", "Pop!_OS"]:
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


def fix_ownership(user="leo", group="leo", folders=[".local", ".terminfo"]):
    """
    Correct ownership of folders in the home directory of the user.
    """
    commands = [
        f"chown --recursive {user}:{group} /home/{user}/{folder}" for folder in folders
    ]
    server.shell(
        commands=commands,
        _sudo=True,
        _ignore_errors=True,
        _continue_on_error=True,
    )


def install_mise(user="leo"):
    server.shell(
        commands="curl https://mise.run | sh",
        _sudo_user=user,
        _sudo=True,
    )


def install_tools(user="leo"):
    tools = ["ripgrep", "fd", "neovim"]
    server.shell(
        commands=f"mise use {' '.join(tools)} --yes",
        _sudo_user=user,
        _use_sudo_login=True,
        _sudo=True,
    )


def ping_google():
    server.shell(commands="ping -c 3 google.com")
