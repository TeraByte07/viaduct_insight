from pydantic import BaseModel, HttpUrl
from typing import Optional, List

class AnalysisRequest(BaseModel):
    domain: HttpUrl
    keywords: Optional[List[str]] = None
    competitors: Optional[List[str]] = None

class KeywordInsight(BaseModel):
    keyword: str
    position: int
    traffic: float
    difficulty: Optional[int] = None

class BacklinkInsight(BaseModel):
    referring_domain: str
    backlinks: int

class AnalysisResponse(BaseModel):
    domain: str
    total_backlinks: int
    referring_domains: int
    top_keywords: List[KeywordInsight]
    top_backlinks: List[BacklinkInsight]

class DomainRequest(BaseModel):
    query: str  # can be a keyword or domain
    search_type: Optional[str] = "organic"  # e.g., organic, news, images

class SearchResult(BaseModel):
    title: str
    link: str
    snippet: Optional[str] = None

class DomainResponse(BaseModel):
    query: str
    total_results: int
    results: List[SearchResult]

