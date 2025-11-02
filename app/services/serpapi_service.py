import os
import requests
from app.schemas.analysis_schema import DomainRequest
from fastapi import HTTPException, status
from app.core.config import get_settings

settings = get_settings()
class SerpService:
    BASE_URL = "https://serpapi.com/search.json"

    def __init__(self):
        self.api_key = settings.SERPAPI_KEY
        if not self.api_key:
            raise HTTPException(status_code=500, detail="SERPAPI key not set in environment")

    def analyze_domain(self, request_data: DomainRequest):
        params = {
            "q": request_data.query,
            "engine": "google",
            "api_key": self.api_key
        }

        response = requests.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"SerpAPI error: {response.text}"
            )

        data = response.json()
        results = [
            {
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            }
            for item in data.get("organic_results", [])
        ]

        return {
            "query": request_data.query,
            "total_results": len(results),
            "results": results
        }
