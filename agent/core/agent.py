from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from core.tools import github_tools
from services.llm_factory import llm_factory
from typing import Dict, Any

class AgentOrchestrator:
    """
    Manages the autonomous agent loop.
    """
    
    def __init__(self, provider: str = "openai", model: str = "gpt-4-turbo"):
        self.llm = llm_factory.get_model(provider, model)
        self.tools = github_tools
        
        # Define the ReAct prompt
        template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

        self.prompt = PromptTemplate.from_template(template)
        
        # Construct the ReAct agent
        self.agent = create_react_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent, 
            tools=self.tools, 
            verbose=True, 
            handle_parsing_errors=True,
            max_iterations=15
        )

    async def run_task(self, task: str) -> Dict[str, Any]:
        """
        Executes a task using the agent.
        """
        try:
            result = await self.agent_executor.ainvoke({"input": task})
            return {"status": "success", "output": result["output"]}
        except Exception as e:
            return {"status": "error", "error": str(e)}

# Global instance manager could go here
