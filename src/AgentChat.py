from __init__ import *
async def main():


    from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.ui import Console


    llm = AzureOpenAIChatCompletionClient(azure_deployment="aif-gpt-4.1",
                                        model="gpt-4.1",
                                        api_version="2024-06-01",
                                        azure_endpoint=os.getenv("AOAI_ENDPOINT"),
                                        api_key=os.getenv("AOAI_API_KEY"))

    agent = AssistantAgent(name="Simplificateur",
                           model_client=llm,
                           system_message="Tu expliques des concepts complexes de manière simple et accessible, comme si tu parlais avec un enfant de 7 ans")

    await Console(agent.run_stream(task="comment marche un avion"))





run(main)