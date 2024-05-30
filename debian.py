# run from fish shell:
# set -x PYTHONPATH "."; pyinfra inventory/test.py debian.install_base_packages

from pyinfra import logger
from pyinfra.api.deploy import deploy
from pyinfra.operations import apt, files
from io import StringIO


@deploy("Install common base packages")
def install_base_packages():
    apt.packages(
        packages=["vim", "sudo", "kitty-terminfo"],
        update=True,
        _sudo=True,
    )


def _bash_config():
    files.put(src="files/profile", dest=".profile", force=True)
    files.put(src="files/bashrc", dest=".bashrc", force=True)
    files.put(src="files/bash_aliases", dest=".bash_aliases", force=True)


@deploy("Setup bash")
def setup_bash():
    _bash_config()
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
