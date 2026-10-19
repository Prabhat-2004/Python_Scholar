
import os
import speech_recognition as sr
import pyttsx3

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Voice output
speaker = pyttsx3.init()
speaker.setProperty("rate", 165)


def speak(text):
    print("Assistant:", text)
    speaker.say(text)
    speaker.runAndWait()


def connect_gmail():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE, SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w", encoding="utf-8") as file:
            file.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def get_latest_emails(service, limit=5):
    result = service.users().messages().list(
        userId="me",
        maxResults=limit
    ).execute()

    messages = result.get("messages", [])
    emails = []

    for message in messages:
        email = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="metadata",
            metadataHeaders=["Subject", "From"]
        ).execute()

        headers = email.get("payload", {}).get("headers", [])
        details = {
            h["name"].lower(): h["value"] for h in headers
        }

        emails.append({
            "subject": details.get("subject", "No subject"),
            "sender": details.get("from", "Unknown sender")
        })

    return emails


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nListening... Speak now.")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source, timeout=5, phrase_time_limit=7
            )
        except sr.WaitTimeoutError:
            speak("I did not hear anything. Please try again.")
            return ""

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I could not understand.")
        return ""

    except sr.RequestError:
        speak("Speech recognition needs an internet connection.")
        return ""


def main():
    if not os.path.exists(CREDENTIALS_FILE):
        speak("credentials.json was not found.")
        return

    service = connect_gmail()
    speak("Gmail connected. How can I help you?")

    while True:
        command = listen()

        if not command:
            continue

        if "check email" in command or "check my email" in command:
            emails = get_latest_emails(service, 5)

            if not emails:
                speak("You have no emails in your inbox.")
            else:
                speak(f"You have {len(emails)} recent email messages.")
                for email in emails:
                    speak(
                        "From " + email["sender"] +
                        ". Subject: " + email["subject"]
                    )

        elif "read latest email" in command or "read my latest email" in command:
            emails = get_latest_emails(service, 1)

            if emails:
                speak("Latest email subject is " + emails[0]["subject"])
                speak("It is from " + emails[0]["sender"])
            else:
                speak("No email messages were found.")

        elif "how many emails" in command or "count emails" in command:
            result = service.users().messages().list(
                userId="me",
                maxResults=1
            ).execute()

            # This is an estimate of the inbox count returned by Gmail.
            count = result.get("resultSizeEstimate", 0)
            speak(f"Gmail reports approximately {count} inbox messages.")

        elif "help" in command:
            speak(
                "Say check my emails, read latest email, "
                "how many emails, or stop."
            )

        elif "stop" in command or "exit" in command or "quit" in command:
            speak("Goodbye.")
            break

        else:
            speak("Command not recognized. Say help for commands.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error:", error)
        speak("Something went wrong. Check the terminal.")
