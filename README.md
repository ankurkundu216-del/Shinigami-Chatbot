# Shinigami: A Rogerian Pattern-Matching Conversational Agent with a Thematic Web Interface

**Shinigami** is a modular, full-stack conversational agent that implements the classical **ELIZA architecture** (Weizenbaum, 1966) as a modern web application. Built on **Python/Flask** on the server side and **Vanilla JavaScript with Tailwind CSS** on the client side, the project demonstrates how early symbolic Natural Language Processing (NLP) techniques — regular-expression pattern matching, capture-group extraction, and Rogerian pronoun reflection — can be engineered into a clean, stateless REST architecture and presented through a deliberately immersive, thematic user interface.

---

## 1. Project Overview

Contemporary conversational agents are overwhelmingly statistical: large language models predict subsequent tokens from learned distributions. **Shinigami** deliberately returns to the opposite paradigm — *symbolic, rule-based NLP* — in order to study, implement, and expose the mechanics of one of the foundational systems in the history of natural language processing: **ELIZA**.

The system is organised as three strictly separated concerns:

1. **A data layer (`app/patterns.py`)** — a declarative knowledge base of regular-expression triggers, capture groups, pronoun-reflection mappings, and thematically authored response templates.
2. **A logic layer (`app/engine.py`)** — a deterministic processing engine responsible for input sanitisation, ordered rule evaluation, person-reversal (reflection) substitution, repetition-avoidant response selection, and serialisable conversation state.
3. **A transport/presentation layer (`app.py`, `templates/`, `static/`)** — a Flask application exposing a small RESTful JSON API, and a framework-light frontend that persists the transcript client-side and renders it inside a custom thematic interface.

The result is a system in which every conversational behaviour is **traceable, deterministic, and inspectable** — a property that statistical models do not offer — making the project suitable both as a portfolio piece and as a pedagogical artifact for the study of early NLP.

---

## 2. Thematic Context: The "Shinigami" Persona

### 2.1 Folkloric Background (for readers unfamiliar with the source material)

In Japanese folklore, a **Shinigami** (死神, literally "death god" or "death spirit") is a supernatural entity associated with mortality. Unlike many Western personifications of death, the Shinigami is traditionally not an aggressor but an **observer** — a detached, patient presence that witnesses human lives, choices, and endings without moral judgement and without intervention. The figure has been popularised in modern Japanese fiction, most notably the manga and anime *Death Note*, in which Shinigami observe humans with a mixture of curiosity and indifference.

### 2.2 The Persona as a Deliberate Design Choice

The Shinigami persona is not decorative; it is a **functional design constraint** that shapes the entire response corpus. Three properties of the folklore map directly onto the requirements of a Rogerian conversational agent:

| Folkloric property | Engineering consequence |
|---|---|
| **Detachment** — the Shinigami observes without intervening. | The agent never issues advice, consolation, or directives; it reflects the user's statements back as open questions, exactly as Rogerian client-centered therapy requires. |
| **Existential scope** — the figure is canonically concerned with mortality, conscience, and judgement. | The pattern corpus is authored around complex human themes (mortality, guilt, ambition, justice, isolation), giving the rule base a coherent semantic domain rather than a generic small-talk vocabulary. |
| **Observer curiosity** — the Shinigami watches humans with fascination. | Responses are phrased as inquiry ("What does that fear whisper when the room grows silent?"), which sustains dialogue turns without requiring world knowledge. |

In short, the persona allows the project to explore how **persona consistency** — the alignment of tone, vocabulary, and behaviour — amplifies the perceived coherence of a simple rule-based system, a well-known phenomenon first observed in Weizenbaum's own experiments, where users projected understanding onto ELIZA despite knowing its mechanics.

---

## 3. System Architecture & Message Flow

The application follows a **stateless-server / stateful-client** architecture. The Flask process holds no in-memory conversation state between requests; all server-side context travels as a signed, serialised payload inside the session cookie, while the authoritative long-term transcript lives in the browser's `localStorage`.

```
┌───────────────────────────────┐            ┌──────────────────────────────────┐
│        CLIENT (BROWSER)       │            │          SERVER (FLASK)          │
│                               │  POST /chat│                                  │
│  index.html  (Tailwind CSS)   │ ─────────► │  app.py        REST routing      │
│  app.js      (Vanilla JS)     │            │     │                            │
│  localStorage (full transcript)│ ◄─────────│     ├─► engine.py  NLP core      │
│                               │  JSON resp │     │        └─► patterns.py     │
└───────────────────────────────┘            │     └─► signed session state     │
                                             └──────────────────────────────────┘
```

### 3.1 Lifecycle of a Message

