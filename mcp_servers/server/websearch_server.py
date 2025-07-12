import httpx
from bs4 import BeautifulSoup
import os
from mcp.server.fastmcp import FastMCP
import asyncio
from dotenv import load_dotenv
load_dotenv(".env", override=True)

mcp = FastMCP(name = "search_tool")

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
    # sample_result = asyncio.run(get_google_search(query = "What is the news about Operation Sindoor", num_results_ent=3))
    # print(sample_result)
