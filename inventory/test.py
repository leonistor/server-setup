import getpass

_SUDO_PASSWORD = getpass.getpass(prompt="Sudo password: ")

test_hosts = [("192.168.64.2", {"_use_sudo_password": _SUDO_PASSWORD})]
