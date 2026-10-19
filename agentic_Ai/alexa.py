
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import subprocess
import webbrowser
import platform
import os
import psutil
import pyautogui

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Desktop Voice Assistant</title>
<style>
body {
    margin: 0;
    padding: 30px;
    text-align: center;
    font-family: Arial;
    background: #08152e;
    color: white;
}
main {
    max-width: 650px;
    margin: 30px auto;
    padding: 25px;
    border-radius: 20px;
    background: #132b49;
}
h1 { color: #42dcff; }
#orb {
    margin: 25px auto;
    width: 130px;
    height: 130px;
    border-radius: 50%;
    background: radial-gradient(circle, #b5faff, #0284c7, #172554);
    box-shadow: 0 0 35px #00cfff;
    display: grid;
    place-items: center;
    font-size: 48px;
}
#chat {
    text-align: left;
    min-height: 100px;
    padding: 15px;
    background: #071b32;
    border-radius: 12px;
    overflow-wrap: anywhere;
}
input {
    width: 60%;
    padding: 12px;
    border-radius: 8px;
    border: 0;
}
button {
    padding: 12px;
    margin: 5px;
    border: 0;
    border-radius: 8px;
    background: #38dff5;
    cursor: pointer;
}
</style>
</head>
<body>
<main>
<h1>My Desktop Assistant</h1>
<p>Control supported desktop functions with your voice</p>
<div id="orb">🤖</div>
<p id="status">Ready</p>
<div id="chat">Assistant: Hello! What can I do for you?</div>
<br>
<button onclick="listen()">🎙️ Speak</button>
<br><br>
<input id="msg" placeholder="Enter a command"
onkeydown="if(event.key==='Enter') send()">
<button onclick="send()">Send</button>
<p>Try: open Chrome, open Notepad, tell me the time,
show CPU usage, open Google.</p>
</main>

<script>
const chat = document.getElementById("chat");

function add(who, text) {
    const p = document.createElement("p");
    p.textContent = who + ": " + text;
    chat.appendChild(p);
}

function speak(text) {
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = "en-IN";
    speechSynthesis.speak(u);
}

async function send(text) {
    const input = document.getElementById("msg");
    text = text || input.value.trim();
    if (!text) return;
    input.value = "";
    add("You", text);
    document.getElementById("status").textContent = "Working...";

    try {
        const r = await fetch("/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: text})
        });
        const d = await r.json();
        add("Assistant", d.reply);
        speak(d.reply);
        document.getElementById("status").textContent = "Ready";
    } catch (e) {
        add("Assistant", "Could not connect to the server.");
    }
}

function listen() {
    const SR = window.SpeechRecognition ||
               window.webkitSpeechRecognition;
    if (!SR) {
        alert("Use Chrome and allow microphone access.");
        return;
    }
    const r = new SR();
    r.lang = "en-IN";
    r.onstart = () =>
        document.getElementById("status").textContent = "Listening...";
    r.onresult = e => send(e.results[0][0].transcript);
    r.onerror = () =>
        document.getElementById("status").textContent = "Microphone error";
    r.start();
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    msg = data.get("message", "").lower().strip()
    reply = "Sorry, I don't know that command yet."

    if not msg:
        reply = "Please say a command."

    elif "time" in msg:
        reply = datetime.now().strftime("The time is %I:%M %p")

    elif "date" in msg:
        reply = datetime.now().strftime("Today is %d %B %Y")

    elif "cpu" in msg:
        reply = f"CPU usage is {psutil.cpu_percent(interval=0.5)} percent."

    elif "memory" in msg or "ram" in msg:
        reply = f"RAM usage is {psutil.virtual_memory().percent} percent."

    elif "open google" in msg:
        webbrowser.open("https://www.google.com")
        reply = "Opening Google."

    elif "open youtube" in msg:
        webbrowser.open("https://www.youtube.com")
        reply = "Opening YouTube."

    elif "open github" in msg:
        webbrowser.open("https://github.com")
        reply = "Opening GitHub."

    elif "open notepad" in msg:
        if platform.system() == "Windows":
            subprocess.Popen(["notepad.exe"])
            reply = "Opening Notepad."
        else:
            reply = "Notepad command is for Windows only."

    elif "open calculator" in msg:
        if platform.system() == "Windows":
            subprocess.Popen(["calc.exe"])
            reply = "Opening Calculator."
        else:
            reply = "Calculator command is for Windows only."

    elif "open chrome" in msg:
        if platform.system() == "Windows":
            paths = [
                os.path.join(os.environ.get("PROGRAMFILES", ""),
                             "Google", "Chrome", "Application",
                             "chrome.exe"),
                os.path.join(os.environ.get("PROGRAMFILES(X86)", ""),
                             "Google", "Chrome", "Application",
                             "chrome.exe"),
                os.path.join(os.environ.get("LOCALAPPDATA", ""),
                             "Google", "Chrome", "Application",
                             "chrome.exe")
            ]
            chrome = next((p for p in paths if os.path.isfile(p)), None)
            if chrome:
                subprocess.Popen([chrome])
                reply = "Opening Chrome."
            else:
                reply = "Chrome was not found in the usual locations."
        else:
            reply = "Chrome launcher is configured for Windows."

    elif "who are you" in msg:
        reply = "I am your personal desktop voice assistant."

    elif "hello" in msg or msg == "hi":
        reply = "Hello! How can I help you?"

    elif "stop speaking" in msg:
        reply = "Okay."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=False)
