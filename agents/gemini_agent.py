import os
from typing import List

from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.tools.base import BaseTool
from .base_agent import BaseAgent
from dotenv import load_dotenv
from config import CONFIG
from tools.datetime_tool import datetime_tool


class AgenticModel(BaseAgent):
    """AgenticModel dynamically loads and manages the selected LLM provider and model with tool support."""
    def __init__(self, name: str = "AgenticModel"):
        super().__init__(name)
        load_dotenv()
        provider = CONFIG.get('provider', 'google').lower()
        model = CONFIG.get('model')
        
        # Initialize LLM
        self.llm = self._load_llm(provider, model)
        self.provider = provider
        self.model = model
        
        # Initialize tools
        self.tools = self._initialize_tools()
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Initialize the agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            handle_parsing_errors=True
        )

    def _load_llm(self, provider, model):
        if provider == 'google':
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model=model,
                api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )
        elif provider == 'openai':
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=model or "gpt-3.5-turbo",
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )
        elif provider == 'anthropic':
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model=model or "claude-3-opus-20240229",
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _initialize_tools(self) -> List[BaseTool]:
        """Initialize and return list of available tools."""
        return [datetime_tool]

    def run(self, input_text: str) -> str:
        """
        Run the agent with the given input.
        The agent will automatically:
        1. Understand the user's request
        2. Decide if and which tools to use
        3. Use tools if needed
        4. Formulate a natural response
        """
        try:
            response = self.agent.run(input=input_text)
            return response
        except Exception as e:
            return f"I encountered an error: {str(e)}"
