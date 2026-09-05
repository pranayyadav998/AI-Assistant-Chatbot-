"""
app.py
------
Flask app that connects the HTML/CSS/JS frontend to the existing
chatbot logic in chatbot.py. Flask's only job here is routing:
- Serve the chat page
- Receive a message from the browser, pass it to chatbot.get_response()
- Receive feedback from the browser, pass it to chatbot.save_feedback()

No extra features (auth, database, etc.) are added.
"""

from flask import Flask, render_template, request, jsonify
import chatbot

app = Flask(__name__)


@app.route("/")
def home():
    """Serves the main chat page."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Receives a user message as JSON, sends it to Gemini via
    chatbot.get_response(), and returns the AI's reply as JSON.
    """
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please type a question first."})

    ai_response = chatbot.get_response(user_message)
    return jsonify({"response": ai_response})


@app.route("/feedback", methods=["POST"])
def feedback():
    """
    Receives feedback text as JSON and saves it using the existing
    file-handling logic in chatbot.py.
    """
    data = request.get_json(silent=True) or {}
    feedback_text = data.get("feedback", "").strip()

    saved = chatbot.save_feedback(feedback_text)

    if saved:
        return jsonify({"status": "success"})
    return jsonify({"status": "empty"})


if __name__ == "__main__":
    # debug=True is fine for local development/student projects
    app.run(debug=True)
