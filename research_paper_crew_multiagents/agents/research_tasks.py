from crewai import Task
from textwrap import dedent 
class ResearchTasks():
    def __validate_inputs(self, topic):
        if not topic:
            raise ValueError("Please enter research topic.")
        return True

    def identify_task(self, agent, topic):
        self.__validate_inputs(topic)
        return Task(description=dedent(f"""
            Search and extract metadata (title, abstract, publication date, and URLs) for recent (last 3 years) patents on the topic '{topic}'.
            {self.__tip_section()} 
          """),
            expected_output="A structured list of 5-6 recent patents with metadata (title, abstract, date, and source URL).",
            agent=agent)

    def gather_task(self, agent):
        return Task(description=dedent(f"""
            Analyze the extracted patent data to identify current innovation trends, emerging technologies, and active areas of research.
            {self.__tip_section()} 
          """),
            expected_output="A comprehensive trend analysis and technology forecast based on the patent data.",
            agent=agent)

    def plan_task(self, agent,topic):
        return Task(description=dedent(f"""
            Generate a professional report that summarizes recent patents, identified trends, and predicts upcoming innovations in the field of '{topic}'.
            # up each place, what make them special! {self.__tip_section()}
 
          """),
            expected_output="A well-structured final report suitable for business and R&D stakeholders.",
            agent=agent)

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $100 and grant you any wish you want!"
