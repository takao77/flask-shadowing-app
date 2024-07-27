from flask import Flask, render_template, request, jsonify
import requests
import base64
from pydub import AudioSegment
from io import BytesIO

app = Flask(__name__)

# Replace these with your actual API key and endpoint
AZURE_API_KEY = '7f08d064b12e4b3b897eb343f5334d51'
AZURE_TTS_ENDPOINT = 'https://eastus.api.cognitive.microsoft.com/sts/v1.0/issuetoken'
AZURE_TTS_API_URL = 'https://eastus.tts.speech.microsoft.com/cognitiveservices/v1'


def get_access_token():
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_API_KEY,
    }
    response = requests.post(AZURE_TTS_ENDPOINT, headers=headers)
    response.raise_for_status()
    return response.text


def generate_speech(text, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'audio-16khz-32kbitrate-mono-mp3'
    }
    body = f"""
    <speak version='1.0' xml:lang='en-US'>
        <voice xml:lang='en-US' xml:gender='Female' name='en-US-JennyNeural'>
            {text}
        </voice>
    </speak>
    """
    response = requests.post(AZURE_TTS_API_URL, headers=headers, data=body)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
    response.raise_for_status()
    return response.content


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shadow', methods=['POST'])
def shadow():
    text = request.form['text']
    try:
        access_token = get_access_token()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error obtaining access token: {str(e)}'}), 500

    try:
        audio_content = generate_speech(text, access_token)
        combined = AudioSegment.empty()
        for _ in range(5):
            audio_segment = AudioSegment.from_file(BytesIO(audio_content), format="mp3")
            combined += audio_segment

        # Convert the combined audio to base64
        buffered = BytesIO()
        combined.export(buffered, format="mp3")
        audio_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error generating speech: {str(e)}'}), 500

    return jsonify({'audio': audio_base64})


if __name__ == '__main__':
    app.run(debug=True)