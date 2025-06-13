# AutoGen Sandbox

## Présentation

Ce projet est un bac à sable pour expérimenter et orchestrer des agents conversationnels basés sur AutoGen en version 0.4 et supérieure, avec différentes architectures d'équipe (Selector, Swarm, RoundRobin, etc.), des outils locaux ou distants (MCP), et une interface utilisateur Chainlit.
Ce projet vise essentiellement à démontrer les capacités d'AutoGen pour la construction d'agent et d'équipe d'agents.

## Prérequis
Les fichiers de code ont été validés pour être utilisé avec des endpoints Azure AI Foundry en utilisant le modèle OpenAI GPT-4.1 ainsi que DeepSeek R1 pour le fichier de code concerné.

Pour faire fonctionner l'ensemble des exemples il faut au préalable:
- Déployer un LLM `GPT-4.1` sur Azure AI Foundry
- Déployer un LLM `DeepSeek R1` sur Azure AI Foundry

## Installation

1. Cloner le dépôt
2. Installer les dépendances Python :

```
pip install -r requirements.txt
```

3. Configurer les accès aux modèles:
    - Créer un fichier `.env` à la racine du projet ou renommer le fichier `.env.template` en `.env` et mettre à jour les informations requises.
    - Y ajouter les sections suivantes avec les valeurs correspondantes à vos déploiements Azure AI Foundry:

```
AOAI_API_KEY=<placer ici la clé d'API Azure OpenAI>
AOAI_ENDPOINT=<placer ici le endpoint d'API Azure OpenAI>

DSR1_API_KEY=<placer ici la clé d'API DeepSeek R1>
DSR1_ENDPOINT=<placer ici le endpoint d'API DeepSeek R1>
```

4. Configurer Chainlit pour accéder au modèle:
    - Créer un fichier `model_config.yaml` à la racine du projet (fichier utilisé par Chainlit) renommer le fichier `model_config.yaml.template` en `.env` et mettre à jour les informations requises.

```
provider: autogen_ext.models.openai.AzureOpenAIChatCompletionClient
config:
  model: <Indiquer ici le modèle utiliser>
  azure_endpoint: <placer ici le endpoint d'API Azure OpenAI>
  azure_deployment: <Indiquer ici le nom du déploiement de votre modèle Azure OpenAI>
  api_version: 2024-12-01-preview
  api_key: <placer ici la clé d'API Azure OpenAI>
```


## Utilisation

- Lancer un script d'agent ou d'équipe depuis le dossier `src` (ou encore mieux, se mettre en mode `debug`et utiliser des breakpoints)
- Exemple: `python src/AssistantAgent_AOAI.py` pour démontrer l'execution d'un Agent AutoGen utilisant un modèle Azure OpenAI.

### Fichiers d'agents individuels
- `AssistantAgent_AOAI.py` : Agent simplificateur utilisant Azure OpenAI, explique des concepts complexes de façon simple.
- `AssistantAgent_DSR1.py` : Agent simplificateur utilisant un modèle Azure DSR1, même principe que ci-dessus.

### Fichiers d'équipes d'agents
- `SelectorTeam.py` : Équipe d'agents spécialisés (Recherche, Rédacteur, SEO, Relecteur) orchestrés par sélection dynamique du rôle à chaque tour.
- `SwarmTeam.py` : Équipe d'agents travaillant en parallèle (Swarm) sur la rédaction, l'optimisation SEO et la relecture d'un article.
- `RoundRobinTeam.py` : Deux agents collaborent en tour de rôle pour construire une phrase mot à mot.

### Interface et interaction utilisateur
- `HumanITLoop.py` : Exemple d'orchestration homme-dans-la-boucle avec validation utilisateur.
- `Chainlit.py` : Script principal pour lancer l'interface conversationnelle Chainlit avec une équipe assistant/critic/user.
  - Pour l'interface conversationnelle avec Chainlit, utiliser la commande suivante: `chainlit run .\src\Chainlit.py`

### Utilisation de tools et MCP
#### Tool local
- `ToolingLocal.py` : Agent assistant qui mélange des mots selon un thème donné, outil local `mix_words`.

#### Tool avec MCP
- Pour expérimenter l'utilisation d'outils MCP dans un agent AutoGen il faut au préalable lancer le serveur MCP local avec la commande `python src/MCPServer.py`. Ce serveur est disponible sur l'url `http://127.0.0.1:8000/mcp`.
- Pour vérifier la bonne disponibilité du serveur MCP vous pouvez utiliser le script MCP Client avec la commande `python src/MCPClient.py`. Ce script s'assure que le serveur MCP soit bien lancé et que les tools soient bien exposés.


- `ToolingMCP.py` : Ce fichier de code démontre l'utilisation de tools via MCP.
- `ToolingMCPWrkbnch.py` : Ce fichier de code démontre l'intérêt d'utiliser MCP Workbench pour la découverte et l'utilisation de capacités exposées par un MCP Server.


### Serveur et client MCP
- `MCPServer.py` : Serveur MCP exposant des outils (greet, mix_words, factorial, sha3_hash) via FastMCP.
- `MCPClient.py` : Client asynchrone pour tester les outils exposés par le serveur MCP.


## Ressources complémentaires

- Documentation Autogen : https://github.com/microsoft/autogen
- Documentation Chainlit : https://docs.chainlit.io
- Documentation Azure AI Foundry: https://learn.microsoft.com/en-us/azure/ai-foundry/


---

*Ce projet est destiné à l'expérimentation et à la démonstration de AutoGen >= 0.4*
