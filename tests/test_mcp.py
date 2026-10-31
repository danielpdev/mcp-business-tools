import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_real_stdio_protocol_and_capability_boundary(tmp_path):
    env = dict(
        os.environ, DATABASE_URL="sqlite:///" + str(tmp_path / "mcp.sqlite"), MCP_SCOPES="inventory:read"
    )
    async with stdio_client(
        StdioServerParameters(command=sys.executable, args=["-m", "app.server"], env=env)
    ) as (read, write):
        async with ClientSession(read, write) as client:
            await client.initialize()
            tools = await client.list_tools()
            assert {t.name for t in tools.tools} == {"search_inventory", "prepare_order"}
            result = await client.call_tool("search_inventory", {"query": "laptop"})
            assert not result.is_error
            denied = await client.call_tool("prepare_order", {"sku": "LAP-01", "quantity": 1})
            assert denied.is_error
            invalid = await client.call_tool("prepare_order", {"sku": "LAP-01", "quantity": -3})
            assert invalid.is_error
