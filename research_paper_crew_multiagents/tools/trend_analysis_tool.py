# tools/trend_analysis_tool.py
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import json

class TrendAnalysisInput(BaseModel):
    patents_json: str = Field(..., description="JSON string of patent metadata to analyze trends")

class TrendAnalysisTool(BaseTool):
    name :str= "Patent Trend Analyzer"
    description:str = "Analyzes a list of patents and detects innovation trends, tech shifts, and dominant themes"
    args_schema: type[BaseModel]  = TrendAnalysisInput

    def _run(self, patents_json: str) -> str:
        try:
            patents = json.loads(patents_json)
            print("###################################### trend analysis tools ######################################")
            print(f"trend analysis tools: {patents}")
            print("########################################### END ###########################################")
          
            keywords = [p["title"].lower() for p in patents]
            trends = []

            if any("solid-state" in k for k in keywords):
                trends.append("Growing focus on solid-state battery technology")
            if any("nano" in k or "energy density" in k for k in keywords):
                trends.append("Increasing emphasis on nanotech and performance improvements")

            return "\n".join(trends) if trends else "No clear trend found."
        except Exception as e:
            return f"Error analyzing trends: {str(e)}"
