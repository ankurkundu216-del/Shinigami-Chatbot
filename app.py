"""
Flask entry point for the Shinigami chatbot.

This application exposes:
- GET /       : serves the themed chat UI
- POST /chat  : accepts JSON messages and returns Shinigami responses
- POST /reset : clears backend session state and restarts the engine
"""

from __future__ import annotations

import os
import secrets
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request, session

from app.engine import ShinigamiEngine
from app.patterns import GREETING


def create_app() -> Flask:
    app = Flask(__name__)

    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        secret_key = secrets.token_hex(32)
        app.logger.warning(
            "SECRET_KEY is not set. Using an ephemeral key. "
            "Set SECRET_KEY in production for stable signed sessions."
        )

    app.secret_key = secret_key

    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    app.json.sort_keys = False

    def utc_now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @app.get("/")
    def index():
        if "engine_state" not in session:
            engine = ShinigamiEngine()
            session["engine_state"] = engine.to_dict()

        return render_template(
            "index.html",
            default_greeting=GREETING,
        )

    @app.post("/chat")
    def chat():
        payload = request.get_json(silent=True, force=True)

        if payload is None:
            payload = request.form.to_dict()

        raw_message = payload.get("message", "") if isinstance(payload, dict) else ""

        if not isinstance(raw_message, str) or not raw_message.strip():
            return jsonify({"error": "A non-empty message is required."}), 400

        message = ShinigamiEngine.sanitize(raw_message)
        if not message:
            return jsonify({"error": "Message contained no usable text."}), 400

        state = session.get("engine_state")
        engine = ShinigamiEngine.from_dict(state) if state else ShinigamiEngine()

        response_text = engine.respond(message)
        session["engine_state"] = engine.to_dict()

        return jsonify(
            {
                "response": response_text,
                "timestamp": utc_now(),
            }
        )

    @app.post("/reset")
    def reset():
        engine = ShinigamiEngine()
        session["engine_state"] = engine.to_dict()

        return jsonify(
            {
                "response": engine.greeting,
                "timestamp": utc_now(),
            }
        )

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({"error": "Endpoint not found."}), 404

    @app.errorhandler(405)
    def handle_405(error):
        return jsonify({"error": "Method not allowed."}), 405

    @app.errorhandler(500)
    def handle_500(error):
        app.logger.exception("Internal server error.")
        return jsonify({"error": "Internal server error."}), 500

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0").lower() in {"1", "true", "yes"}

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
    )