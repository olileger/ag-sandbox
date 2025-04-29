from __init__ import *
async def main():


    from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.teams import RoundRobinGroupChat
    from autogen_agentchat.ui import Console


    llm = AzureOpenAIChatCompletionClient(azure_deployment="aif-gpt-4.1",
                                        model="gpt-4.1",
                                        api_version="2024-06-01",
                                        azure_endpoint=os.getenv("AOAI_ENDPOINT"),
                                        api_key=os.getenv("AOAI_API_KEY"))

    system_message="""
                   Ton role est d'ajouter un mot à une phrase en faisant en sorte que la phrase soit toujours correcte.
                   Tu reçois en entrée: un mot ou une phrase.
                   Tu génères en sortie: ve mot ou cette phrase avec un mot supplémentaire.
                   Règle:
                   - Tu ne dois ajouter qu'UN SEUL mot.
                   - A tout moment la phrase doit avoir un sens.
                   """
    
    aga = AssistantAgent(name="A",
                         model_client=llm,
                         system_message=system_message)
    
    agb = AssistantAgent(name="B",
                         model_client=llm,
                         system_message=system_message)

    team = RoundRobinGroupChat([aga, agb],
                               max_turns=40)

    await Console(team.run_stream(task="Voici le premier mot: 'Bonjour'"))





run(main)