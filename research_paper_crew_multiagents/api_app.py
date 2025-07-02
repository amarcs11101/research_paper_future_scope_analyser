from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from crewai import Crew
from langchain_groq import ChatGroq
from agents.research_agents import ResearchPaperAgents
from agents.research_tasks import ResearchTasks
import os
from dotenv import load_dotenv
from functools import lru_cache

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Future Scope API",
    description="AI-powered future scope API using CrewAI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchPaperRequest(BaseModel): 
    research_on: str = Field(..., 
       description="A specific research topic, technology, or area of innovation for which academic papers or patents should be analyzed",
        examples=["Recent advancements in lithium-ion battery technology", 
                  "AI applications in cancer diagnosis", 
                  "Trends in quantum computing hardware", 
                  "Sustainable packaging materials in e-commerce"]
    )

class ResearchResponse(BaseModel):
    status: str
    message: str
    itinerary: Optional[str] = None
    error: Optional[str] = None

class Settings:
    def __init__(self):
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.SERPER_API_KEY = os.getenv("SERPER_API_KEY")
        self.BROWSERLESS_API_KEY = os.getenv("BROWSERLESS_API_KEY")

@lru_cache()
def get_settings():
    return Settings()

def validate_api_keys(settings: Settings = Depends(get_settings)):
    required_keys = {
        'GEMINI_API_KEY': settings.GEMINI_API_KEY,
        'SERPER_API_KEY': settings.SERPER_API_KEY,
        'BROWSERLESS_API_KEY': settings.BROWSERLESS_API_KEY
    }
    
    missing_keys = [key for key, value in required_keys.items() if not value]
    if missing_keys:
        raise HTTPException(
            status_code=500,
            detail=f"Missing required API keys: {', '.join(missing_keys)}"
        )
    return settings

class ResearchCrew:
    def __init__(self, topic):
        self.topic = topic 
        self.llm = ChatGroq(model="gemini/gemini-2.0-flash")

    def run(self):
        try:
            agents = ResearchPaperAgents(llm=self.llm)
            tasks = ResearchTasks()

            patent_research_expert_agent = agents.patent_research_expert()
            trend_analyst_agent = agents.trend_analyst()
            future_scope_analyst_agent = agents.future_scope_analyst()

            identify_task = tasks.identify_task(
                patent_research_expert_agent,
                self.topic
            )

            gather_task = tasks.gather_task(
                trend_analyst_agent, 
            )

            plan_task = tasks.plan_task(
                future_scope_analyst_agent,
                topic=self.topic
            )

            crew = Crew(
                agents=[
                    patent_research_expert_agent, trend_analyst_agent, future_scope_analyst_agent
                ],
                tasks=[ identify_task,
                        gather_task,
                       plan_task],
                verbose=True
            )

            result = crew.kickoff() 
            return result.raw if hasattr(result, 'raw') else str(result)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

@app.get("/")
async def root():
    return {
        "message": "Welcome to future research API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

@app.post("/api/v1/research", response_model=ResearchResponse)
async def research_paper_future_scope_analyst(
    research_request: ResearchPaperRequest,
    settings: Settings = Depends(validate_api_keys)
): 

    try:
        research_crew = ResearchCrew(
            research_request.research_on
        )
        
        itinerary = research_crew.run()
        
        # Ensure itinerary is a string
        if not isinstance(itinerary, str):
            itinerary = str(itinerary)
            
        return ResearchResponse(
            status="success",
            message="Future scope based on research generated successfully",
            itinerary=itinerary
        )
    
    except Exception as e:
        print(e)
        return ResearchResponse(
            status="error",
            message="Failed to generate future scope report",
            error=str(e)
        )

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
