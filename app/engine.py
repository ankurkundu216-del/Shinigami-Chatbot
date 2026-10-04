"""
Core conversational engine for Shinigami.

This module implements the ShinigamiEngine class, which is responsible for:
- sanitizing user input
- matching input against themed regex patterns
- applying Rogerian reflection mappings
- maintaining short-term conversational history
- selecting responses while avoiding consecutive fallback repetition
"""

from __future__ import annotations

import html
import random
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .patterns import FALLBACK_RESPONSES, GREETING, PATTERNS, REFLECTIONS


class ShinigamiEngine:
    """
    A Death Note-themed ELIZA-style conversational engine.

    The engine is intentionally stateless across requests except for the
    serialized state stored in the Flask session. This makes it safe for
    horizontal scaling and avoids server-side in-memory session storage.
    """

    DEFAULT_GREETING = GREETING

    _TAG_RE = re.compile(r"<[^>]*>")
    _CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
    _WHITESPACE_RE = re.compile(r"\s+")
    _WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")

    _MAX_INPUT_LENGTH = 2000
    _MAX_SERIALIZED_TEXT_LENGTH = 500

    def __init__(self, max_history: int = 12) -> None:
        self.max_history = max_history
        self.history: List[Dict[str, str]] = []
        self.last_response: Optional[str] = None
        self.last_fallback: Optional[str] = None

        self._compiled_patterns: List[tuple[re.Pattern[str], List[str]]] = []
        for rule in PATTERNS:
            try:
                compiled = re.compile(rule["pattern"], re.IGNORECASE)
                responses = rule.get("responses", [])
                if responses:
                    self._compiled_patterns.append((compiled, responses))
            except KeyError:
                continue

    @property
    def greeting(self) -> str:
        return self.DEFAULT_GREETING

    @classmethod
    def sanitize(cls, raw: Any) -> str:
        """
        Sanitize raw user input before pattern matching.

        This removes HTML tags, control characters, and excess whitespace.
        It also decodes common HTML entities once before stripping tags so
        encoded markup does not survive as executable-looking input.
        """
        if raw is None:
            return ""

        text = str(raw)
        text = html.unescape(text)
        text = cls._TAG_RE.sub(" ", text)
        text = cls._CONTROL_CHARS_RE.sub("", text)
        text = cls._WHITESPACE_RE.sub(" ", text).strip()
        return text[: cls._MAX_INPUT_LENGTH]

    def respond(self, user_input: Any) -> str:
        """
        Generate the next Shinigami response for a user message.

        The user message is sanitized, added to history, matched against
        compiled patterns, and then a response is chosen. If no pattern
        matches, a fallback response is selected without repeating the
        immediately previous fallback.
        """
        clean_input = self.sanitize(user_input)

        if not clean_input:
            clean_input = "..."

        self._add_to_history("user", clean_input)

        response = self._match_pattern(clean_input)
        if response is None:
            response = self._fallback()

        self.last_response = response
        self._add_to_history("bot", response)
        return response

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the engine state for storage in Flask session.

        History text is truncated for session-cookie safety, while the
        frontend localStorage can keep a longer transcript.
        """
        serialized_history = []
        for entry in self.history[-self.max_history :]:
            serialized_history.append(
                {
                    "role": entry.get("role"),
                    "text": str(entry.get("text", ""))[: self._MAX_SERIALIZED_TEXT_LENGTH],
                    "timestamp": entry.get("timestamp"),
                }
            )

        return {
            "history": serialized_history,
            "last_response": self.last_response,
            "last_fallback": self.last_fallback,
            "max_history": self.max_history,
        }

    @classmethod
    def from_dict(cls, state: Optional[Dict[str, Any]]) -> "ShinigamiEngine":
        """
        Recreate an engine instance from serialized session state.

        Invalid or malformed history entries are discarded defensively.
        """
        engine = cls()

        if not isinstance(state, dict):
            return engine

        try:
            max_history = int(state.get("max_history", engine.max_history))
        except (TypeError, ValueError):
            max_history = engine.max_history

        engine.max_history = max(1, min(max_history, 20))

        raw_history = state.get("history", [])
        if isinstance(raw_history, list):
            for item in raw_history:
                if not isinstance(item, dict):
                    continue

                role = item.get("role")
                text = item.get("text")
                timestamp = item.get("timestamp")

                if role not in ("user", "bot"):
                    continue

                if not isinstance(text, str):
                    continue

                clean_text = cls.sanitize(text)
                if not clean_text:
                    continue

                engine.history.append(
                    {
                        "role": role,
                        "text": clean_text,
                        "timestamp": timestamp,
                    }
                )

        engine.history = engine.history[-engine.max_history :]

        last_response = state.get("last_response")
        last_fallback = state.get("last_fallback")

        engine.last_response = last_response if isinstance(last_response, str) else None
        engine.last_fallback = last_fallback if isinstance(last_fallback, str) else None

        return engine

    def _add_to_history(self, role: str, text: str) -> None:
        entry = {
            "role": role,
            "text": text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.history.append(entry)

        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history :]

    def _match_pattern(self, text: str) -> Optional[str]:
        """
        Attempt to match input against ordered regex rules.

        If a rule captures text, the captured fragment is reflected before
        being inserted into the response template.
        """
        for pattern, responses in self._compiled_patterns:
            match = pattern.search(text)
            if not match:
                continue

            captured = match.group(1) if match.groups() else ""
            candidates: List[str] = []

            for template in responses:
                if not isinstance(template, str):
                    continue

                if "{0}" in template:
                    if not captured.strip():
                        continue
                    reflected = self._reflect(captured)
                    candidates.append(template.replace("{0}", reflected))
                else:
                    candidates.append(template)

            if candidates:
                return self._choose(candidates)

        return None

    def _fallback(self) -> str:
        """
        Choose a fallback response without repeating the previous fallback.

        The pool is filtered to avoid both the last fallback and the last
        response wherever possible.
        """
        excluded = {self.last_response, self.last_fallback}
        candidates = [response for response in FALLBACK_RESPONSES if response not in excluded]

        if not candidates:
            candidates = [
                response for response in FALLBACK_RESPONSES if response != self.last_fallback
            ]

        if not candidates:
            candidates = list(FALLBACK_RESPONSES)

        response = random.choice(candidates)
        self.last_fallback = response
        return response

    def _choose(self, options: List[str]) -> str:
        """
        Choose a response while avoiding immediate repetition of the last
        generated response when possible.
        """
        if not options:
            return self._fallback()

        if len(options) == 1:
            return options[0]

        filtered = [option for option in options if option != self.last_response]
        if not filtered:
            filtered = options

        return random.choice(filtered)

    def _reflect(self, text: str) -> str:
        """
        Apply pronoun and verb reflection to a captured phrase.

        This preserves the original casing style as closely as possible.
        """

        def replace_word(match: re.Match[str]) -> str:
            word = match.group(0)
            replacement = REFLECTIONS.get(word.lower())

            if replacement is None:
                return word

            if word.isupper():
                return replacement.upper()

            if word[0].isupper():
                return replacement.capitalize()

            return replacement

        return self._WORD_RE.sub(replace_word, text).strip()