from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("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")
ASSISTANT_ID = os.getenv("SonnyJr")

@app.route("/")
def index():
    return "✅ Sonny server is online and running!"

@app.route("/ask", methods=["POST"])
def ask_sonny():
    data = request.get_json()
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Missing 'message'"}), 400

    try:
        # Create new thread
        thread = openai.beta.threads.create()

        # Add user message
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )

        # Run assistant
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # Poll for completion
        import time
        while True:
            run_status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run_status.status == "completed":
                break
            time.sleep(1)

        # Get reply
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        reply = next((m for m in reversed(messages.data) if m.role == "assistant"), None)

        return jsonify({
            "reply": reply.content[0].text.value if reply else "No response"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
