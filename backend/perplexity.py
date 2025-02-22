from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/perplexity_search', methods=['GET'])
def perplexity_search():
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        return jsonify({"error": "Missing Perplexity API key"}), 500

    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "sonar-pro", # sonar-reasoning-pro
        "messages": [
            {
                "role": "user",
                "content": "Provide the 10 most recent linkedin computer science internship job postings."
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return jsonify(data), 200

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": str(e),
            "response_text": e.response.text if e.response else ""
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
