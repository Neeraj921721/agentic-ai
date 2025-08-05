"""Tool for providing current date and time information, using LangChain's built-in tool if available."""
try:
    # Try to import the standard LangChain DateTime tool
    from langchain_community.tools import DateTimeTool
    datetime_tool = DateTimeTool()
    # Usage: datetime_tool.run() returns the current date and time as a string
except ImportError:
    # Fallback to custom implementation
    from datetime import datetime

    def get_current_datetime() -> str:
        now = datetime.now()
        return now.strftime("%A, %d %B %Y, %H:%M:%S")

    def datetime_tool(query: str = None) -> str:
        """Answer queries about the current date and time."""
        return f"Current date and time: {get_current_datetime()}"
