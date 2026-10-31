"""Stdio authority comes from the operator's process environment, never tool arguments."""

import os
from functools import lru_cache
from typing import Annotated
from pydantic import Field
from mcp.server import MCPServer
from app.core import Inventory

server = MCPServer(
    "Business Inventory",
    instructions="Read inventory and prepare an order. Approval must happen outside the agent session.",
)


@lru_cache
def inventory():
    return Inventory()


@server.tool()
def search_inventory(query: str = "") -> list[dict]:
    """Search synthetic inventory. Does not mutate stock."""
    return inventory().search(query)


@server.tool()
def prepare_order(sku: str, quantity: Annotated[int, Field(strict=True, ge=1, le=100)]) -> dict:
    """Prepare an expiring order proposal. Does not commit stock."""
    scopes = set(os.getenv("MCP_SCOPES", "inventory:read").split(","))
    return inventory().prepare(sku, quantity, scopes)


if __name__ == "__main__":
    server.run()
