import httpx
from mcp.server.fastmcp import FastMCP
from typing import Any
import asyncio
import httpx
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
load_dotenv(".env", override=True)


mcp = FastMCP(name = "mcp")

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



async def scrape_website(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout = 10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            paragraph = soup.find_all("p")
            full_text = " ".join([p.get_text() for p in paragraph])
            return full_text
        except Exception as e:
            print("Error fetching the content", e)
            return " "

async def format_search_results(json_body: dict, num_results = 3):
    result_list = []
    for result in json_body["organic"][:num_results]:
        link = result.get('link', "unknown")
        if link != "unknown":
            scraped_text = await scrape_website(link)
            
        result_body = f"""
        Title: {result.get('title', "unknown")}
        Link: {link}
        Snippet: {result.get('snippet', "unknown")}
        Full_text: {scraped_text}
        """
        result_list.append(result_body)

    return "\n -- \n".join(result_list)

@mcp.tool()
async def get_google_search(query: str, num_results_ent: int) -> str:
    """
        Make Request to make a google search
    
    """

    headers = {
      'X-API-KEY': os.getenv("SERPER_API_KEY"),
      'Content-Type': 'application/json'
    }

    payload = {
        "q": query
    }
    SERPER_API_URL = "https://google.serper.dev/search"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(SERPER_API_URL, headers=headers, json = payload)
            response.raise_for_status()
            final_text = await format_search_results(response.json(), num_results = num_results_ent)
            return final_text
        except Exception as e:
            print(e)
            return e 


if __name__ == "__main__":
    mcp.run(transport="stdio")
