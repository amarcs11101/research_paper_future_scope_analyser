# tools/patent_research_tool.py
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import json
import requests

class PatentSearchInput(BaseModel):
    topic: str = Field(..., description="Topic to search patents for, e.g., 'lithium battery'")

class PatentResearchTool(BaseTool):
    name:str = "Patent Metadata Extractor"
    description:str = "Searches for recent patents on a topic and extracts metadata like title, abstract, filing date"
    args_schema:str = PatentSearchInput

    def _run(self, topic: str) -> str:
        try:
            # Simulate results for now
            dummy_results = [
                {
                    "title": "Advanced Lithium Battery Design",
                    "abstract": "Improved energy density and charge cycles using nano-tech...",
                    "filing_date": "2023-11-15"
                },
                {
                    "title": "Solid-State Battery Innovation",
                    "abstract": "New approach to solid-state architecture increasing safety...",
                    "filing_date": "2022-09-10"
                }
            ]
            return json.dumps(dummy_results, indent=2)
        except Exception as e:
            return f"Error fetching patent data: {str(e)}"
