# Shinigami Chatbot

A production-grade, modular Python chatbot inspired by **Death Note**.  
Shinigami is built on classic **ELIZA-style Rogerian pattern matching**, but with a darker, philosophical Shinigami persona.

This project is designed as a strong university computer science portfolio piece, featuring:

- Modular Flask backend
- Regex-based conversational rules
- Pronoun reflection
- Session-safe conversational state
- Persistent frontend chat memory using `localStorage`
- Death Note-themed UI using Tailwind CSS and custom CSS
- Fully vanilla JavaScript frontend

---

## Project Structure

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