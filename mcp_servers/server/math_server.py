from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name = "math_tool")

@mcp.tool()
def add(num_a: float, num_b:float):
    """
    Adds two numbers
    """
    return num_a + num_b

@mcp.tool()
def multiply(num_a: float, num_b:float):
    """
    Multiplies two numbers
    """
    return num_a * num_b

if __name__ == "__main__":
    mcp.run(transport="stdio")

    
# uvicorn mcp.server.math_server:mcp --reload --host 0.0.0.0 --port 8000