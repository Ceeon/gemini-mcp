"""
Gemini MCP - MCP server for Gemini AI image processing
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .gemini_api import process_image_async, GeminiImageProcessor
from .mcp_server import mcp

__all__ = [
    "process_image_async",
    "GeminiImageProcessor",
    "mcp",
]