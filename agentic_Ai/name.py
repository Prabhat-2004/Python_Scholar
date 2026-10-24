
from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

# Cinematic gradient backgrounds
BACKGROUNDS = [
    "linear-gradient(135deg, #141e30, #243b55)",
    "linear-gradient(135deg, #42275a, #734b6d)",
    "linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
    "linear-gradient(135deg, #200122, #6f0000)",
    "linear-gradient(135deg, #134e5e, #71b280)",
    "linear-gradient(135deg, #360033, #0b8793)",
    "linear-gradient(135deg, #232526, #414345)",
    "linear-gradient(135deg, #3a1c71, #d76d77, #ffaf7b)",
]

# Ayushi - Sister quotes
SISTER_QUOTES = [
    "A sister is a forever friend and a beautiful blessing. ❤️",
    "Sisters make ordinary moments unforgettable. 🌸",
    "A sister's love stays with you forever. 💖",
]

# Lija - Elder sister quotes
OLDER_SISTER_QUOTES = [
    "An elder sister is a guide, protector, and lifelong blessing. ❤️",
    "A big sister makes life's journey easier and brighter. 🌸",
    "An elder sister's love is a shelter in every storm. 💖",
]

# Prachi - Sister quotes
SISTER_QUOTES_NEW = [
    "A sister is a forever friend and a beautiful blessing. 🌷",
    "Sisters share love, laughter, and unforgettable memories. 💕",
    "Life is more beautiful with a loving sister. ❤️",
]

# Preeti - Girlfriend quotes
GIRLFRIEND_QUOTES = [
    "You make my world brighter just by being in it. ❤️",
    "My favourite place is wherever you are. 💕",
    "Every love story is special, but ours is my favourite. 🌹",
]

# Prasant - Brother quotes
BROTHER_QUOTES = [
    "A brother is a friend life gives you forever. 💪",
    "Brothers may fight, but their bond never breaks. ❤️",
    "A brother's support makes every challenge easier. 🌟",
]

# Sanjay and Patitapaban - Big brother quotes
BIG_BROTHER_QUOTES = [
    "A big brother is a protector, guide, and lifelong friend. 💪",
    "A big brother always stands beside his family. ❤️",
    "A brother's support gives you courage to face the world. 🌟",
]

# Trilochan - Friendship quotes
FRIEND_QUOTES = [
    "Good friends make life's journey beautiful. 🤝",
    "Real friendship is a treasure that time cannot replace. ❤️",
    "Friends make happy memories even out of ordinary days. 🌟",
]

