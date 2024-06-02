import sys

from inventory.test import debians

if not "testinfra_hosts" in globals():
    testinfra_hosts = debians

from dotenv import dotenv_values

secrets = dotenv_values(".env")


def test_admin(host):
    assert host.user("admin").exists
    assert host.group("admin").exists
    assert host.user("admin").shell == "/bin/bash"


def test_packages(host):
    packages = ["vim", "sudo", "wget"]
    for package in packages:
        assert host.package(package).is_installed


def test_tools(host):
    commands = ["vim", "lf", "moar", "fd", "ttyd"]
    for command in commands:
        assert host.exists(command)


def test_bash_config(host):
    password = secrets["ADMIN_PASSWORD"]
    result = host.run(f"echo '{password}' | su -c env - admin")
    # logging.info(result.stdout)
    assert "EDITOR=vim" in result.stdout
    assert "PAGER=moar" in result.stdout