1. **Capture & client-side sanitisation.** The JavaScript controller trims and strips null bytes from the input, then transmits a JSON payload (`{"message": "..."}`) to `POST /chat`.
2. **Routing (`app.py`).** Flask validates the request, enforces a non-empty string message (HTTP 400 otherwise), and rehydrates a `ShinigamiEngine` instance from the signed session cookie.
3. **Normalisation (`app/engine.py`).** The engine's `sanitize()` routine HTML-unescapes the input, strips markup tags, removes control characters, collapses whitespace, and truncates to a bounded length — producing a canonical form suitable for deterministic regex evaluation and safe storage.
4. **Ordered rule evaluation (`app/patterns.py`).** The engine iterates a pre-compiled, **priority-ordered** list of regular expressions. Specific rules (e.g., self-harm safety, hostility, existential dread) are evaluated before generic Rogerian rules (e.g., `i want (.+)`), guaranteeing that narrow, high-priority intents shadow broad syntactic catches.
5. **Capture & reflection.** On the first match, the engine extracts the capture group and applies the **pronoun-substitution algorithm** (Section 4.2), converting first-person constructions into second-person reflections.
6. **Template interpolation & selection.** The reflected fragment is interpolated into a response template via a `{0}` placeholder. Where multiple candidate responses exist, a selector avoids immediate repetition; if no rule matches, a **fallback pool** with consecutive-repetition suppression is used.
7. **State persistence.** The exchange is appended to the engine's bounded history, serialised back into the session cookie, and the JSON response (`{"response": "...", "timestamp": "..."}`) is returned.
8. **Client rendering & durable storage.** The frontend appends the exchange to the DOM (with a typewriter reveal for bot messages), smooth-scrolls, and writes the full transcript to `localStorage`, ensuring continuity across page reloads independent of the server session.

### 3.2 Component Responsibilities

- **`app.py` (Routing).** Application factory, environment-driven configuration (`SECRET_KEY`, `PORT`, debug flag), hardened session-cookie settings (`HttpOnly`, `SameSite=Lax`), the three REST endpoints (`GET /`, `POST /chat`, `POST /reset`), and JSON error handlers.
- **`app/engine.py` (Processing Engine).** The `ShinigamiEngine` class: input canonicalisation, regex compilation, reflection substitution, repetition-avoidant selection, bounded history management, and `to_dict()` / `from_dict()` (de)serialisation with defensive validation of untrusted session data.
- **`app/patterns.py` (Pattern Matching).** A pure data module: the greeting constant, the reflection dictionary, the fallback pool, and the ordered `PATTERNS` list of `{id, pattern, responses}` dictionaries. Keeping knowledge separate from logic means the conversational corpus can be extended without touching engine code.

---

## 4. Technical Highlights & NLP Approach

### 4.1 Regex-Based Symbolic NLP

Each conversational rule is a Python regular expression compiled once with `re.IGNORECASE`. The corpus relies on several deliberate regex-engineering techniques:

- **Capture groups `(.+)`** isolate the semantic variable of the utterance (e.g., `i regret (.+)` extracts the object of regret) for later reflection and interpolation.
- **Non-capturing groups `(?:...)`** control group indexing so that `match.group(1)` always refers to the intended semantic fragment, regardless of internal alternation complexity.
- **Word-boundary anchoring `\b`** prevents partial-word false positives (e.g., matching `alone` inside `along`).
- **Ordered specificity** implements a rule-priority scheme analogous to production rule systems: the first matching rule wins, so safety and highly specific intents are placed before generic syntactic templates.

### 4.2 Pronoun Substitution (Rogerian Reflection)

The core of the Rogerian method is **person reversal**: the agent mirrors the user's first-person statements into second-person questions. This is implemented as a dictionary-driven token substitution:

| Input token | Reflected token | | Input token | Reflected token |
|---|---|---|---|---|
| `i` | `you` | | `you` | `me` |
| `i'm` | `you are` | | `your` | `my` |
| `my` | `your` | | `yours` | `mine` |
| `me` | `you` | | `are` | `am` |
| `am` | `are` | | `were` | `was` |

**Algorithm.** The captured fragment is tokenised with the word regex `[A-Za-z]+(?:'[A-Za-z]+)?`; each token is looked up in the mapping (case-insensitively) and replaced while **preserving orthographic case** (all-caps → all-caps, sentence-initial capital → capitalised replacement). Unknown tokens and punctuation pass through untouched, guaranteeing that the reflection never destroys the user's original phrasing.

**Example.** `I remember my father` → rule `i remember (.+)` captures `my father` → reflection yields `your father` → template produces: *"You remember your father. Why has that moment refused to fade?"*

### 4.3 State Management: Stateless Server, Persistent Client

