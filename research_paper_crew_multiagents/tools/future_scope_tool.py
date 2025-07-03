# tools/future_scope_tool.py
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class FutureScopeInput(BaseModel):
    trend_summary: str = Field(..., description="Text summary of innovation trends from patent analysis")

class FutureScopeTool(BaseTool):
    name: str = "Patent Trend Analyzer & Future Scope Generator" 
    description:str = "Analyzes a list of patents and detects innovation trends, tech shifts, and dominant themes . Generates strategic insights and future business opportunities based on technology trends"
    args_schema: type[BaseModel] = FutureScopeInput 

    def _run(self, trend_summary: str) -> str:
        try:
            if "solid-state" in trend_summary.lower():
                return ("Solid-state batteries are likely to become mainstream within the next 3-5 years, "
                        "offering safer, faster-charging electric vehicles and consumer electronics.")

            if "nanotech" in trend_summary.lower():
                return ("Nanotechnology-driven energy storage may enable smaller, more powerful devices, "
                        "ideal for wearables, IoT, and aerospace.")
            print("###################################### future scope tool ######################################")
            print(f"Search results for query: {trend_summary}")
            print("########################################### END ###########################################")
          
            return trend_summary.lower()
        except Exception as e:
            return f"Error generating future scope: {str(e)}"
