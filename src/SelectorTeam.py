from __init__ import *
async def main():


    from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.teams import SelectorGroupChat
    from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
    from autogen_agentchat.ui import Console


    llm = AzureOpenAIChatCompletionClient(azure_deployment="aif-gpt-4.1",
                                          model="gpt-4.1-2025-04-14",
                                          api_version="2024-06-01",
                                          azure_endpoint=os.getenv("AOAI_ENDPOINT"),
                                          api_key=os.getenv("AOAI_API_KEY"))

    aga = AssistantAgent(name="Recherche",
                          description="Cet agent génère des informations fiables et pertinentes sur le sujet demandé.",
                          model_client=llm,
                          system_message="""
                          Analyse le sujet donné et rassemble rapidement les informations fiables,
                          références et points clés nécessaires à la rédaction d'un article de blog clair et informatif.
                          Ton role est de fournir des données pertinentes et précises pour aider à la rédaction.
                          Tu ne dois rien proposer d'autre que des données.
                          """)

    agb = AssistantAgent(name="Redacteur",
                          description="Cet agent écrit un article de blog clair, engageant, structuré et adapté au public cible à partir d’un plan et d’informations collectées préalablement.",
                          model_client=llm,
                          system_message="""
                          A partir de données existantes, rédige un article structuré à partir du plan fourni et des points clés,
                          en adoptant un ton engageant et adapté au public cible.
                          Utilise un langage clair, évite le plagiat et ne mentionne pas tes sources dans le texte.
                          Ton role est de produire un contenu original et engageant.
                          """)

    agc = AssistantAgent(name="SEO",
                          description="Cet agent optimise l’article pour le référencement naturel : intégration de mots-clés, titres optimisés, méta-description, balises et recommandations",
                          model_client=llm,
                          system_message="""
                          # Ce que tu dois faire
                          A partir d'un article, améliore l’article fourni pour le référencement naturel :
                          - intègre les mots-clés pertinents
                          - optimise les titres
                          - propose une méta-description
                          - structure le contenu avec des balises.
                          Ton rôle est d'optimiser l'article pour un bon contenu pour le SEO.

                          # Ce que tu ne dois JAMAIS faire
                          - Tu ne dois pas faire de suggestions sur le contenu lui-même.
                          - Tu ne dois pas réaliser de recherche.
                          - Tu ne dois pas revoir le contenu que tu viens juste de produire.
                          """)

    agd = AssistantAgent(name="Relecteur",
                          description="Cet agent vérifie la grammaire, l’orthographe, la clarté et la cohérence du texte, propose des corrections, et valide la version finale.",
                          model_client=llm,
                          system_message="""
                          # But
                          Proposer des corrections sur le texte fourni pour améliorer la grammaire, l’orthographe et le style.

                          # Workflow
                            1. Relis le texte fourni
                            2. Si tu penses que le texte est correct, réponds simplement avec le mot-clé "__END__".
                            2. Sinon, propose des corrections pour le texte concernant la grammaire, l’orthographe et le style.

                          # Règles
                            - Le mot-clé "__END__" ne DOIT PAS apparaitre si tu as des corrections à suggérer.
                            - Tu ne DOIS PAS corriger directement le texte, mais seulement signaler les erreurs.
                          """)

    tc = MaxMessageTermination(15) | TextMentionTermination("__END__")

    sp = """
    Vous êtes dans un jeu de rôle. Les rôles suivants sont disponibles :
    {roles}.
    Lisez la conversation suivante. Puis sélectionnez le prochain rôle à jouer parmi {participants}. Retournez uniquement le rôle.

    {history}

    Lisez la conversation ci-dessus. Puis sélectionnez le prochain rôle à jouer parmi {participants}. Retournez uniquement le rôle.
    """

    team = SelectorGroupChat(participants=[aga, agb, agc, agd],
                              model_client=llm,
                              selector_prompt=sp,
                              termination_condition=tc)
    print(team._selector_prompt)

    await Console(team.run_stream(task="Rédige un cours article sur les bénéfices de l'IA générative"))





run(main)