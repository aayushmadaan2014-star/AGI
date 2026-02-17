from flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

# ==============================
# RANDOM FUNNY AI NAME
# ==============================

funny_names = [
    "Quantum Pickle",
    "Neon Potato 9000",
    "Sir Laughs-a-Lot AI",
    "Cyber Panda",
    "Captain BrainSpark",
    "Glitchy Goblin",
    "Professor Zap",
    "Disco Neuron",
    "MegaMind Jr.",
    "Pixel Wizard"
]

AI_NAME = random.choice(funny_names)

# ==============================
# CONFIG
# ==============================

DIM = 3
vocab = {}

base_knowledge = [
    "The central processing unit executes instructions efficiently.",
    "Artificial intelligence analyzes patterns in data.",
    "Regular exercise improves health and reduces stress.",
    "Effective communication improves relationships.",
    "Inflation increases prices over time.",
    "Supply and demand control markets.",
    "A firewall protects networks from threats.",
    "Photosynthesis produces energy in plants."
]

# ==============================
# VECTOR SYSTEM
# ==============================

def vectorize(sentence):
    words = sentence.lower().split()
    for word in words:
        if word not in vocab:
            vocab[word] = [random.uniform(0, 1) for _ in range(DIM)]

def vectorize_sentence_average(sentence):
    words = sentence.lower().split()
    vectorize(sentence)

    totals = [0.0] * DIM
    for word in words:
        for i in range(DIM):
            totals[i] += vocab[word][i]

    for i in range(DIM):
        totals[i] /= max(len(words), 1)

    return totals

def train(sentence, correct_label, lr):
    vectorize(sentence)
    words = sentence.lower().split()
    for word in words:
        for i in range(DIM):
            error = vocab[word][i] - correct_label[i]
            vocab[word][i] -= error * lr

def quick_train():
    samples = [
        ("i love this amazing thing", [0.6, 0.4, 0.9]),
        ("i hate this terrible thing", [0.8, 0.7, 0.1]),
    ]
    for _ in range(3):
        for sentence, label in samples:
            train(sentence, label, 0.01)

quick_train()

# ==============================
# FILTER + MARKOV
# ==============================

def filter_sentences_by_emotion(vec):
    emotional, intense, positive = vec
    filtered = []

    for sentence in base_knowledge:
        lower = sentence.lower()

        if positive > 0.6:
            if any(w in lower for w in ["improve", "energy", "efficient"]):
                filtered.append(sentence)

        elif positive < 0.4:
            if any(w in lower for w in ["stress", "threat"]):
                filtered.append(sentence)

        else:
            filtered.append(sentence)

    return filtered if filtered else base_knowledge

def build_markov(sentences):
    markov = {}
    for sentence in sentences:
        words = sentence.lower().split()
        for i in range(len(words) - 1):
            markov.setdefault(words[i], []).append(words[i + 1])
    return markov

# ==============================
# HTML (Responsive Neon)
# ==============================

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ai_name}}</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: radial-gradient(circle at center, #111 0%, #000 80%);
    font-family: Arial, sans-serif;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

/* CONTAINER */
.container {
    width: 95%;
    max-width: 600px;
    height: 95vh;
    max-height: 800px;
    display: flex;
    flex-direction: column;
    border-radius: 20px;
    border: 2px solid #00ffff;
    box-shadow: 0 0 25px #00ffff;
    background: rgba(0,0,0,0.92);
    padding: 15px;
}

/* TITLE */
h1 {
    text-align: center;
    color: #ff00ff;
    text-shadow: 0 0 20px #ff00ff;
    margin: 10px 0;
    font-size: 22px;
}

/* CHATBOX */
#chatbox {
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    padding-right: 5px;
}

/* MESSAGE ROW */
.message {
    display: flex;
    margin: 6px 0;
}

/* HUMAN RIGHT */
.user {
    justify-content: flex-end;
}

