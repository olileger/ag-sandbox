from __init__ import *
import random
async def main():



    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.ui import Console
    from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
    from autogen_ext.tools.mcp import StreamableHttpServerParams, StreamableHttpMcpToolAdapter
    from datetime import timedelta



    # MCP Server config
    server_params = StreamableHttpServerParams(
        url="http://127.0.0.1:8000/mcp",
        timeout=timedelta(seconds=30),
        sse_read_timeout=timedelta(seconds=60 * 5),
        terminate_on_close=True,
    )
    t_greet = await StreamableHttpMcpToolAdapter.from_server_params(server_params, "greet")
    t_mix_words = await StreamableHttpMcpToolAdapter.from_server_params(server_params, "mix_words")
    t_factorial = await StreamableHttpMcpToolAdapter.from_server_params(server_params, "factorial")
    t_sha3_hash = await StreamableHttpMcpToolAdapter.from_server_params(server_params, "sha3_hash")


    # Et c'est parti pour le show...
    llm = AzureOpenAIChatCompletionClient(azure_deployment="aif-gpt-4.1",
                                        model="gpt-4.1",
                                        api_version="2024-06-01",
                                        azure_endpoint=os.getenv("AOAI_ENDPOINT"),
                                        api_key=os.getenv("AOAI_API_KEY"))
    
    agent = AssistantAgent(name="Cryptographe",
                           model_client=llm,
                           tools=[t_greet, t_mix_words, t_factorial, t_sha3_hash],
                           system_message="""
                                   Tu es un expert en cryptographie.
                                   Tu t'appuis sur tes outils pour répondre aux questions de l'utilisateur.
                                   """)

    await Console(agent.run_stream(task="Génère une phrase de 5 mots puis calcul son hash SHA3."))



run(main)
