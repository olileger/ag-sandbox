from fastmcp import FastMCP
import random
import hashlib

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    """
    Greets the user with their name.
    This function takes a string input representing the user's name and returns a greeting message.
    """
    return f"Hello, {name}!"


@mcp.tool
def mix_words(a: str, b: str) -> str:
    """
    Mixes two words in a random order.
    This function takes two strings and returns a new string where the two input strings
    are concatenated in a random order. There is a 50% chance that the first word will
    come before the second word, and a 50% chance that the second word will come before
    the first word.
    """
    return f"{a}{b}" if random.randint(0, 1) == 0 else f"{b}{a}"


@mcp.tool
def factorial(n: int) -> int:
    """
    Calculates the factorial of a non-negative integer.
    This function takes a non-negative integer n and returns n! (n factorial),
    which is the product of all positive integers less than or equal to n.
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


@mcp.tool
def sha3_hash(data: str, bits: int = 256) -> str:
    """
    Computes the SHA3 hash of the given data.
    
    This function takes a string input and an optional bit length (default: 256),
    and returns the SHA3 hash of the input data as a hexadecimal string.
    
    Args:
        data: The string to hash
        bits: The bit length of the hash (224, 256, 384, or 512)
    
    Returns:
        The SHA3 hash as a hexadecimal string
    """
    
    if bits not in [224, 256, 384, 512]:
        raise ValueError("Bits must be one of: 224, 256, 384, 512")
    
    hash_function = getattr(hashlib, f"sha3_{bits}")
    return hash_function(data.encode()).hexdigest()


if __name__ == "__main__":
    mcp.run(transport="streamable-http")