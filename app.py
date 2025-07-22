from flask import Flask, request, jsonify
import requests
import json
import base64

app = Flask(__name__)

API_USER = '726098218'
API_SECRET = 'dxyXDBjB499UsE6MfvRe5Lfjh4jYL4Co'

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    image_file = request.files['image']
    image_bytes = image_file.read()  # Read bytes for encoding

    # Rewind the file pointer for API request
    image_file.stream.seek(0)

    params = {
        'models': 'genai',
        'api_user': API_USER,
        'api_secret': API_SECRET
    }

    files = {
        'media': image_file
    }

    response = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

    try:
        result = response.json()
        if result['status'] != 'success':
            return jsonify({'error': 'API returned an error'}), 500

        ai_score = result['type']['ai_generated']
        image_url = result['media']['uri']

        # Encode image to base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        return jsonify({
            'ai_generated_score': ai_score,
            'image_url': image_url,  # Still keeping if useful
            'is_ai_generated': ai_score > 0.5,
            'image_base64': base64_image
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
