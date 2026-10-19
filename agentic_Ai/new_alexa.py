
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
from openai import OpenAI
import subprocess
import webbrowser
import platform
import os
import psutil

app = Flask(__name__)

# Read the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Alexa AI Desktop Assistant</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    padding: 25px 15px;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #06152e, #075985);
    color: white;
    text-align: center;
}
.container {
    max-width: 750px;
    margin: 20px auto;
    padding: 25px;
    background: #132b49;
    border-radius: 22px;
    box-shadow: 0 0 25px #00152c;
}
h1 { color: #42dcff; }
.orb {
    margin: 25px auto;
    width: 135px;
    height: 135px;
    border-radius: 50%;
    background: radial-gradient(circle, #b5faff, #0284c7, #172554);
    box-shadow: 0 0 35px #00cfff;
    display: grid;
    place-items: center;
    font-size: 50px;
}
#status { color: #7deaff; min-height: 20px; }
#chat {
    text-align: left;
    min-height: 140px;
    max-height: 350px;
    overflow-y: auto;
    padding: 15px;
    background: #071b32;
    border-radius: 12px;
    overflow-wrap: anywhere;
}
.user { color: white; }
.bot { color: #70eaff; line-height: 1.6; }
input {
    width: 72%;
    padding: 14px;
    border-radius: 9px;
    border: none;
    font-size: 15px;
}
button {
    padding: 14px 18px;
    margin: 5px;
    border: none;
    border-radius: 9px;
    background: #38dff5;
    color: #062038;
    font-weight: bold;
    cursor: pointer;
}
button:hover { background: #a5f3fc; }
small { color: #c9d8e8; }
@media(max-width: 480px) {
    input { width: 100%; }
}
</style>
</head>
<body>
<div class="container">
    <h1>Alexa AI Assistant</h1>
    <p>Your voice assistant with AI and web search</p>

    <div class="orb">🤖</div>
    <p id="status">Ready to help</p>

    <div id="chat">
        <p class="bot">Alexa: Hello! Ask me anything.</p>
    </div>

    <br>
    <button onclick="listen()">🎙️ Speak</button>
    <button onclick="stopVoice()">🔇 Stop speaking</button>
    <br><br>

    <input id="msg" placeholder="Alexa, search the web for Python"
           onkeydown="if(event.key==='Enter') send()">
    <button onclick="send()">Send</button>

    <p><small>
      Try: Open Notepad | Open Chrome | Search the web for AI news |
      Explain Python | Tell me the time | Show CPU usage
    </small></p>
</div>

<script>
const chat = document.getElementById("chat");

function addMessage(who, text) {
    const p = document.createElement("p");
    p.className = who === "You" ? "user" : "bot";

    const label = document.createElement("b");
    label.textContent = who + ": ";
    p.appendChild(label);

    // Display answers as text, not executable HTML.
    p.appendChild(document.createTextNode(text));
    chat.appendChild(p);
    chat.scrollTop = chat.scrollHeight;
}

function speak(text) {
    if (!("speechSynthesis" in window)) return;

    // Spoken responses can be lengthy; the stop button cancels them.
    speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-IN";
    utterance.rate = 0.95;
    speechSynthesis.speak(utterance);
}

async function send(text) {
    const input = document.getElementById("msg");
    text = text || input.value.trim();
    if (!text) return;

    input.value = "";
    addMessage("You", text);
    document.getElementById("status").textContent = "Thinking...";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: text})
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.reply || "Request failed");
        }

        addMessage("Alexa", data.reply);
        speak(data.reply);
        document.getElementById("status").textContent = "Ready";
    } catch (error) {
        addMessage("Alexa", error.message || "Could not connect to the server.");
        document.getElementById("status").textContent = "Error";
    }
}

function listen() {
    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Please use Chrome and allow microphone access.");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-IN";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
        document.getElementById("status").textContent = "Listening...";
    };

    recognition.onresult = (event) => {
        send(event.results[0][0].transcript);
    };

    recognition.onerror = () => {
        document.getElementById("status").textContent =
            "Microphone error. Check browser permissions.";
    };

    recognition.onend = () => {
        if (document.getElementById("status").textContent === "Listening...") {
            document.getElementById("status").textContent = "Ready";
        }
    };

    recognition.start();
}

