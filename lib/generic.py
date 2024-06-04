from pyinfra.operations import apt, files, server
from pyinfra import logger
from io import StringIO


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
    then [astrovim](https://github.com/astrovim/astrovim)
    """
    server.shell(
        commands=[
            # install bob. rust must be installed and configured for user
            "cargo install bob-nvim",
            # ask bob to install stable neovim
            "bob use stable",
        ],
        _sudo_user=user,
        _use_sudo_login=True,
        _sudo=True,
    )
    # simlink to binary
    files.link(
        path=f"/home/{user}/.local/bin/nvim",
        target=f"/home/{user}/.local/share/bob/nvim-bin/nvim",
        user=user,
    )


def ping_google():
    server.shell(commands="ping -c 3 google.com")
