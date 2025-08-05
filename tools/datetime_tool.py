"""Tool for providing current date and time information."""
from datetime import datetime
from langchain.tools import BaseTool

class DateTimeTool(BaseTool):
    name: str = "datetime_tool"
    description: str = "Use this tool to get the current date and time. Useful for answering questions about current time, date, day of the week, etc."

    def _run(self, query: str = "") -> str:
        """Get the current date and time."""
        now = datetime.now()
        return now.strftime("%A, %d %B %Y, %H:%M:%S")

# Create an instance of the tool
datetime_tool = DateTimeTool()
