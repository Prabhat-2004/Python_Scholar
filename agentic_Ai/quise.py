
from flask import Flask, render_template_string, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "india-quiz-secret-key"

CAPITALS = {
    "Andhra Pradesh": "Amaravati",
    "Arunachal Pradesh": "Itanagar",
    "Assam": "Dispur",
    "Bihar": "Patna",
    "Chhattisgarh": "Raipur",
    "Goa": "Panaji",
    "Gujarat": "Gandhinagar",
    "Haryana": "Chandigarh",
    "Himachal Pradesh": "Shimla",
    "Jharkhand": "Ranchi",
    "Karnataka": "Bengaluru",
    "Kerala": "Thiruvananthapuram",
    "Madhya Pradesh": "Bhopal",
    "Maharashtra": "Mumbai",
    "Manipur": "Imphal",
    "Meghalaya": "Shillong",
    "Mizoram": "Aizawl",
    "Nagaland": "Kohima",
    "Odisha": "Bhubaneswar",
    "Punjab": "Chandigarh",
    "Rajasthan": "Jaipur",
    "Sikkim": "Gangtok",
    "Tamil Nadu": "Chennai",
    "Telangana": "Hyderabad",
    "Tripura": "Agartala",
    "Uttar Pradesh": "Lucknow",
    "Uttarakhand": "Dehradun",
    "West Bengal": "Kolkata"
}

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>India Capital Quest</title>

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    font-family: Arial, sans-serif;
    color: white;
    background:
        radial-gradient(circle at top left, #ff993333, transparent 35%),
        radial-gradient(circle at bottom right, #13880833, transparent 35%),
        linear-gradient(135deg, #080d1b, #17233d, #080d1b);
}

.container {
    width: 100%;
    max-width: 720px;
    padding: 32px;
    border: 1px solid #ffffff25;
    border-radius: 24px;
    background: #111a2bed;
    box-shadow: 0 20px 70px #0008;
    animation: appear .6s ease;
}

@keyframes appear {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

header { text-align: center; }

.flag {
    width: 65px;
    margin: 0 auto 16px;
    font-size: 10px;
    text-align: center;
}

.saffron, .white, .green { height: 12px; }
.saffron { background: #ff9933; }
.white { background: white; color: #174a9c; }
.green { background: #138808; }

.tag {
    color: #ff9933;
    letter-spacing: 3px;
    font-size: 11px;
    font-weight: bold;
}

h1 { font-size: clamp(26px, 5vw, 40px); }
h1 span, h2 span { color: #ff9933; }

.subtitle { color: #b5bfd2; line-height: 1.6; }

.info {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    margin: 26px 0 14px;
    font-size: 14px;
}

.progress {
    height: 6px;
    background: #ffffff18;
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 28px;
}

.progress div {
    height: 100%;
    background: linear-gradient(90deg, #ff9933, white, #138808);
}

.question-label {
    color: #5ce477;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 2px;
}

h2 { font-size: 26px; line-height: 1.4; }

.options {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

.option {
    padding: 16px;
    min-height: 58px;
    border-radius: 12px;
    border: 1px solid #ffffff25;
    background: #ffffff09;
    color: white;
    font-size: 15px;
    text-align: left;
    cursor: pointer;
    transition: .2s;
}

.option:hover {
    border-color: #ff9933;
    background: #ff993322;
    transform: translateY(-2px);
}

.voice-btn, .next-btn {
    display: inline-block;
    padding: 14px 20px;
    border: 0;
    border-radius: 12px;
    background: linear-gradient(100deg, #ff9933, #ffd08a);
    color: #101522;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
    text-decoration: none;
}

.voice-btn { margin-top: 18px; }
.voice-btn:disabled { opacity: .65; cursor: wait; }

.voice-status {
    min-height: 24px;
    margin-top: 12px;
    color: #cbd5e1;
    font-size: 14px;
}

.feedback {
    padding: 15px;
    border-radius: 12px;
    margin-top: 20px;
    line-height: 1.6;
}

.correct {
    color: #a8ffba;
    background: #13880830;
    border: 1px solid #35d65b70;
}

.wrong {
    color: #ffd0d0;
    background: #ff333322;
    border: 1px solid #ff666670;
}

.center { text-align: center; }
.score { font-size: 62px; color: #ff9933; font-weight: bold; }

footer {
    text-align: center;
    color: #8995aa;
    font-size: 11px;
    margin-top: 26px;
}

@media(max-width: 520px) {
    .container { padding: 22px; }
    .options { grid-template-columns: 1fr; }
    h2 { font-size: 22px; }
}
</style>
</head>

<body>
<div class="container">

<header>
    <div class="flag">
        <div class="saffron"></div>
        <div class="white">✺</div>
        <div class="green"></div>
    </div>
    <div class="tag">THE GEOGRAPHY CHALLENGE</div>
    <h1>INDIA <span>CAPITAL QUEST</span></h1>
    <p class="subtitle">
        28 states. 28 capitals. Speak or select your answer!
    </p>
</header>

{% if finished %}

<div class="center">
    <div style="font-size:48px">🏆</div>
    <div class="question-label">QUIZ COMPLETED</div>
    <div class="score">{{ score }} / {{ total }}</div>

    <h2>
    {% if score == total %}
        Perfect score! Amazing!
    {% elif score >= total // 2 %}
        Well done, explorer!
    {% else %}
        Keep learning and try again!
    {% endif %}
    </h2>

    <p class="subtitle">
        You answered {{ score }} out of {{ total }} correctly.
    </p>

    <a class="next-btn" href="{{ url_for('restart') }}">
        ↻ Play Again
    </a>
</div>

{% else %}

<div class="info">
    <span>QUESTION {{ number }} / {{ total }}</span>
    <span>⭐ Score: {{ score }}</span>
</div>

<div class="progress">
    <div style="width:{{ ((number - 1) / total * 100)|round }}%"></div>
</div>

<div class="question-label">FIND THE CAPITAL</div>

<h2>
    What is the capital of <span>{{ state }}</span>?
</h2>

{% if not answered %}

<form id="answerForm" method="POST" action="{{ url_for('answer') }}">
    <div class="options">
        {% for option in options %}
        <button class="option" type="submit"
                name="answer" value="{{ option }}">
            {{ "ABCD"[loop.index0] }}. {{ option }}
        </button>
        {% endfor %}
    </div>
</form>

<button type="button" class="voice-btn" id="voiceBtn"
        onclick="startVoice()">
    🎤 Speak Answer
</button>

<div class="voice-status" id="voiceStatus" aria-live="polite">
    Click the microphone and speak your answer.
</div>

{% else %}

{% if correct %}
<div class="feedback correct">
    ✓ Correct answer! Excellent work.
</div>
{% else %}
<div class="feedback wrong">
    ✗ Wrong answer. The correct capital is
    <strong>{{ capital }}</strong>.
</div>
{% endif %}

<a class="next-btn" href="{{ url_for('next_question') }}">
    {% if number == total %}
        See Final Result →
    {% else %}
        Next Question →
    {% endif %}
</a>

{% endif %}
{% endif %}

<footer>LEARN INDIA ONE CAPITAL AT A TIME</footer>
</div>

<script>
function startVoice() {
    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    const status = document.getElementById("voiceStatus");
    const button = document.getElementById("voiceBtn");

    if (!SpeechRecognition) {
        status.textContent =
            "Voice input is not supported here. Please use Google Chrome.";
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-IN";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 3;

    button.disabled = true;
    button.textContent = "🎙 Listening...";
    status.textContent = "Listening... Speak the capital clearly.";

    recognition.onresult = function(event) {
        const results = event.results[0];
        const spoken = results[0].transcript.trim();

        status.textContent = "You said: " + spoken;

        // Try all recognized alternatives against the displayed choices.
        const alternatives = Array.from(results).map(
            result => result.transcript.trim().toLowerCase()
        );

        const buttons = document.querySelectorAll(
            '#answerForm button[name="answer"]'
        );

        let selected = null;

        for (const alternative of alternatives) {
            selected = Array.from(buttons).find(
                btn => btn.value.toLowerCase() === alternative
            );
            if (selected) break;
        }

        // Submit the matching option; otherwise submit the spoken words
        // so the quiz can show the correct answer and mark it wrong.
        const form = document.getElementById("answerForm");
        const input = document.createElement("input");
        input.type = "hidden";
        input.name = "answer";
        input.value = selected ? selected.value : spoken;
        form.appendChild(input);
        form.requestSubmit();
    };

    recognition.onerror = function(event) {
        if (event.error === "not-allowed") {
            status.textContent =
                "Microphone access denied. Allow microphone permission in Chrome.";
        } else if (event.error === "no-speech") {
            status.textContent =
                "No speech detected. Click the microphone and try again.";
        } else {
            status.textContent =
                "Voice error: " + event.error + ". Please try again.";
        }

        button.disabled = false;
        button.textContent = "🎤 Try Voice Again";
    };

    recognition.onend = function() {
        button.disabled = false;
        if (button.isConnected) {
            button.textContent = "🎤 Speak Answer";
        }
    };

    recognition.start();
}
</script>
</body>
</html>
"""


def start_quiz():
    questions = list(CAPITALS.items())
    random.shuffle(questions)

    session["questions"] = questions
    session["index"] = 0
    session["score"] = 0
    session["answered"] = False
    session["correct"] = False
    session["options"] = []


@app.route("/")
def home():
    if "questions" not in session:
        start_quiz()

    questions = session["questions"]
    index = session["index"]
    total = len(questions)

    if index >= total:
        return render_template_string(
            HTML,
            finished=True,
            score=session["score"],
            total=total
        )

    state, capital = questions[index]

    if not session["answered"]:
        wrong = [
            value for value in CAPITALS.values()
            if value != capital
        ]
        options = random.sample(wrong, 3) + [capital]
        random.shuffle(options)
        session["options"] = options
    else:
        options = session["options"]

    return render_template_string(
        HTML,
        finished=False,
        state=state,
        capital=capital,
        options=options,
        number=index + 1,
        total=total,
        score=session["score"],
        answered=session["answered"],
        correct=session["correct"]
    )


@app.route("/answer", methods=["POST"])
def answer():
    if "questions" not in session:
        return redirect(url_for("restart"))

    if session["answered"]:
        return redirect(url_for("home"))

    index = session["index"]
    questions = session["questions"]

    if index >= len(questions):
        return redirect(url_for("home"))

    state, capital = questions[index]
    selected = request.form.get("answer", "").strip()

    session["correct"] = selected.casefold() == capital.casefold()
    session["answered"] = True

    if session["correct"]:
        session["score"] += 1

    return redirect(url_for("home"))


@app.route("/next")
def next_question():
    if "questions" not in session:
        return redirect(url_for("restart"))

    if session["answered"]:
        session["index"] += 1
        session["answered"] = False
        session["correct"] = False
        session["options"] = []

    return redirect(url_for("home"))


@app.route("/restart")
def restart():
    session.clear()
    start_quiz()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
