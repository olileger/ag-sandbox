from __init__ import *
import random

async def mix_words(a: str, b: str) -> str:
    """
    Mixes two words in a random order.
    This function takes two strings and returns a new string where the two input strings
    are concatenated in a random order. There is a 50% chance that the first word will
    come before the second word, and a 50% chance that the second word will come before
    the first word.
    """
    return f"{a}{b}" if random.randint(0, 1) == 0 else f"{b}{a}"



async def main():
    from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.ui import Console


    llm = AzureOpenAIChatCompletionClient(azure_deployment="aif-gpt-4.1",
                                        model="gpt-4.1",
                                        api_version="2024-06-01",
                                        azure_endpoint=os.getenv("AOAI_ENDPOINT"),
                                        api_key=os.getenv("AOAI_API_KEY"))

    agent = AssistantAgent(name="Melangeur",
                           model_client=llm,
                           tools=[mix_words],
                           system_message="""
                                   Tu dois faire 2 choses:
                                   1) Identifie 10 mots correspondant au thème donné par l'utilisateur.
                                   2) Mélange chaque mot avec les autres sur l'ensemble des cas possibles.

                                   Tu affiches ensuite les mots de base puis les mots mélangés.
                                   Exemple de réponse:
                                     Mots de base: rose, tulipe, lys
                                     Mots mélangés:
                                     - RoseTulipe
                                     - RoseLys
                                     - TulipeRose
                                     - TulipeLys
                                     - LysRose
                                     - LysTulipe
                                   """)

    await Console(agent.run_stream(task="Thème: L'IA générative"))

run(main)