from __init__ import *
import random
async def main():



    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.ui import Console
    from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
    from autogen_ext.tools.mcp import StreamableHttpServerParams, McpWorkbench
    from datetime import timedelta
    import yaml



    # MCP Server config
    server_params = StreamableHttpServerParams(
        url="http://127.0.0.1:8000/mcp",
        timeout=timedelta(seconds=30),
        sse_read_timeout=timedelta(seconds=60 * 5),
        terminate_on_close=True,
    )

    # Test d'accès aux outils du MCP
    async with McpWorkbench(server_params=server_params) as wb:
        tools = await wb.list_tools()
        print(yaml.dump(tools, sort_keys=False, default_flow_style=False))
        tr = await wb.call_tool(tools[0]["name"], {"name": "Olivier"})
        print(tr.result[0].content)


    # Et c'est parti pour le show...
    llm = AzureOpenAIChatCompletionClient(azure_deployment="aif-gpt-4.1",
                                          model="gpt-4.1",
                                          api_version="2024-06-01",
                                          azure_endpoint=os.getenv("AOAI_ENDPOINT"),
                                          api_key=os.getenv("AOAI_API_KEY"))
    
    async with McpWorkbench(server_params=server_params) as wb:
        agent = AssistantAgent(name="Cryptographe",
                               model_client=llm,
                               workbench=wb,
                               system_message="""
                                Tu es un expert en cryptographie.
                                Tu t'appuis sur tes outils pour répondre aux questions de l'utilisateur.
                                """)

        await Console(agent.run_stream(task="Génère une phrase de 5 mots puis calcul son hash SHA3-256."))

run(main)
