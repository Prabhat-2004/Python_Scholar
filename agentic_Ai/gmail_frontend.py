
import base64
from pathlib import Path
from flask import Flask, jsonify, request, render_template_string

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
TOKEN_FILE = BASE_DIR / "token.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_service():
    credentials_file = BASE_DIR / "credentials.json"

    if not credentials_file.exists():
        credentials_file = BASE_DIR / "credentials.json.json"

    if not credentials_file.exists():
        raise FileNotFoundError(
            "Put credentials.json beside gmail.py"
        )

    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(
            str(TOKEN_FILE), SCOPES
        )

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(credentials_file), SCOPES
        )
        creds = flow.run_local_server(port=0)

    TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    return build("gmail", "v1", credentials=creds)


def get_header(headers, name):
    for item in headers:
        if item.get("name", "").lower() == name.lower():
            return item.get("value", "")
    return ""


def get_body(payload):
    parts = []

    def walk(part):
        mime = part.get("mimeType", "")
        data = part.get("body", {}).get("data")

        if mime == "text/plain" and data:
            try:
                data += "=" * (-len(data) % 4)
                text = base64.urlsafe_b64decode(data).decode(
                    "utf-8", errors="replace"
                )
                parts.append(text)
            except Exception:
                pass

        for child in part.get("parts", []):
            walk(child)

    walk(payload)
    return "\n".join(parts).strip()


def fetch_emails(query="in:inbox", limit=10):
    service = get_gmail_service()

    result = service.users().messages().list(
        userId="me", q=query, maxResults=limit
    ).execute()

    emails = []

    for index, message in enumerate(
        result.get("messages", []), start=1
    ):
        item = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full"
        ).execute()

        payload = item.get("payload", {})
        headers = payload.get("headers", [])

        emails.append({
            "number": index,
            "id": item["id"],
            "sender": get_header(headers, "From"),
            "subject": get_header(headers, "Subject") or "(No subject)",
            "date": get_header(headers, "Date"),
            "snippet": item.get("snippet", ""),
            "body": get_body(payload)
        })

    return emails


def process_command(command):
    command = command.lower().strip()
    command = command.replace(".", "").replace(",", "")

    # Allow common variations recognized by voice input.
    if any(word in command for word in [
        "help", "what can you do", "commands"
    ]):
        return {
            "reply": (
                "Say read my emails, show inbox, "
                "search subject meeting, or read email one."
            )
        }

    if any(phrase in command for phrase in [
        "read my emails", "read emails", "latest mail",
        "latest emails", "show my inbox", "show inbox",
        "check my mail", "check my emails", "open gmail"
    ]):
        emails = fetch_emails("in:inbox", 10)
        return {
            "reply": f"Here are your latest {len(emails)} emails.",
            "emails": emails
        }

    if command.startswith("search subject "):
        subject = command.replace("search subject ", "", 1)
        emails = fetch_emails(f"subject:({subject})")
        return {
            "reply": f"Found {len(emails)} emails.",
            "emails": emails
        }

    if command.startswith("search from "):
        sender = command.replace("search from ", "", 1)
        emails = fetch_emails(f"from:({sender})")
        return {
            "reply": f"Found {len(emails)} emails.",
            "emails": emails
        }

    if "read email" in command or "open email" in command:
        number_words = {
            "one": 1, "two": 2, "three": 3, "four": 4,
            "five": 5, "six": 6, "seven": 7, "eight": 8,
            "nine": 9, "ten": 10
        }

        number = None
        for word, value in number_words.items():
            if word in command:
                number = value
                break

        import re
        match = re.search(r"\b\d+\b", command)
        if match:
            number = int(match.group())

        if number is None:
            return {"reply": "Please say read email one or read email two."}

        emails = fetch_emails("in:inbox", 10)

        if 1 <= number <= len(emails):
            return {
                "reply": f"Opening email {number}.",
                "selected": emails[number - 1]
            }

        return {"reply": "That email number is not available."}

    if command in ["stop", "stop reading", "quiet"]:
        return {"reply": "Okay. You can stop audio using the Stop button."}

    return {
        "reply": (
            f"I heard: {command}. "
            "Try saying read my emails or help."
        )
    }


