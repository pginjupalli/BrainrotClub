from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/perplexity_search', methods=['GET'])
def perplexity_search(search):
    # print(search)
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        return jsonify({"error": "Missing Perplexity API key"}), 500

    url = "https://api.perplexity.ai/chat/completions"
    
    content = f"""Provide a script for a promotional video that describes the following event.\n
        The club's name is {search["club_name"]}.\n
        The event name is {search["event_name"]}.\n
        The details are as follows: {search["details"]}.\n
        Use a(n) {search["tone"]} tone.\n
        MAKE SURE NOT TO INCLUDE ANY OTHER TEXT BESIDES THE SCRIPT.\n
        THE TEXT YOU OUTPUT WILL BE SPOKEN EXACTLY AS-IS.\n
        SO DON'T INCLUDE ANYTHING LIKE "[in an angry tone]" AT THE BEGINNING OR ANYTHING SIMILAR.\n
        THESE ARE IMPORTANT!\n
        """
        
    print(content)

    payload = {
        "model": "sonar-pro", # sonar-reasoning-pro
        "messages": [
            {
                "role": "user",
                "content": content
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
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": str(e),
            "response_text": e.response.text if e.response else ""
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
