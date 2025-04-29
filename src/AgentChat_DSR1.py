from __init__ import *
async def main():


    from autogen_ext.models.azure import AzureAIChatCompletionClient
    from azure.core.credentials import AzureKeyCredential
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.ui import Console


    llm = AzureAIChatCompletionClient(endpoint=os.getenv("DSR1_ENDPOINT"),
                                      credential=AzureKeyCredential(os.getenv("DSR1_API_KEY")),
                                      model="aif-dsr1",
                                      model_info=
                                      {
                                          "family": "r1",
                                          "function_calling": False,
                                          "json_output": False,
                                          "structured_output": True,
                                          "vision": False
                                      })

    agent = AssistantAgent(name="Simplificateur",
                           model_client=llm,
                           system_message="Tu expliques des concepts complexes de manière simple et accessible, comme si tu parlais avec un enfant de 7 ans")

    await Console(agent.run_stream(task="comment marche un avion"))





run(main)