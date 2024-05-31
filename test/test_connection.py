import sys

sys.path.append("../inventory")
from inventory import test

testinfra_hosts = test.all


def test_leo(host):
    assert host.user("leo").exists
