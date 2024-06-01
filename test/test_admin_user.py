import sys
import logging

sys.path.append("../inventory")
from inventory import test

testinfra_hosts = test.debians


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
    result = host.run("echo 'test123#' | su -c env - admin")
    # logging.info(result.stdout)
    assert "EDITOR=vim" in result.stdout
    assert "PAGER=moar" in result.stdout
