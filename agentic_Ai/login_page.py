
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Login credentials
INBUILT_USER_NAME = "admin"
INBUILT_USER_PASSWORD = "admin123"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Egg Heist | Login</title>

<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Outfit:wght@300;400;500;600;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --gold: #ffc857;
    --bg: #080b16;
    --panel: #111827;
    --muted: #929bb0;
}

body {
    min-height: 100vh;
    background: var(--bg);
    color: #f8f7ff;
    font-family: 'Outfit', sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 25px;
    overflow-x: hidden;
}

body::before {
    content: "";
    position: fixed;
    width: 500px;
    height: 500px;
    background: #7040ff;
    filter: blur(150px);
    opacity: .18;
    top: -200px;
    left: -150px;
    pointer-events: none;
}

body::after {
    content: "";
    position: fixed;
    width: 450px;
    height: 450px;
    background: #ffb52e;
    filter: blur(150px);
    opacity: .12;
    bottom: -200px;
    right: -100px;
    pointer-events: none;
}

.container {
    width: 100%;
    max-width: 1100px;
    min-height: 650px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    position: relative;
    z-index: 1;
    background: #0d1220;
    border: 1px solid #ffffff15;
    border-radius: 26px;
    overflow: hidden;
    box-shadow: 0 30px 100px #0008;
    animation: appear .8s ease;
}

@keyframes appear {
    from { opacity: 0; transform: translateY(25px); }
    to { opacity: 1; transform: translateY(0); }
}

/* LEFT SIDE */

