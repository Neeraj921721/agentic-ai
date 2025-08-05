from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Abstract base class for AI agents."""
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, input_text: str):
        """Process user input and return agent response."""
        pass
