import os

from .base_agent import BaseAgent
from dotenv import load_dotenv
from config import CONFIG
from tools.datetime_tool import datetime_tool


class AgenticModel(BaseAgent):
    """AgenticModel dynamically loads and manages the selected LLM provider and model."""
    def __init__(self, name: str = "AgenticModel"):
        super().__init__(name)
        load_dotenv()
        provider = CONFIG.get('provider', 'google').lower()
        model = CONFIG.get('model')
        self.llm = self._load_llm(provider, model)
        self.provider = provider
        self.model = model

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

    def run(self, input_text: str) -> str:
        """
        1. Let LLM try to answer first.
        2. If LLM can't answer (detected by broad fallback patterns), or if the query matches a tool's domain, use the tool.
        3. Return a user-friendly answer.
        """
        # Step 1: LLM tries to answer
        result = self.llm.invoke(input_text)
        llm_response = result.content if hasattr(result, 'content') else str(result)

        # Step 2: Check if the query matches a tool's domain (date/time)
        date_keywords = ["date", "time", "day", "today", "current time", "what day", "clock", "month", "year"]
        query_is_datetime = any(kw in input_text.lower() for kw in date_keywords)

        # Step 3: Check for broad fallback patterns in LLM response
        fallback_patterns = [
            "i don't have access to real-time information",
            "i'm unable to provide that information",
            "i don't know",
            "i'm not sure",
            "as an ai language model",
            "i cannot tell you the exact time",
            "i don't have access to current time",
            "i don't have access to current date",
            "i don't have access to a clock",
            "please check the clock",
            "please check your device",
            "i can't access real-time",
            "i can't access the current time",
            "i can't access the current date",
        ]
        llm_response_lower = llm_response.lower()
        fallback_triggered = any(pat in llm_response_lower for pat in fallback_patterns)

        # If the query is about date/time, always use the tool for accuracy
        if query_is_datetime:
            if hasattr(datetime_tool, 'run'):
                tool_result = datetime_tool.run()
            else:
                tool_result = datetime_tool(input_text)
            return f"{tool_result}"

        # If LLM fallback is triggered, try tool as a backup (for future extensibility)
        if fallback_triggered:
            if hasattr(datetime_tool, 'run'):
                tool_result = datetime_tool.run()
            else:
                tool_result = datetime_tool(input_text)
            return f"{tool_result}"

        # Otherwise, return LLM's answer
        return llm_response
