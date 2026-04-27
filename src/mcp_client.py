"""
modified from https://modelcontextprotocol.io/quickstart/client  in tab 'python'
"""

import asyncio
from typing import Any, Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters, Tool
from mcp.client.stdio import stdio_client

from rich import print as rprint

from dotenv import load_dotenv

from mcp_tools import PresetMcpTools
from utils.info import PROJECT_ROOT_DIR
from utils.pretty import RICH_CONSOLE

load_dotenv()


class MCPClient:
    def __init__(
        self,
        name: str,
        command: str,
        args: list[str],
        version: str = "0.0.1",
    ) -> None:
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.name = name
        self.version = version
        self.command = command
        self.args = args
        self.tools: list[Tool] = []

    async def init(self) -> None:
        await self._connect_to_server()

    async def cleanup(self) -> None:
        try:
            await self.exit_stack.aclose()
        except Exception:
            rprint("在清理 MCP 客户端时出现错误，正在进行回溯并继续操作！")
            RICH_CONSOLE.print_exception()

    def get_tools(self) -> list[Tool]:
        return self.tools

    async def _connect_to_server(
        self,
    ) -> None:
        """
        连接到MCP服务器
        """
        server_params = StdioServerParameters(
            command=self.command,
            args=self.args,
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params),
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        self.tools = response.tools
        rprint("\n连接到MCP服务器，可用的工具如下：", [tool.name for tool in self.tools])

    async def call_tool(self, name: str, params: dict[str, Any]):
        return await self.session.call_tool(name, params)


async def example() -> None:
    for mcp_tool in [
        PresetMcpTools.filesystem.append_mcp_params(f" {PROJECT_ROOT_DIR!s}"),
        PresetMcpTools.fetch,
    ]:
        try:
            rprint(mcp_tool.shell_cmd)
            mcp_client = MCPClient(**mcp_tool.to_common_params())
            await mcp_client.init()
            tools = mcp_client.get_tools()
            rprint(tools)
        except Exception:
            rprint("调用mcp工具时出现错误，正在进行回溯并继续操作！")
            RICH_CONSOLE.print_exception()
        finally:
            await mcp_client.cleanup()
            


if __name__ == "__main__":
    asyncio.run(example())