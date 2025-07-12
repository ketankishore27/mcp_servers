import httpx
from mcp.server.fastmcp import FastMCP
from typing import Any
import asyncio

mcp = FastMCP(name = "weather_tool")

## Weather API
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """
        Make Request for NWS API with proper error handling
    
    """

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(e)
            return None


def format_alert(response_body: dict):
    props = response_body["properties"]
    return f"""
    Event: {props.get('event', 'Unknown')}
    Area: {props.get('areaDesc', 'Unknown')}
    Severity: {props.get('severity', 'Unknown')}
    Description: {props.get('description', 'No Description Available')}
    Instruction: {props.get('instruction', 'No Specific instructions provided')}
    """

@mcp.tool()
async def get_alerts(state: str) -> str:
    """
        Get weather alerts for a US State

        Args: 
            state: Two letter US State Code {e.g. CA, NY}

    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found"
        
    if not data["features"]:
        return "No Active alerts for this state"

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n--- \n".join(alerts)

if __name__ == "__main__":
    mcp.run(transport='stdio')
    # mcp dev weather_server.py

