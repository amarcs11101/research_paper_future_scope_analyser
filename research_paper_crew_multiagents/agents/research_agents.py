
from crewai import Agent 
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_groq import ChatGroq 
from langchain_openai import ChatOpenAI 
from langchain_google_genai import ChatGoogleGenerativeAI
from euriai import EuriaiClient
from tools.future_scope_tool import FutureScopeTool
from tools.search_tools import SearchTools 
import os
from dotenv import load_dotenv
load_dotenv()
class ResearchPaperAgents():
    def __init__(self, llm: BaseChatModel = None):
        if llm is None:
            #self.llm = LLM(model="groq/deepseek-r1-distill-llama-70b")
            #self.llm = ChatGroq(model=os.getenv("CHAT_GROQ_MODEL_NAME"),chatgroq_api_key=os.getenv("OPENAI_API_KEY"))
            self.llm = ChatOpenAI(model= os.getenv("OPEN_AI_MODEL"), openai_api_key=os.getenv("OPENAI_API_KEY"))
            #self.llm = ChatGoogleGenerativeAI(model= os.getenv("GEMINI_MODEL_NAME"), google_api_key= os.getenv("GEMINI_API_KEY"))
        else:
            self.llm = llm

        # Initialize tools once
        self.search_tool = SearchTools() 
        self.future_scope_tool = FutureScopeTool()
        #self.patent_research_expert_tool = PatentResearchTool()

    def patent_research_expert(self):
        return Agent(
            role="AI Patent Research Expert",
            goal="Search recent (last 3 years) patents and extract metadata including title, abstract, and filing date for a given topic",
            backstory="A research-savvy AI with deep skills in finding and understanding patents from public databases",        
            tools=[self.search_tool],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )
 

    def future_scope_analyst(self):
        return Agent(
            role="Technology Trend Analyst & technical Report Generator",
            goal="Analyze patent data to discover innovation patterns and predict future technologies and trends . Generate a final technical report combining findings and predictions for business and product stakeholders",
            backstory="An expert at understanding technology progression by analyzing patent filings and R&D signals . Experienced in crafting clear, insightful summaries for C-level decision makers",        
            tools=[self.search_tool, self.future_scope_tool],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

 