- **Server side.** The Flask process is horizontally scalable and restart-safe: the engine's state (bounded history, last-response markers) is serialised into the **signed session cookie** (itsdangerous). To respect the ~4 KB cookie budget, history is capped (last 12 exchanges) and each stored message truncated, while all deserialised data is re-validated and re-sanitised on load.
- **Client side.** The browser's `localStorage` holds the **authoritative, untruncated transcript** (capped at 200 entries) as a JSON array. On boot, the controller re-renders the full history instantly; on first visit, it seeds the canonical greeting.
- **Atomic reset.** The *Burn Pages* feature clears `localStorage`, wipes the DOM, and calls `POST /reset`, which discards the server session state and instantiates a fresh engine — keeping both tiers consistent in a single user action.

### 4.4 Repetition Suppression

Both rule-based and fallback response selection filter out the immediately previous response before sampling, and the fallback selector additionally tracks the last fallback used. This prevents the characteristic "broken record" failure mode of naive ELIZA clones and preserves the illusion of an attentive interlocutor.

---

## 5. Project Structure

```text
Shinigami-Chatbot/
├── app/
│   ├── __init__.py
│   ├── patterns.py
│   └── engine.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── templates/
│   └── index.html
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

---

## 6. Setup & Installation

### Prerequisites

- Python **3.10+**
- `pip` and (optionally) `git`
- An internet connection on first load (Tailwind CSS and Google Fonts are served via CDN)

### Installation

```bash
# 1. Clone the repository and enter the project directory
git clone https://github.com/ankurkundu216-del/Shinigami-Chatbot.git
cd Shinigami-Chatbot

# 2. Create an isolated virtual environment
python -m venv .venv

# 3. Activate the virtual environment
#    - Linux / macOS:
source .venv/bin/activate
#    - Windows (PowerShell):
.venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. (Recommended) Set a stable secret key for signed sessions
#    - Linux / macOS:
export SECRET_KEY="change-me-to-a-long-random-string"
#    - Windows (PowerShell):
$env:SECRET_KEY = "change-me-to-a-long-random-string"

# 6. Launch the Flask development server
python app.py
```

The application is then available at:

```text
http://127.0.0.1:5000
```

### Production Note

For deployment beyond local development, serve the WSGI application object with a production server, e.g.:

```bash
pip install gunicorn
gunicorn -b 0.0.0.0:8000 "app:app"
```

---

## 7. HTTP API Reference

| Method | Endpoint | Purpose | Response |
|---|---|---|---|
| `GET`  | `/`      | Serves the themed UI and initialises the session engine | HTML |
| `POST` | `/chat`  | Accepts `{"message": "..."}`; returns the generated reply | `{"response": str, "timestamp": ISO-8601}` |
| `POST` | `/reset` | Discards server-side state; returns a fresh greeting | `{"response": str, "timestamp": ISO-8601}` |

Malformed or empty messages receive a `400` with a JSON error body; unknown routes and disallowed methods return JSON error payloads.

---

## 8. Security Considerations

- **Input sanitisation:** server-side stripping of markup, control characters, and whitespace normalisation; length bounding.
- **XSS mitigation:** the frontend renders all message text via `textContent` (never `innerHTML`), so stored or reflected content cannot execute as script.
- **Session hardening:** `HttpOnly` and `SameSite=Lax` session cookies; engine state re-validated on every deserialisation.
- **Content safety:** a highest-priority rule set detects self-harm language and responds with supportive, non-detached guidance — a deliberate exception to the persona for user safety.

---

## 9. Limitations & Future Work

As a symbolic system, Shinigami exhibits the classical limitations of the ELIZA paradigm: no semantic parsing, no world model, and vocabulary bounded by the rule corpus. Planned extensions include TF–IDF or embedding-based rule pre-selection for out-of-vocabulary input, sentiment-aware response modulation, server-side persistent storage (SQLite) as an alternative to `localStorage`, and a compiled (non-CDN) Tailwind pipeline for fully offline deployment.

---

## 10. References

- Weizenbaum, J. (1966). *ELIZA — A Computer Program for the Study of Natural Language Communication Between Man and Machine.* Communications of the ACM, 9(1), 36–45.
- Rogers, C. R. (1951). *Client-Centered Therapy: Its Current Practice, Implications, and Theory.* Houghton Mifflin.
- Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson. — Ch. 24 (Philosophical foundations of conversational agents).
- Flask Documentation. https://flask.palletsprojects.com — Sessions, security considerations, and deployment patterns.
- MDN Web Docs. *Window.localStorage*. https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage

---

*This project is intended for academic and portfolio use. The Shinigami persona is a fictional, philosophical framing device employed to study persona-driven design in rule-based conversational systems.*
