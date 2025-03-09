import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from typing import List, Dict
from fastapi import HTTPException

# Base URL
BASE_URL = "https://www.bancoguayaquil.com/page-data/creditos"

class BancoGuayaquilService:
    """Service to fetch and process credit data from Banco Guayaquil using Selenium."""
    
    @staticmethod
    def fetch_page_source(url: str) -> Dict:
        """Uses Selenium to fetch the page source and extract JSON data."""
        options = Options()
        options.add_argument("--headless")  # Run without opening a browser window
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
        
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        
        # Extract raw page source
        page_source = driver.page_source
        driver.quit()  # Close browser session
        
        try:
            # Use BeautifulSoup to find <pre> tag and extract its content
            soup = BeautifulSoup(page_source, "html.parser")
            pre_tag = soup.find("pre")  # Locate the <pre> tag containing JSON
            if not pre_tag:
                raise ValueError("No JSON found inside <pre> tag")

            json_data = json.loads(pre_tag.text)  # Parse JSON from <pre> content
            return json_data
        
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse JSON from page source: {str(e)}")

    @classmethod
    def extract_credit_types(cls) -> List[Dict]:
        """
        Extracts credit types and their URLs from Banco Guayaquil's JSON data.
        """
        try:
            json_data = cls.fetch_page_source(BASE_URL)
            sections = json_data["result"]["data"]["contentfulPage"]["sections"]

            # Find the section containing the credit options
            credit_cards = next(
                (section["items"] for section in sections if section["__typename"] == "ContentfulCardContent"), []
            )

            # Extract credit titles and URLs
            credit_list = []
            for card in credit_cards:
                title = card.get("title")
                link = card["botones"][0]["linkPage"] if card.get("botones") else None

                if link:
                    link = link.replace("/creditos/", "").strip("/")  # Clean URL

                credit_list.append({"title": title, "link": link})

            return credit_list

        except KeyError as e:
            raise ValueError(f"Unexpected JSON structure: Missing key {e}")
        
    @classmethod
    def get_credit_details(cls, credit_type: str) -> Dict:
        """Fetches detailed credit information for a given credit type."""
        credit_url = f"{BASE_URL}/{credit_type}/page-data.json"
        data = cls.fetch_page_source(credit_url)

        try:
            credit_info = data["result"]["data"]["contentfulPage"]
            return {
                "slug": credit_info.get("slug"),
                "title": credit_info.get("title"),
                "description": credit_info.get("description"),
                "breadcrumb": credit_info.get("breadcrumb"),
                "tags": credit_info.get("tags", []),
                "sections": credit_info.get("sections", [])
            }
        
        except KeyError as e:
            raise HTTPException(status_code=500, detail=f"Unexpected JSON structure: Missing key {e}")

    @classmethod
    def get_all_credit_details(cls) -> Dict[str, Dict]:
        """Fetches details for all available credits."""
        credit_types = cls.extract_credit_types()

        results = {}
        for credit in credit_types:
            try:
                results[credit["title"]] = cls.get_credit_details(credit["link"])
            except Exception as e:
                results[credit["title"]] = {"error": str(e)}

        return results

