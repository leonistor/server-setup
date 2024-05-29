# run from fish shell:
# set -x PYTHONPATH "."; pyinfra inventory/test.py debian.install_base_packages

from pyinfra.api import deploy
from pyinfra.operations import apt, files, server


@deploy("Install common base packages")
def install_base_packages():
    apt.packages(
        packages=["vim", "sudo", "kitty-terminfo"],
        update=True,
        _sudo=True,
    )
