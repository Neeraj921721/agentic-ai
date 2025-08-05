# Agentic AI

A sophisticated AI agent framework built with LangChain that supports multiple LLM providers (Google, OpenAI, Anthropic) and extensible tools. The agent can understand user queries, decide when to use tools, and provide natural responses.

## Features

- 🤖 Multi-provider LLM support (Google Gemini, OpenAI GPT, Anthropic Claude)
- 🛠️ Extensible tool system
- 💬 Conversational memory
- 🔄 Automatic tool routing
- 📅 Built-in datetime tool
- ⚡ Provider-agnostic architecture

## Project Structure

```
agentic-ai/
│
├── agents/              # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py   # Abstract base agent class
│   └── gemini_agent.py # Main agent implementation
│
├── tools/              # Tool implementations
│   ├── __init__.py
│   ├── datetime_tool.py
│   └── tool_example.py
│
├── chains/            # LangChain chains
│   ├── __init__.py
│   └── chain_example.py
│
├── utils/            # Utility functions
│   ├── __init__.py
│   └── helpers.py
│
├── main.py          # Entry point
├── config.py        # Configuration
└── requirements.txt # Dependencies
```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Neeraj921721/agentic-ai.git
   cd agentic-ai
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your API keys:
   ```env
   GOOGLE_API_KEY=your_google_api_key
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   LLM_PROVIDER=google  # or 'openai' or 'anthropic'
   LLM_MODEL=gemini-2.5-flash  # or other model names
   ```

## Usage

1. Run the main script:
   ```bash
   python main.py
   ```

2. Start chatting with the agent! Example interactions:
   ```
   You: What time is it now?
   Agent: Let me check the current time for you...
   Current time is 14:30:45 on Friday, August 5, 2025.

   You: Tell me a joke
   Agent: Why don't programmers like nature? It has too many bugs!
   ```

## Extending with New Tools

1. Create a new tool in the `tools` directory:
   ```python
   from langchain.tools import BaseTool

   class MyNewTool(BaseTool):
       name: str = "my_tool"
       description: str = "Description of what your tool does"

       def _run(self, query: str = "") -> str:
           # Implement your tool logic here
           return "Tool result"
   ```

2. Add the tool to the agent in `agents/gemini_agent.py`:
   ```python
   def _initialize_tools(self) -> List[BaseTool]:
       return [datetime_tool, my_new_tool]
   ```

## Configuration

The project uses a configuration system in `config.py` that supports:
- Multiple LLM providers
- Model selection
- Environment-based configuration
- Easy extension for new providers

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
