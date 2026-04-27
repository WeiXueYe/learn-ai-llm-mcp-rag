import asyncio
from agent import Agent
from rich import print as rprint
import os

from embedding_retriever import EembeddingRetriever
from mcp_client import MCPClient
from mcp_tools import PresetMcpTools
from utils import pretty
from utils.info import DEFAULT_MODEL_NAME, PROJECT_ROOT_DIR
from vector_store import VectorStoreItem

ENABLED_MCP_CLIENTS = []
for mcp_tool in [
    PresetMcpTools.filesystem.append_mcp_params(f" {PROJECT_ROOT_DIR!s}"),
    PresetMcpTools.fetch,
]:
    rprint(mcp_tool.shell_cmd)
    mcp_client = MCPClient(**mcp_tool.to_common_params())
    ENABLED_MCP_CLIENTS.append(mcp_client)


KNOWLEDGE_BASE_DIR = PROJECT_ROOT_DIR / "output"
KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)

PRETTY_LOGGER = pretty.ALogger("[RAG]")


async def prepare_knowleage_data():
    PRETTY_LOGGER.title("PREPARE_KNOWLEAGE_DATA")
    if list(KNOWLEDGE_BASE_DIR.glob("*.md")):
        rprint(
            "[green]knowledge base already exists, skip prepare_knowleage_data[/green]"
        )
        return
    agent = Agent(
        model=DEFAULT_MODEL_NAME,
        mcp_clients=ENABLED_MCP_CLIENTS,
    )
    try:
        await agent.init()
        resp = await agent.invoke(
            f"爬取 https://jsonplaceholder.typicode.com/users 的内容, 在 {KNOWLEDGE_BASE_DIR!s} 每个人创建一个md文件, 保存基本信息"
        )
        rprint(resp)
    finally:
        await agent.cleanup()


async def retrieve_context(prompt: str):
    er = EembeddingRetriever(os.getenv("EMBEDDING_MODEL"))
    for path in KNOWLEDGE_BASE_DIR.glob("*.md"):
        document = path.read_text()
        await er.embed_documents(document)

    context: list[VectorStoreItem] = await er.retrieve(prompt)
    PRETTY_LOGGER.title("CONTEXT")
    rprint(context)
    return "\n".join([c.document for c in context])


async def rag():
    prompt = f"根据Bret的信息, 创作一个他的故事, 并且把他的故事保存到 {KNOWLEDGE_BASE_DIR / 'story' !s}文件夹下，故事需要包含他的基本信息和故事。文件格式是.md, 文件名是Bret的名字 ,"

    context = await retrieve_context(prompt)

    agent = Agent(
        model=DEFAULT_MODEL_NAME, 
        mcp_clients=ENABLED_MCP_CLIENTS,
        context=context,
    )
    try:
        await agent.init()
        resp = await agent.invoke(prompt)
        rprint(resp)
    finally:
        await agent.cleanup()



async def main():
    # await prepare_knowleage_data()
    await rag()


if __name__ == "__main__":
    asyncio.run(main())