.user .bubble {
    background: #00ffff;
    color: black;
    padding: 10px 14px;
    border-radius: 15px 15px 0 15px;
    max-width: 75%;
    word-wrap: break-word;
    box-shadow: 0 0 12px #00ffff;
}

/* BOT LEFT */
.bot {
    justify-content: flex-start;
}

.bot .bubble {
    background: #ff00ff;
    color: white;
    padding: 10px 14px;
    border-radius: 15px 15px 15px 0;
    max-width: 75%;
    word-wrap: break-word;
    box-shadow: 0 0 12px #ff00ff;
}

/* INPUT ROW */
.input-row {
    display: flex;
    margin-top: 10px;
}

input {
    flex: 1;
    padding: 12px;
    background: #111;
    border: 1px solid #00ffff;
    color: white;
    border-radius: 10px 0 0 10px;
    outline: none;
}

button {
    padding: 12px 16px;
    background: #ff00ff;
    border: none;
    color: white;
    cursor: pointer;
    border-radius: 0 10px 10px 0;
    box-shadow: 0 0 10px #ff00ff;
}

button:hover {
    background: #00ffff;
    box-shadow: 0 0 20px #00ffff;
}

/* EMOTION DISPLAY */
#emotion {
    margin-top: 8px;
    font-size: 13px;
    color: #00ff99;
    text-align: center;
}

/* MOBILE TWEAKS */
@media (max-width: 480px) {
    h1 { font-size: 18px; }
    .bubble { font-size: 14px; }
}
</style>
</head>

<body>

<div class="container">
<h1>⚡ {{ai_name}} ⚡</h1>
<!-- AD BANNER -->
<div style="text-align:center; margin-bottom:10px;">
    <script async src="https://example-ad-network.com/ads.js"></script>
    <ins class="adsbyexample"
         style="display:block"
         data-ad-client="YOUR_CLIENT_ID"
         data-ad-slot="12345678"></ins>
    <script>
         (adsbyexample = window.adsbyexample || []).push({});
    </script>
</div>


<div id="chatbox"></div>

<div class="input-row">
    <input id="input" placeholder="Talk to {{ai_name}}..." />
    <button onclick="send()">Send</button>
</div>

<div id="emotion"></div>
</div>

<script>
let inputField = document.getElementById("input");
let chatbox = document.getElementById("chatbox");

inputField.addEventListener("keypress", function(e) {
    if (e.key === "Enter") send();
});

async function send() {
    let message = inputField.value.trim();
    if (!message) return;

    chatbox.innerHTML += `
        <div class="message user">
            <div class="bubble">${message}</div>
        </div>
    `;

    inputField.value = "";
    chatbox.scrollTop = chatbox.scrollHeight;

    let response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message})
    });

    let data = await response.json();

    chatbox.innerHTML += `
        <div class="message bot">
            <div class="bubble">${data.reply}</div>
        </div>
    `;

    document.getElementById("emotion").innerHTML =
        "Emotional: " + data.emotion.emotional +
        " | Intense: " + data.emotion.intense +
        " | Positive: " + data.emotion.positive;

    chatbox.scrollTop = chatbox.scrollHeight;
}
</script>

</body>
</html>
"""

# ==============================
# ROUTES
# ==============================

@app.route("/")
def home():
    return render_template_string(HTML_PAGE, ai_name=AI_NAME)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]

    vec = vectorize_sentence_average(user_input)
    filtered = filter_sentences_by_emotion(vec)
    markov = build_markov(filtered)

    start_word = random.choice(list(markov.keys()))
    result = [start_word]

    current_word = start_word
    for _ in range(random.randint(8, 15)):
        if current_word in markov:
            next_word = random.choice(markov[current_word])
            result.append(next_word)
            current_word = next_word
        else:
            break

    return jsonify({
        "reply": " ".join(result),
        "emotion": {
            "emotional": round(vec[0], 2),
            "intense": round(vec[1], 2),
            "positive": round(vec[2], 2)
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
