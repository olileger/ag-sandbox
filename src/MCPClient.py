import asyncio
from fastmcp import Client


client = Client("http://127.0.0.1:8000/mcp")


async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result[0].text)

        result = await client.call_tool("mix_words", {"a": "Hello", "b": "World"})
        print(result[0].text)

        result = await client.call_tool("factorial", {"n": 347})
        print(result[0].text)

        result = await client.call_tool("sha3_hash", {"data": "Hello, World!", "bits": 256})
        print(result[0].text)


asyncio.run(call_tool("Ford"))