# Subhasree and Sila - Daughter quotes
DAUGHTER_QUOTES = [
    "A daughter is a little sunshine that brightens every day. ☀️",
    "A daughter fills the heart with endless love. 💖",
    "A daughter is one of life's most precious blessings. 🌸",
]

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A Special Welcome</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            min-height: 100vh;
            font-family: 'Segoe UI', Arial, sans-serif;
            color: white;
            background: {{ background }};
            background-size: 300% 300%;
            animation: gradientMove 12s ease infinite;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 24px;
            overflow-x: hidden;
            position: relative;
        }

        @keyframes gradientMove {
            0%   { background-position: 0% 50%; }
            50%  { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(3px);
            opacity: 0.22;
            pointer-events: none;
            animation: float 9s ease-in-out infinite;
        }

        .orb-one {
            width: 220px;
            height: 220px;
            background: #ff69b4;
            top: 5%;
            left: 5%;
        }

        .orb-two {
            width: 280px;
            height: 280px;
            background: #00d4ff;
            right: 3%;
            bottom: 4%;
            animation-delay: -3s;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-25px) scale(1.08); }
        }

        .card {
            width: 100%;
            max-width: 650px;
            text-align: center;
            padding: 48px 32px;
            border: 1px solid rgba(255,255,255,0.25);
            border-radius: 28px;
            background: rgba(255,255,255,0.10);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            box-shadow: 0 25px 70px rgba(0,0,0,0.3);
            position: relative;
            z-index: 1;
            animation: appear 0.9s ease both;
        }

        @keyframes appear {
            from { opacity: 0; transform: translateY(25px) scale(0.97); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        .heart {
            font-size: 48px;
            margin-bottom: 16px;
            animation: heartbeat 1.5s infinite;
        }

        @keyframes heartbeat {
            0%, 100% { transform: scale(1); }
            15% { transform: scale(1.16); }
            30% { transform: scale(1); }
            45% { transform: scale(1.1); }
        }

        .eyebrow {
            text-transform: uppercase;
            letter-spacing: 4px;
            font-size: 12px;
            opacity: 0.8;
            margin-bottom: 15px;
        }

        h1 {
            font-size: clamp(30px, 7vw, 49px);
            line-height: 1.2;
            margin-bottom: 18px;
            overflow-wrap: anywhere;
        }

        .subtitle {
            font-size: 17px;
            line-height: 1.8;
            color: rgba(255,255,255,0.88);
        }

        .quote {
            margin: 28px 0;
            padding: 22px;
            border-radius: 18px;
            background: rgba(255,255,255,0.10);
            border-left: 3px solid rgba(255,255,255,0.8);
            font-size: 19px;
            line-height: 1.7;
            font-style: italic;
        }

        .buttons {
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 28px;
        }

        .btn {
            display: inline-block;
            padding: 13px 21px;
            border-radius: 50px;
            border: 1px solid rgba(255,255,255,0.4);
            color: white;
            text-decoration: none;
            font-size: 14px;
            font-weight: 600;
            background: rgba(255,255,255,0.12);
            transition: transform 0.25s, background 0.25s;
            cursor: pointer;
        }

        .btn:hover {
            transform: translateY(-3px);
            background: rgba(255,255,255,0.25);
        }

        .btn-primary {
            background: white;
            color: #252544;
        }

        .form {
            margin-top: 28px;
        }

        .form label {
            display: block;
            margin-bottom: 12px;
            font-size: 14px;
            opacity: 0.9;
        }

        .form input {
            width: 100%;
            padding: 15px 18px;
            border: 1px solid rgba(255,255,255,0.35);
            border-radius: 14px;
            background: rgba(0,0,0,0.16);
            color: white;
            outline: none;
            font-size: 16px;
            text-align: center;
        }

        .form input::placeholder {
            color: rgba(255,255,255,0.65);
        }

        .form input:focus {
            border-color: white;
            box-shadow: 0 0 0 3px rgba(255,255,255,0.12);
        }

        .form button {
            margin-top: 14px;
            width: 100%;
        }

        .footer {
            margin-top: 30px;
            font-size: 12px;
            opacity: 0.65;
            letter-spacing: 1px;
        }

        @media (max-width: 480px) {
            .card {
                padding: 35px 22px;
                border-radius: 22px;
            }

            .quote {
                font-size: 17px;
                padding: 18px;
            }

            .eyebrow {
                letter-spacing: 2px;
            }
        }
    </style>
</head>

<body>
    <div class="orb orb-one"></div>
    <div class="orb orb-two"></div>

    <main class="card">
        <div class="heart">
            {% if category == 'girlfriend' %}❤️
            {% elif category == 'sister' %}🌸
            {% elif category == 'brother' %}💙
            {% elif category == 'friend' %}🤝
            {% elif category == 'daughter' %}🌷
            {% else %}✨
            {% endif %}
        </div>

        <p class="eyebrow">A little message for you</p>

        {% if name %}
            <h1>Welcome, {{ name }}!</h1>

            {% if category == 'girlfriend' %}
                <p class="subtitle">To someone who makes life more beautiful.</p>
            {% elif category == 'sister' %}
                <p class="subtitle">A special message for a wonderful sister.</p>
            {% elif category == 'brother' %}
                <p class="subtitle">For a brother who means so much.</p>
            {% elif category == 'friend' %}
                <p class="subtitle">Celebrating a friendship worth keeping.</p>
            {% elif category == 'daughter' %}
                <p class="subtitle">A beautiful blessing, today and always.</p>
            {% else %}
                <p class="subtitle">You are special. May your day be full of happiness!</p>
            {% endif %}

            {% if quote %}
                <div class="quote">{{ quote }}</div>
            {% endif %}

            <div class="buttons">
                <a class="btn btn-primary" href="/">Enter Another Name</a>
                <a class="btn" href="/welcome?name={{ name | urlencode }}">New Quote & Background</a>
            </div>
        {% else %}
            <h1>A Special Welcome ✨</h1>
            <p class="subtitle">
                Every name has a story. Enter a name to discover a special message.
            </p>

            <form class="form" action="/welcome" method="get">
                <label for="name">Who would you like to surprise?</label>
                <input
                    type="text"
                    id="name"
                    name="name"
                    placeholder="Enter a name..."
                    maxlength="60"
                    required
                    autofocus
                >
                <button class="btn btn-primary" type="submit">
                    Reveal Their Message ✨
                </button>
            </form>
        {% endif %}

        <div class="footer">MADE WITH ❤️ AND GOOD VIBES</div>
    </main>
</body>
</html>
"""


def get_message(name):
    key = name.strip().casefold()

    if key == "ayushi":
        return "sister", random.choice(SISTER_QUOTES)

    elif key == "lija":
        return "sister", random.choice(OLDER_SISTER_QUOTES)

    elif key == "prachi":
        return "sister", random.choice(SISTER_QUOTES_NEW)

    elif key == "preeti":
        return "girlfriend", random.choice(GIRLFRIEND_QUOTES)

    elif key == "prasant":
        return "brother", random.choice(BROTHER_QUOTES)

    elif key == "sanjay":
        return "brother", random.choice(BIG_BROTHER_QUOTES)

    elif key == "patitapaban":
        return "brother", random.choice(BIG_BROTHER_QUOTES)

    elif key == "trilochan":
        return "friend", random.choice(FRIEND_QUOTES)

    elif key in ("subhasree", "sila"):
        return "daughter", random.choice(DAUGHTER_QUOTES)

    else:
        return "", ""


@app.route("/")
def home():
    return render_template_string(
        HTML,
        name="",
        category="",
        quote="",
        background=random.choice(BACKGROUNDS),
    )


@app.route("/welcome")
def welcome():
    name = request.args.get("name", "").strip()[:60]

    if not name:
        return home()

    category, quote = get_message(name)

    return render_template_string(
        HTML,
        name=name,
        category=category,
        quote=quote,
        background=random.choice(BACKGROUNDS),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
