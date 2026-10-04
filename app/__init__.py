"""
Shinigami application package.

This package contains the modular backend components for the Shinigami chatbot:
- patterns.py: regex rules, triggers, reflections, and response pools
- engine.py: core conversational engine with session-safe state handling
"""

__all__ = ["engine", "patterns"]