function stopVoice() {
    speechSynthesis.cancel();
    document.getElementById("status").textContent = "Speech stopped";
}
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


def clean_command(text):
    """Remove wake words and common filler words."""
    words = text.lower().strip().split()

    while words and words[0] in ("alexa", "assistant"):
        words.pop(0)

    fillers = {"please", "my", "the", "a", "an"}
    return " ".join(word for word in words if word not in fillers)


def desktop_command(msg):
    """Return a response for supported local commands, or None."""
    system = platform.system()

    if msg in ("open notepad", "start notepad", "launch notepad"):
        if system == "Windows":
            subprocess.Popen(["notepad.exe"])
            return "Opening Notepad."
        return "Notepad command is configured for Windows."

    if msg in ("open calculator", "start calculator", "launch calculator"):
        if system == "Windows":
            subprocess.Popen(["calc.exe"])
            return "Opening Calculator."
        return "Calculator command is configured for Windows."

    if msg in ("open chrome", "start chrome", "launch chrome"):
        if system == "Windows":
            paths = [
                os.path.join(
                    os.environ.get("PROGRAMFILES", ""),
                    "Google", "Chrome", "Application", "chrome.exe"
                ),
                os.path.join(
                    os.environ.get("PROGRAMFILES(X86)", ""),
                    "Google", "Chrome", "Application", "chrome.exe"
                ),
                os.path.join(
                    os.environ.get("LOCALAPPDATA", ""),
                    "Google", "Chrome", "Application", "chrome.exe"
                )
            ]

            chrome = next((p for p in paths if os.path.isfile(p)), None)

            if chrome:
                subprocess.Popen([chrome])
                return "Opening Chrome."

        return "Chrome was not found in the usual locations."

    websites = {
        "open google": ("https://www.google.com", "Google"),
        "open youtube": ("https://www.youtube.com", "YouTube"),
        "open github": ("https://github.com", "GitHub"),
        "open gmail": ("https://mail.google.com", "Gmail")
    }

    for command, (url, name) in websites.items():
        if msg == command:
            webbrowser.open(url)
            return f"Opening {name}."

    if "time" in msg:
        return "The time is " + datetime.now().strftime("%I:%M %p")

    if "date" in msg or msg == "today":
        return "Today's date is " + datetime.now().strftime("%d %B %Y")

    if "cpu" in msg:
        return f"CPU usage is {psutil.cpu_percent(interval=0.5)} percent."

    if "ram" in msg or "memory usage" in msg:
        return f"RAM usage is {psutil.virtual_memory().percent} percent."

    if msg in ("who are you", "what is your name"):
        return "I am your personal AI voice assistant."

    if msg in ("stop speaking", "stop talking"):
        return "You can press the Stop Speaking button to stop my voice."

    return None


def ai_answer(question):
    """Use AI with web search available for suitable questions."""
    if client is None:
        return (
            "AI is not configured. Set the OPENAI_API_KEY environment "
            "variable in your terminal and restart the server."
        )

    response = client.responses.create(
        model="gpt-5-mini",
        tools=[{"type": "web_search"}],
        instructions=(
            "You are a helpful desktop voice assistant. "
            "Answer the user's actual question clearly in simple English. "
            "Use web search when current facts, recent events, or online "
            "research would help. Cite sources with URLs when available. "
            "Never claim to have performed a computer action unless a "
            "separate desktop command actually performed it. "
            "Keep answers reasonably concise for text-to-speech."
        ),
        input=question
    )

    answer = response.output_text.strip()
    return answer or "Sorry, I could not generate an answer."


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    original = data.get("message", "").strip()

    if not original:
        return jsonify({"reply": "Please ask me a question."}), 400

    msg = clean_command(original)

    try:
        # Handle safe local commands before asking AI.
        reply = desktop_command(msg)

        # All other questions go to AI; web search is available.
        if reply is None:
            reply = ai_answer(msg)

        return jsonify({"reply": reply})

    except Exception:
        app.logger.exception("Assistant request failed")
        return jsonify({
            "reply": (
                "I could not complete that request. Check your internet "
                "connection, API key, API account access, and terminal logs."
            )
        }), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
