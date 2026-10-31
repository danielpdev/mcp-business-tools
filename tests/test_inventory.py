import pytest
from app.core import Inventory


@pytest.fixture
def inv(tmp_path):
    return Inventory("sqlite:///" + str(tmp_path / "test.sqlite"))


def test_no_capability_no_order(inv):
    with pytest.raises(PermissionError):
        inv.prepare("LAP-01", 1, {"inventory:read"})
    assert inv.search("laptop")[0]["available"] == 7


def test_approval_replay_and_persistence(inv):
    order = inv.prepare("LAP-01", 2, {"orders:prepare"})
    inv.approve(order["id"], order["fingerprint"])
    assert inv.approve(order["id"], order["fingerprint"])["replayed"]
    assert Inventory(str(inv.engine.url)).search("laptop")[0]["available"] == 5


def test_tampering_expiry_and_stock_change(inv):
    order = inv.prepare("LAP-01", 7, {"orders:prepare"}, now=100)
    with pytest.raises(ValueError):
        inv.approve(order["id"], "tampered", now=101)
    with pytest.raises(ValueError):
        inv.approve(order["id"], order["fingerprint"], now=401)
    inv.approve(order["id"], order["fingerprint"], now=101)
    with pytest.raises(ValueError):
        inv.prepare("LAP-01", 1, {"orders:prepare"})


@pytest.mark.parametrize("quantity", [0, -1, 101, True, 1.5])
def test_invalid_quantities(inv, quantity):
    with pytest.raises(ValueError):
        inv.prepare("LAP-01", quantity, {"orders:prepare"})
