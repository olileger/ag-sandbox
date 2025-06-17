from __init__ import *
async def main():


    from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
    from autogen_agentchat.agents import AssistantAgent, MessageFilterAgent, MessageFilterConfig, PerSourceFilter
    from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
    from autogen_agentchat.ui import Console


    llm = AzureOpenAIChatCompletionClient(azure_deployment="aif-gpt-4.1",
                                          model="gpt-4.1",
                                          api_version="2024-06-01",
                                          azure_endpoint=os.getenv("AOAI_ENDPOINT"),
                                          api_key=os.getenv("AOAI_API_KEY"))

    redaction = AssistantAgent(name="Redacteur",
                          description="Cet agent écrit un article de blog clair, engageant, structuré et adapté au public cible à partir d’un plan et d’informations collectées préalablement.",
                          model_client=llm,
                          system_message="""
                          Analyse le sujet donné et rassemble rapidement les informations fiables,
                          références et points clés nécessaires à la rédaction d'un article de blog clair et informatif.
                          Rédige ensuite un article structuré à partir des informations fournies.
                          Adopte un ton engageant et adapté au public cible.
                          Utilise un langage clair, évite le plagiat et ne mentionne pas tes sources dans le texte.
                          Ton role est de produire un contenu original et engageant.
                          """)

    relecture = AssistantAgent(name="Relecteur",
                          description="Cet agent vérifie la grammaire, l’orthographe, la clarté et la cohérence du texte et propose des corrections.",
                          model_client=llm,
                          system_message="""
                          # But
                          Propose des corrections sur le texte fourni pour améliorer la grammaire, l’orthographe et le style.

                          # Workflow
                            1. Relis le texte fourni
                            2. Identifie si tu as des corrections à proposer concernant la grammaire, l’orthographe et le style.
                            3. Si tu as des corrections à proposer : affiche tes corrections.
                            4. Si tu n'as pas de corrections à proposer: affiche le message "_OKVALIDE_".

                          # Règles
                            - Tu ne dois pas modifier le texte original, mais seulement proposer des corrections.
                          """)
    
    seo = AssistantAgent(name="SEO",
                          description="Cet agent optimise l’article pour le référencement naturel : intégration de mots-clés, titres optimisés, méta-description, balises et recommandations",
                          model_client=llm,
                          system_message="""
                          Ajoute des éléments pour le référencement naturel :
                          - intègre les mots-clés pertinents
                          - optimise les titres
                          - propose une méta-description
                          - structure le contenu avec des balises.
                          Ton rôle est d'optimiser le texte pour un bon référencement SEO.
                          """)


    # Add the nodes
    seo_last_redaction = MessageFilterAgent(
        name="seo_last_redaction",
        wrapped_agent=seo,
        filter=MessageFilterConfig(
            per_source=[
                PerSourceFilter(source="Relecteur", position="last", count=1),
            ]
        ),
    )
    dgb = DiGraphBuilder()
    dgb.add_node(redaction).add_node(relecture).add_node(seo_last_redaction)

    # Add edges
    dgb.add_edge(redaction, relecture)
    dgb.add_edge(relecture, seo_last_redaction, condition = lambda msg: "_OKVALIDE_" in msg.to_model_text())
    dgb.add_edge(relecture, redaction, condition=lambda msg: "_OKVALIDE_" not in msg.to_model_text())

    # Build the graph with entry point
    dgb.set_entry_point(redaction)
    graph = dgb.build()
    
    # Run the graph flow
    flow = GraphFlow(participants=dgb.get_participants(), graph=graph)
    await Console(flow.run_stream(task="Rédige un cours article sur les bénéfices de l'IA générative"))





run(main)