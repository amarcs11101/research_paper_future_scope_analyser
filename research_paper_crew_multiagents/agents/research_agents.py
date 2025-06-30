
from crewai import Agent 
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_groq import ChatGroq 
from tools.future_scope_tool import FutureScopeTool
from tools.search_tools import SearchTools
from tools.trend_analysis_tool import TrendAnalysisTool
from tools.patent_research_tool import PatentResearchTool

class ResearchPaperAgents():
    def __init__(self, llm: BaseChatModel = None):
        if llm is None:
            #self.llm = LLM(model="groq/deepseek-r1-distill-llama-70b")
            self.llm = ChatGroq(model="gemini/gemini-2.0-flash")
        else:
            self.llm = llm

        # Initialize tools once
        self.search_tool = SearchTools()
        self.trend_analysis_tool = TrendAnalysisTool()
        self.future_scope_tool = FutureScopeTool()
        self.patent_research_expert_tool = PatentResearchTool()

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

    def trend_analyst(self):
        return Agent(
            role="Technology Trend Analyst",
            goal="Analyze patent data to discover innovation patterns and predict future technologies and trends",
            backstory="An expert at understanding technology progression by analyzing patent filings and R&D signals",        
            tools=[self.search_tool, self.trend_analysis_tool],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def future_scope_analyst(self):
        return Agent(
            role="Technical Report Generator",
            goal="Generate a final technical report combining findings and predictions for business and product stakeholders",
            backstory="Experienced in crafting clear, insightful summaries for C-level decision makers",        
            tools=[self.search_tool, self.trend_analysis_tool, self.future_scope_tool],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

 