.hero {
    padding: 35px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(ellipse at 50% 50%, #242347 0%, #111627 55%, #0b1020 100%);
    border-right: 1px solid #ffffff12;
}

.brand {
    font-family: 'Orbitron', sans-serif;
    font-size: 19px;
    font-weight: 800;
    letter-spacing: 2px;
}

.brand span {
    color: var(--gold);
}

.brand .white {
    color: white;
}

.scene {
    height: 280px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

.moon {
    position: absolute;
    width: 190px;
    height: 190px;
    border-radius: 50%;
    background: #ffc8570c;
    box-shadow: 0 0 80px #ffc85715;
}

.stars {
    position: absolute;
    top: 20px;
    left: 15%;
    color: var(--gold);
    letter-spacing: 20px;
    line-height: 3.5;
    font-size: 19px;
    opacity: .8;
}

.vault {
    position: absolute;
    right: 5%;
    width: 190px;
    height: 210px;
    border-radius: 18px;
    background: linear-gradient(145deg, #6e647b, #292c43 45%, #141a2b);
    border: 5px solid #a7a0b5;
    box-shadow: 0 20px 35px #0007, inset 0 0 20px #0007;
    transform: perspective(500px) rotateY(-10deg);
}

.vault::before {
    content: "";
    position: absolute;
    inset: 12px;
    border: 2px solid #d0b66c;
    border-radius: 10px;
}

.vault::after {
    content: "✦";
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 55px;
    height: 55px;
    display: grid;
    place-items: center;
    border-radius: 50%;
    color: var(--gold);
    font-size: 27px;
    background: #111827;
    border: 4px solid #c6ad72;
    box-shadow: 0 0 20px #ffc85725;
}

.character {
    position: absolute;
    left: 12%;
    bottom: 25px;
    width: 115px;
    height: 180px;
    animation: sneak 3s ease-in-out infinite;
}

@keyframes sneak {
    0%, 100% { transform: translateY(0) rotate(-2deg); }
    50% { transform: translateY(-9px) rotate(2deg); }
}

.hood {
    position: absolute;
    width: 85px;
    height: 85px;
    left: 15px;
    top: 0;
    border-radius: 45% 45% 35% 35%;
    background: linear-gradient(135deg, #a16bff, #5230a1);
    border: 3px solid #c4a4ff;
}

.face {
    position: absolute;
    width: 57px;
    height: 38px;
    left: 29px;
    top: 30px;
    background: #f3c9a4;
    border-radius: 35%;
    z-index: 2;
}

.eye {
    position: absolute;
    top: 15px;
    width: 6px;
    height: 8px;
    border-radius: 50%;
    background: #242038;
}

.eye-left { left: 14px; }
.eye-right { right: 14px; }

.body {
    position: absolute;
    top: 75px;
    left: 9px;
    width: 98px;
    height: 100px;
    border-radius: 25px 25px 12px 12px;
    background: linear-gradient(140deg, #8053db, #30215d);
    border: 2px solid #a584f1;
}

.bag {
    position: absolute;
    right: -15px;
    bottom: 10px;
    font-size: 35px;
    transform: rotate(15deg);
    z-index: 3;
}

.egg {
    position: absolute;
    font-size: 38px;
    filter: drop-shadow(0 5px 12px #ffc85750);
    animation: float 3s ease-in-out infinite;
}

.egg-one {
    top: 25px;
    right: 24%;
}

.egg-two {
    bottom: 15px;
    right: 10%;
    animation-delay: 1s;
}

@keyframes float {
    0%, 100% { transform: translateY(0) rotate(-5deg); }
    50% { transform: translateY(-12px) rotate(5deg); }
}

.hero-text .eyebrow {
    color: var(--gold);
    font-size: 10px;
    letter-spacing: 2.5px;
    font-weight: 700;
}

.hero-text h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(27px, 3vw, 38px);
    line-height: 1.35;
    margin: 14px 0;
}

.hero-text h1 span {
    color: var(--gold);
}

.hero-text p {
    color: var(--muted);
    font-size: 14px;
    line-height: 1.8;
}

.mission {
    margin-top: 25px;
    color: #a7afc4;
    font-size: 10px;
    letter-spacing: 2px;
}

.mission span {
    color: #55e6a5;
    margin-right: 8px;
}

/* RIGHT SIDE */

.login-section {
    padding: 45px clamp(25px, 5vw, 60px);
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.topline {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    margin-bottom: 45px;
    font-size: 9px;
    letter-spacing: 1px;
    color: var(--muted);
}

.online {
    color: #55e6a5;
}

.welcome-icon {
    width: 65px;
    height: 65px;
    display: grid;
    place-items: center;
    font-size: 30px;
    border: 1px solid #ffc85740;
    border-radius: 18px;
    background: linear-gradient(135deg, #ffc85718, #8c5cff18);
    margin-bottom: 25px;
}

h2 {
    font-size: clamp(25px, 3vw, 31px);
    line-height: 1.4;
}

h2 span {
    color: var(--gold);
}

.subtitle {
    margin: 12px 0 30px;
    color: var(--muted);
    font-size: 13px;
    line-height: 1.7;
}

.message {
    padding: 13px 15px;
    margin-bottom: 22px;
    border-radius: 10px;
    font-size: 13px;
    line-height: 1.6;
    overflow-wrap: anywhere;
}

.success {
    background: #55e6a510;
    border: 1px solid #55e6a550;
    color: #65efb2;
}

.error {
    background: #ff555510;
    border: 1px solid #ff555550;
    color: #ff8a8a;
}

label {
    display: block;
    margin: 22px 0 10px;
    font-size: 10px;
    letter-spacing: 1.5px;
    font-weight: 700;
    color: #d4d8e5;
}

.input-wrap {
    display: flex;
    align-items: center;
    height: 54px;
    background: #080c17;
    border: 1px solid #ffffff1c;
    border-radius: 12px;
    transition: .25s;
}

.input-wrap:focus-within {
    border-color: var(--gold);
    box-shadow: 0 0 0 3px #ffc85712;
}

.input-icon {
    padding-left: 17px;
    color: var(--gold);
    font-size: 19px;
}

input {
    flex: 1;
    min-width: 0;
    height: 100%;
    border: 0;
    outline: none;
    background: transparent;
    padding: 0 13px;
    color: white;
    font: inherit;
    font-size: 13px;
}

input::placeholder {
    color: #646e84;
}

.eye-button {
    border: 0;
    background: transparent;
    color: #9da6bb;
    cursor: pointer;
    padding: 12px;
    font-size: 17px;
}

.login-button {
    margin-top: 30px;
    width: 100%;
    height: 56px;
    border: 0;
    border-radius: 12px;
    background: linear-gradient(100deg, #ffb936, #ffda7a);
    color: #171323;
    font-family: 'Orbitron', sans-serif;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    box-shadow: 0 8px 25px #ffc85720;
    transition: .25s;
}

.login-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px #ffc85745;
}

.arrow {
    font-size: 20px;
}

.divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 30px 0 20px;
    color: #737d92;
    font-size: 8px;
    letter-spacing: 1.3px;
    white-space: nowrap;
}

.divider::before,
.divider::after {
    content: "";
    height: 1px;
    background: #ffffff15;
    flex: 1;
}

.security {
    display: flex;
    justify-content: center;
    gap: 8px;
    color: #8e99ad;
    font-size: 11px;
}

footer {
    margin-top: 45px;
    text-align: center;
    font-size: 9px;
    letter-spacing: 1.5px;
    color: #626d82;
}

/* MOBILE */

@media (max-width: 760px) {
    body {
        padding: 15px;
    }

    .container {
        grid-template-columns: 1fr;
        max-width: 480px;
    }

    .hero {
        min-height: 430px;
        padding: 25px;
        border-right: 0;
        border-bottom: 1px solid #ffffff12;
    }

    .scene {
        height: 210px;
    }

    .vault {
        width: 145px;
        height: 160px;
    }

    .character {
        transform: scale(.8);
        transform-origin: bottom left;
        left: 8%;
    }

    .hero-text h1 {
        font-size: 27px;
    }

    .login-section {
        padding: 30px 25px;
    }

    .topline {
        margin-bottom: 28px;
    }

    footer {
        margin-top: 30px;
    }
}
</style>
</head>

<body>
<main class="container">

    <section class="hero">
        <div class="brand">🥚 EGG<span class="white">HEIST</span></div>

        <div class="scene">
            <div class="moon"></div>
            <div class="stars">✦ &nbsp; · &nbsp; ✧<br> &nbsp; ✦ &nbsp; ·</div>

            <div class="vault"></div>

            <div class="character">
                <div class="hood"></div>
                <div class="face">
                    <span class="eye eye-left"></span>
                    <span class="eye eye-right"></span>
                </div>
                <div class="body"></div>
                <div class="bag">💰</div>
            </div>

            <div class="egg egg-one">🥚</div>
            <div class="egg egg-two">🥚</div>
        </div>

        <div class="hero-text">
            <div class="eyebrow">YOUR NEXT ADVENTURE STARTS HERE</div>
            <h1>Steal the night.<br><span>Own the loot.</span></h1>
            <p>Every great heist begins with a secret entrance.</p>
        </div>

        <div class="mission"><span>●</span> YOUR MISSION AWAITS</div>
    </section>

    <section class="login-section">
        <div class="topline">
            <span>RESTRICTED ACCESS</span>
            <span class="online">● SYSTEM ONLINE</span>
        </div>

        <div class="welcome-icon">🔐</div>

        <h2>Welcome back,<br><span>Heister.</span></h2>
        <p class="subtitle">Enter your credentials to access the vault.</p>

        {% if message %}
            <div class="message {{ status }}" role="status">
                {{ message }}
            </div>
        {% endif %}

        <form method="POST" action="/">
            <label for="username">USERNAME</label>
            <div class="input-wrap">
                <span class="input-icon">♟</span>
                <input type="text" id="username" name="username"
                       placeholder="Enter your username"
                       autocomplete="username" required>
            </div>

            <label for="password">PASSWORD</label>
            <div class="input-wrap">
                <span class="input-icon">♙</span>
                <input type="password" id="password" name="password"
                       placeholder="Enter your password"
                       autocomplete="current-password" required>
                <button class="eye-button" type="button"
                        onclick="togglePassword()" aria-label="Show password">
                    ◉
                </button>
            </div>

            <button class="login-button" type="submit">
                <span>UNLOCK THE VAULT</span>
                <span class="arrow">↗</span>
            </button>
        </form>

        <div class="divider">AUTHORIZED PERSONNEL ONLY</div>

        <div class="security">
            <span>🛡️</span>
            <span>Your mission data stays protected.</span>
        </div>

        <footer>© 2026 EGG HEIST · BUILT FOR THE BOLD</footer>
    </section>

</main>

<script>
function togglePassword() {
    const password = document.getElementById("password");
    password.type =
        password.type === "password" ? "text" : "password";
}
</script>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    status = ""

    if request.method == "POST":
        user_name = request.form.get("username", "").strip()
        user_password = request.form.get("password", "")

        if (
            user_name == INBUILT_USER_NAME
            and user_password == INBUILT_USER_PASSWORD
        ):
            message = "Login successful! Welcome, Admin."
            status = "success"
        else:
            message = "Invalid username or password."
            status = "error"

    return render_template_string(
        HTML_PAGE,
        message=message,
        status=status
    )


if __name__ == "__main__":
    app.run(debug=True)