# Keep your existing HTML frontend in this variable.
# Paste your previous complete HTML between the triple quotes.
HTML = r"""
<!DOCTYPE html>
<html>
<head>
    <title>Gmail Assistant</title>
</head>
<body>
    <h1>My Gmail Assistant</h1>
    <button onclick="loadEmails()">Read Latest Emails</button>
    <button onclick="startListening()">Speak</button>
    <input id="command" placeholder="Type a command">
    <button onclick="sendCommand()">Run Command</button>
    <p id="status">Ready</p>
    <div id="emails"></div>

<script>
function status(text) {
    document.getElementById("status").textContent = text;
}

async function sendCommand(text) {
    const command = (text ||
        document.getElementById("command").value).trim();

    if (!command) {
        status("Please say or type a command.");
        return;
    }

    status("Processing: " + command);

    try {
        const response = await fetch("/api/command", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({command: command})
        });

        const data = await response.json();
        status(data.reply || data.error || "Done");

        if (data.emails) renderEmails(data.emails);

        if (data.selected) {
            renderEmails([data.selected]);
            speak(data.selected.subject + ". " +
                  (data.selected.body || data.selected.snippet));
        } else if (data.reply) {
            speak(data.reply);
        }
    } catch (error) {
        status("Cannot connect to Python Flask server.");
    }
}

async function loadEmails() {
    status("Loading emails...");
    try {
        const response = await fetch("/api/emails");
        const data = await response.json();

        if (!response.ok) throw new Error(data.error);

        renderEmails(data.emails);
        status("Loaded " + data.emails.length + " emails.");
    } catch (error) {
        status("Error: " + error.message);
    }
}

function renderEmails(emails) {
    const root = document.getElementById("emails");
    root.replaceChildren();

    emails.forEach((email, index) => {
        const card = document.createElement("div");
        const title = document.createElement("h3");
        const sender = document.createElement("p");
        const body = document.createElement("p");
        const button = document.createElement("button");

        title.textContent = (index + 1) + ". " + email.subject;
        sender.textContent = "From: " + email.sender;
        body.textContent = email.snippet || email.body || "";
        button.textContent = "Read Aloud";
        button.onclick = () => speak(
            email.subject + ". " + (email.body || email.snippet)
        );

        card.append(title, sender, body, button);
        card.style.cssText =
            "padding:15px;margin:12px;border:1px solid #ccc;border-radius:8px";
        root.appendChild(card);
    });
}

function speak(text) {
    if (!("speechSynthesis" in window)) return;
    speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-IN";
    speechSynthesis.speak(utterance);
}

function startListening() {
    const SR = window.SpeechRecognition ||
               window.webkitSpeechRecognition;

    if (!SR) {
        status("Use Google Chrome or type your command.");
        return;
    }

    const recognition = new SR();
    recognition.lang = "en-IN";
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.onstart = () => status("Listening... Speak now.");

    recognition.onresult = event => {
        const text = event.results[0][0].transcript;
        document.getElementById("command").value = text;
        status("Recognized: " + text);
        sendCommand(text);
    };

    recognition.onerror = event => {
        status("Voice error: " + event.error);
    };

    recognition.onend = () => {
        console.log("Voice recognition ended.");
    };

    recognition.start();
}
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/api/emails")
def emails_api():
    try:
        return jsonify(emails=fetch_emails())
    except Exception as error:
        app.logger.exception("Gmail error")
        return jsonify(error=str(error)), 500


@app.route("/api/command", methods=["POST"])
def command_api():
    try:
        data = request.get_json(silent=True) or {}
        command = data.get("command", "")
        return jsonify(process_command(command))
    except Exception as error:
        app.logger.exception("Command error")
        return jsonify(error=str(error)), 500


if __name__ == "__main__":
    print("Gmail Assistant: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
print("Gmail connected successfully!")
print(f"Emails found: {len(emails)}")