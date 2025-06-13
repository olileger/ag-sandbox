from __init__ import *
async def main():


    from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.teams import Swarm
    from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
    from autogen_agentchat.ui import Console


    llm = AzureOpenAIChatCompletionClient(azure_deployment="aif-gpt-4.1",
                                          model="gpt-4.1",
                                          api_version="2024-06-01",
                                          azure_endpoint=os.getenv("AOAI_ENDPOINT"),
                                          api_key=os.getenv("AOAI_API_KEY"))

    aga = AssistantAgent(name="Recherche",
                          description="Cet agent génère des informations fiables et pertinentes sur le sujet demandé.",
                          model_client=llm,
                          handoffs=["Redacteur"],
                          system_message="""
                          Analyse le sujet donné et rassemble rapidement les informations fiables,
                          références et points clés nécessaires à la rédaction d'un article de blog clair et informatif.
                          Ton role est de fournir des données pertinentes et précises pour aider à la rédaction.
                          Tu ne dois rien proposer d'autre que des données.
                          Lorsque tu as terminé tu peux transférer ton travail à l'agent Redacteur.
                          """)

    agb = AssistantAgent(name="Redacteur",
                          description="Cet agent écrit un article de blog clair, engageant, structuré et adapté au public cible à partir d’un plan et d’informations collectées préalablement.",
                          model_client=llm,
                          handoffs=["Relecteur"],
                          system_message="""
                          # But
                          A partir de données de l'agent Recherche, rédige un article structuré à partir du plan fourni et des points clés,
                          en adoptant un ton engageant et adapté au public cible.
                          Utilise un langage clair, évite le plagiat et ne mentionne pas tes sources dans le texte.
                          Ton role est de produire un contenu original et engageant.

                          # Workflow
                            1. Rédige un contenu
                            2. Lorsque tu as terminé:
                              a) tu affiches ton travail.
                              b) tu transfères l'action à l'agent Relecteur.

                          # Règles
                            - Tu dois rédiger un article de blog clair et engageant.
                            - Tu as toujours un contenu à proposer, même si c'est un brouillon.
                          """)

    agc = AssistantAgent(name="Relecteur",
                          description="Cet agent vérifie la grammaire, l’orthographe, la clarté et la cohérence du texte, propose des corrections, et valide la version finale.",
                          model_client=llm,
                          handoffs=["Redacteur", "SEO"],
                          system_message="""
                          # But
                          Tu dois proposer des corrections sur le texte fourni par l'agent Redacteur pour améliorer la grammaire, l’orthographe et le style.

                          # Workflow
                            1. Relis le texte fourni par l'agent Redacteur.
                            2. Identifie si tu as des corrections à proposer concernant la grammaire, l’orthographe et le style.
                            3. Affiche ton constat: pas de corrections ou corrections à apporter avec le détail le cas échéant.
                            4. Tu transfères ensuite ton travail selon les conditions suivantes :
                              a) Si tu as des corrections à proposer : tu transfères ton travail à l'agent Redacteur.
                              b) Si tu n'as pas de corrections à proposer: tu transfères ton travail à l'agent SEO.

                          # Règles
                            - Tu dois relire le texte attentivement.
                            - Tu ne DOIS PAS corriger directement le texte, mais seulement signaler les erreurs.
                          """)
    
    agd = AssistantAgent(name="SEO",
                          description="Cet agent optimise l’article pour le référencement naturel : intégration de mots-clés, titres optimisés, méta-description, balises et recommandations",
                          model_client=llm,
                          system_message="""
                          # Ce que tu dois faire
                          A partir d'un article, ajoute des éléments pour le référencement naturel :
                          - intègre les mots-clés pertinents
                          - optimise les titres
                          - propose une méta-description
                          - structure le contenu avec des balises.
                          Ton rôle est d'optimiser l'article pour un bon référencement SEO.
                          Lorsque tu as terminé, publie ta réponse et ajoute le mot-clé "__END__" pour signaler la fin du processus.

                          # Ce que tu ne dois JAMAIS faire
                          - Tu ne dois pas faire de suggestions sur le contenu lui-même.
                          - Tu ne dois pas réaliser de recherche.
                          - Tu ne dois pas revoir le contenu que tu viens juste de produire.
                          """)

    tc = MaxMessageTermination(20) | TextMentionTermination("__END__")

    team = Swarm(participants=[aga, agb, agc, agd], termination_condition=tc)

    await Console(team.run_stream(task="Rédige un cours article sur les bénéfices de l'IA générative"))





run(main)