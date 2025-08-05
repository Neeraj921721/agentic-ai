"""Configuration for selecting LLM provider and model."""
import os

CONFIG = {
    # Supported providers: 'google', 'openai', 'anthropic'
    'provider': os.getenv('LLM_PROVIDER', 'google'),
    'model': os.getenv('LLM_MODEL', 'gemini-2.5-flash'),
    # Add more config as needed
}
