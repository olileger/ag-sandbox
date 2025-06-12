from __init__ import *
import random
async def main():



    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.ui import Console
    from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
    from autogen_ext.tools.mcp import StreamableHttpServerParams, StreamableHttpMcpToolAdapter, McpWorkbench
    from datetime import timedelta
    import yaml



    # MCP Server config
    server_params = StreamableHttpServerParams(
        url="http://127.0.0.1:8000/mcp",
        timeout=timedelta(seconds=30),
        sse_read_timeout=timedelta(seconds=60 * 5),
        terminate_on_close=True,
    )

    async with McpWorkbench(server_params=server_params) as wb:
        tools = await wb.list_tools()
        print(yaml.dump(tools, sort_keys=False, default_flow_style=False))
        tr = await wb.call_tool(tools[0]["name"], {"name": "Olivier"})
        print(tr.result[0].content)



run(main)
