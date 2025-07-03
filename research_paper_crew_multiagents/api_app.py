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
from faiss_db_search.similarity_search import search_vector_db,save
from langchain_openai import ChatOpenAI 
from euriai import EuriaiClient
from langchain_google_genai import ChatGoogleGenerativeAI
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
    data: Optional[str] = None
    error: Optional[str] = None

class Settings:
    def __init__(self):
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.SERPER_API_KEY = os.getenv("SERPER_API_KEY")
        self.BROWSERLESS_API_KEY = os.getenv("BROWSERLESS_API_KEY"),
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
 

class ResearchCrew:
    def __init__(self, topic):
        self.topic = topic 
        #self.llm = ChatGroq(model=os.getenv("CHAT_GROQ_MODEL_NAME"),groq_api_key=os.getenv("GROQ_API_KEY"))
        #self.llm = ChatGoogleGenerativeAI(model= os.getenv("GEMINI_MODEL_NAME"), google_api_key= os.getenv("GEMINI_API_KEY"))
        self.llm = ChatOpenAI(model= os.getenv("OPEN_AI_MODEL"), openai_api_key=os.getenv("OPENAI_API_KEY"))
    def run(self):
        try:
            agents = ResearchPaperAgents(llm=self.llm)
            tasks = ResearchTasks()

            patent_research_expert_agent = agents.patent_research_expert() 
            future_scope_analyst_agent = agents.future_scope_analyst()

            identify_task = tasks.identify_task(
                patent_research_expert_agent,
                self.topic
            ) 

            plan_task = tasks.plan_task(
                future_scope_analyst_agent,
                topic=self.topic
            )

            crew = Crew(
                agents=[
                    patent_research_expert_agent, future_scope_analyst_agent
                ],
                tasks=[ identify_task, 
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
    research_request: ResearchPaperRequest
):      
       print("### Searching in the vector db first ###")
       vector_result=search_vector_db(research_request.research_on)
       print(f"### Searching completed in the vector db & data is ### {vector_result}")
       all_contents = [doc.page_content for doc in vector_result if hasattr(doc, "page_content")]
       if vector_result and len(vector_result)>0: 
            return ResearchResponse(
                    status="success",
                    message="Future scope based on research generated successfully from cache.",
                    data="\n\n".join(all_contents) 
                )
       else:
            print("## Calling the agents and tools for getting the research result as vector db doesn't contain the data ###")
            try:
                research_crew = ResearchCrew(
                    research_request.research_on
                )
                
                research_result = research_crew.run()
                
                # Ensure itinerary is a string
                if not isinstance(research_result, str):
                    research_result = str(research_result)
                # Saving the new record in vector db 
                save(query=research_request.research_on,result=research_result)
                # End     
                return ResearchResponse(
                    status="success",
                    message="Future scope based on research generated successfully",
                    data=research_result
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
