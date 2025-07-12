from mcp.server.fastmcp import FastMCP
import subprocess
import asyncio

mcp = FastMCP("TerminalToolServer")

@mcp.tool()
async def terminal(command: str) -> str:
    """
    Execute a shell command on the server.

    Args:
        command (str): The shell command to execute. This should be a valid command string as you would enter in a terminal.

    Returns:
        str: The standard output of the command if successful, or the standard error message if the command fails.
    """
    try:
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        output = stdout.decode().strip() if stdout else stderr.decode().strip()
        return output
    except Exception as e:
        return f"Error: {e}"

@mcp.resource("file://desktop/mcpreadme")
async def read_mcp_readme() -> str:
    """
    Expose the contents of the mcpreadme.md file from the Desktop as an MCP resource.
    """
    try:
        return await asyncio.to_thread(
            lambda: open("/Users/A118390615/Desktop/mcpreadme.md", "r").read()
        )
    except Exception as e:
        return f"Error reading mcpreadme.md: {e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
    # import sys

    # if len(sys.argv) < 2:
    #     print("Usage: python server.py <command>")
    #     sys.exit(1)

    # command = " ".join(sys.argv[1:])
    # print(command)

    # async def run_terminal():
    #     result = await terminal(command)
    #     print(result)

    # asyncio.run(run_terminal())
