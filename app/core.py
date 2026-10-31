"""Capability-bound inventory tools. Approval is an out-of-band operator action."""

import hashlib
import json
import tempfile
import time
import uuid
from pathlib import Path
from sqlalchemy import Integer, String, Float, select, update
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base, database


class Product(Base):
    __tablename__ = "products"
    sku: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str]
    quantity: Mapped[int] = mapped_column(Integer)


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    sku: Mapped[str]
    quantity: Mapped[int]
    fingerprint: Mapped[str]
    status: Mapped[str]
    expires: Mapped[float] = mapped_column(Float)


class Inventory:
    def __init__(self, url=None):
        self.engine, self.sessions = database(url)
        with self.sessions.begin() as s:
            if not s.get(Product, "LAP-01"):
                s.add_all(
                    [
                        Product(sku="LAP-01", name="Demo laptop", quantity=7),
                        Product(sku="DOCK-02", name="USB dock", quantity=12),
                    ]
                )

    def search(self, query=""):
        with self.sessions() as s:
            return [
                dict(sku=p.sku, name=p.name, available=p.quantity)
                for p in s.scalars(
                    select(Product).where(Product.name.ilike(f"%{query}%")).order_by(Product.sku)
                )
            ]

    def prepare(self, sku, quantity, scopes, now=None):
        if "orders:prepare" not in scopes:
            raise PermissionError("orders:prepare capability required")
        if type(quantity) is not int or not 1 <= quantity <= 100:
            raise ValueError("quantity must be an integer in 1..100")
        with self.sessions.begin() as s:
            product = s.get(Product, sku)
            if not product or product.quantity < quantity:
                raise ValueError("insufficient inventory")
            payload = json.dumps([sku, quantity], separators=(",", ":"))
            order = Order(
                id=str(uuid.uuid4()),
                sku=sku,
                quantity=quantity,
                fingerprint=hashlib.sha256(payload.encode()).hexdigest(),
                status="pending",
                expires=(now or time.time()) + 300,
            )
            s.add(order)
            return dict(
                id=order.id, sku=sku, quantity=quantity, status="pending", fingerprint=order.fingerprint
            )

    def approve(self, order_id, fingerprint, now=None):
        with self.sessions.begin() as s:
            o = s.scalar(select(Order).where(Order.id == order_id).with_for_update())
            if not o or o.fingerprint != fingerprint:
                raise ValueError("action mismatch")
            if o.status == "committed":
                return {"id": o.id, "status": o.status, "replayed": True}
            if o.status != "pending" or o.expires <= (now or time.time()):
                raise ValueError("order is no longer approvable")
            claimed = s.execute(
                update(Order).where(Order.id == o.id, Order.status == "pending").values(status="committed")
            )
            if claimed.rowcount != 1:
                raise ValueError("order already processed")
            stock = s.execute(
                update(Product)
                .where(Product.sku == o.sku, Product.quantity >= o.quantity)
                .values(quantity=Product.quantity - o.quantity)
            )
            if stock.rowcount != 1:
                raise ValueError("stock changed; prepare again")
            return {"id": o.id, "status": "committed", "replayed": False}


def demo(mode="fixture"):
    with tempfile.TemporaryDirectory() as d:
        inv = Inventory("sqlite:///" + str(Path(d) / "inventory.sqlite"))
        before = inv.search("laptop")
        order = inv.prepare("LAP-01", 2, {"orders:prepare"})
        result = inv.approve(order["id"], order["fingerprint"])
        replay = inv.approve(order["id"], order["fingerprint"])
        return dict(before=before, prepared=order, approved=result, replay=replay, after=inv.search("laptop"))


def evaluate(mode="fixture"):
    result = demo(mode)
    return {
        "passed": result["after"][0]["available"] == 5 and result["replay"]["replayed"],
        "case": "approval replay cannot decrement inventory twice",
        "observed_stock": result["after"][0]["available"],
    }
