from pydantic import BaseModel, Field
from typing import List, Optional

class CompanyResearchState(BaseModel):
    """Pydantic model for company research state tracking."""
    
    company_name: str = Field(..., description="The official name of the company.")
    company_url: Optional[str] = Field(None, description="Official company website URL (extracted).")
    initial_documents: Optional[str] = Field(None, description="Initial background information on the company.")
    research_findings: List[dict] = Field(default=[], description="List of research insights extracted from Tavily.")
