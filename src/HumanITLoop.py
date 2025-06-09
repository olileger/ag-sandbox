from __init__ import *
async def main():
    

    from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
    from autogen_agentchat.conditions import TextMentionTermination
    from autogen_agentchat.teams import RoundRobinGroupChat
    from autogen_agentchat.ui import Console
    from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

    # Create the agents.
    llm = AzureOpenAIChatCompletionClient(azure_deployment="aif-gpt-4.1",
                                          model="gpt-4.1",
                                          api_version="2024-06-01",
                                          azure_endpoint=os.getenv("AOAI_ENDPOINT"),
                                          api_key=os.getenv("AOAI_API_KEY"))
    
    assistant = AssistantAgent("assistant", model_client=llm)
    user_proxy = UserProxyAgent("user_proxy", input_func=input)  # Use input() to get user input from console.

    # Create the termination condition which will end the conversation when the user says "APPROVE".
    termination = TextMentionTermination("APPROVE")

    # Create the team.
    team = RoundRobinGroupChat([assistant, user_proxy], termination_condition=termination)

    # Run the conversation and stream to the console.
    stream = team.run_stream(task="Write a 4-line poem about the ocean. Ask the user for feedback and approval.",)
    # Use asyncio.run(...) when running in a script.
    await Console(stream)
    await llm.close()



run(main)