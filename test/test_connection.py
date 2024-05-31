import sys
import pytest

sys.path.append("../inventory")
from inventory import test

testinfra_hosts = test.all


@pytest.mark.filterwarnings("ignore:Unknown ssh-ed25519")
def test_leo(host):
    assert host.user("leo").exists
