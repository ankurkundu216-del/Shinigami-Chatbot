(() => {
    "use strict";

    const STORAGE_KEY = "shinigami-chat-history-v1";
    const MAX_STORED_MESSAGES = 200;

    const body = document.body;
    const DEFAULT_GREETING =
        body.dataset.defaultGreeting ||
        "I am a Shinigami. What thoughts plague your human mind?";

    const chatWindow = document.getElementById("chat-window");
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-btn");
    const burnButton = document.getElementById("burn-btn");
    const typingIndicator = document.getElementById("typing-indicator");

    let history = [];
    let isBusy = false;

    const sanitizeText = (value) => {
        if (value === null || value === undefined) {
            return "";
        }
        return String(value).replace(/\u0000/g, "").trim();
    };

    const saveHistory = () => {
        try {
            const trimmed = history.slice(-MAX_STORED_MESSAGES);
            localStorage.setItem(STORAGE_KEY, JSON.stringify(trimmed));
        } catch (error) {
            console.warn("Unable to persist chat history to localStorage.", error);
        }
    };

    const formatTime = (timestamp) => {
        const date = timestamp ? new Date(timestamp) : new Date();
        if (Number.isNaN(date.getTime())) {
            return "";
        }

        return date.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
        });
    };

    const scrollToBottom = (smooth = true) => {
        chatWindow.scrollTo({
            top: chatWindow.scrollHeight,
            behavior: smooth ? "smooth" : "auto",
        });
    };

    const createMessageElement = (entry) => {
        const wrapper = document.createElement("div");
        wrapper.className = `message-row ${
            entry.role === "user" ? "flex justify-end" : "flex justify-start"
        }`;

        const bubble = document.createElement("div");
        bubble.className = `message ${
            entry.role === "user" ? "message-user" : "message-bot"
        } rounded-lg px-4 py-3`;

        const text = document.createElement("p");
        text.textContent = entry.text;

        bubble.appendChild(text);

        if (entry.timestamp) {
            const time = document.createElement("span");
            time.className = "timestamp";
            time.textContent = formatTime(entry.timestamp);
            bubble.appendChild(time);
        }

        wrapper.appendChild(bubble);
        return wrapper;
    };

    const appendMessage = (entry, options = {}) => {
        const shouldSave = options.save !== false;

        history.push(entry);

        if (shouldSave) {
            saveHistory();
        }

        chatWindow.appendChild(createMessageElement(entry));
        scrollToBottom();
    };

    const renderHistory = () => {
        chatWindow.innerHTML = "";

        const fragment = document.createDocumentFragment();
        history.forEach((entry) => {
            fragment.appendChild(createMessageElement(entry));
        });

        chatWindow.appendChild(fragment);
        scrollToBottom(false);
    };

    const showTyping = () => {
        typingIndicator.classList.remove("hidden");
    };

    const hideTyping = () => {
        typingIndicator.classList.add("hidden");
    };

    const setBusy = (busy) => {
        isBusy = busy;
        userInput.disabled = busy;
        sendButton.disabled = busy;
        burnButton.disabled = busy;

        if (!busy) {
            userInput.focus();
        }
    };

    const postJSON = async (url, payload) => {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
            credentials: "same-origin",
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(data.error || `Request failed with status ${response.status}`);
        }

        return data;
    };

    const sendMessage = async () => {
        const text = sanitizeText(userInput.value);

        if (!text || isBusy) {
            return;
        }

        appendMessage({
            role: "user",
            text,
            timestamp: new Date().toISOString(),
        });

        userInput.value = "";
        userInput.style.height = "auto";

        setBusy(true);
        showTyping();

        try {
            const data = await postJSON("/chat", { message: text });

            const responseText = sanitizeText(
                data.response || DEFAULT_GREETING
            );

            appendMessage({
                role: "bot",
                text: responseText,
                timestamp: data.timestamp || new Date().toISOString(),
            });
        } catch (error) {
            console.error(error);

            appendMessage({
                role: "bot",
                text: "The pages are silent. Refresh or burn the pages to summon me again.",
                timestamp: new Date().toISOString(),
            });
        } finally {
            hideTyping();
            setBusy(false);
        }
    };

    const resetChat = async () => {
        if (isBusy) {
            return;
        }

        setBusy(true);
        showTyping();

        try {
            localStorage.removeItem(STORAGE_KEY);
            history = [];
            chatWindow.innerHTML = "";

            const data = await postJSON("/reset", {});

            const responseText = sanitizeText(
                data.response || DEFAULT_GREETING
            );

            appendMessage({
                role: "bot",
                text: responseText,
                timestamp: data.timestamp || new Date().toISOString(),
            });
        } catch (error) {
            console.error(error);

            localStorage.removeItem(STORAGE_KEY);
            history = [];
            chatWindow.innerHTML = "";

            appendMessage({
                role: "bot",
                text: DEFAULT_GREETING,
                timestamp: new Date().toISOString(),
            });
        } finally {
            hideTyping();
            setBusy(false);
        }
    };

    const loadInitialHistory = () => {
        let stored = [];

        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (raw) {
                stored = JSON.parse(raw);
            }
        } catch (error) {
            console.warn("Stored chat history could not be parsed.", error);
            stored = [];
        }

        if (Array.isArray(stored) && stored.length > 0) {
            history = stored
                .filter(
                    (entry) =>
                        entry &&
                        typeof entry.text === "string" &&
                        ["user", "bot"].includes(entry.role)
                )
                .slice(-MAX_STORED_MESSAGES);

            if (history.length > 0) {
                renderHistory();
                return;
            }
        }

        history = [];
        appendMessage({
            role: "bot",
            text: DEFAULT_GREETING,
            timestamp: new Date().toISOString(),
        });
    };

    chatForm.addEventListener("submit", (event) => {
        event.preventDefault();
        sendMessage();
    });

    userInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });

    userInput.addEventListener("input", () => {
        userInput.style.height = "auto";
        userInput.style.height = `${Math.min(userInput.scrollHeight, 160)}px`;
    });

    burnButton.addEventListener("click", resetChat);

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", loadInitialHistory);
    } else {
        loadInitialHistory();
    }
})();