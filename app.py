# app.py

import ollama
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io
import torch
from TTS.api import TTS

device = "cuda" if torch.cuda.is_available() else "cpu"
app = Flask(__name__)
CORS(app)

print("Initializing Coqui Text-to-Speech engine...")
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC").to(device)
print("TTS engine ready.")


@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles chat requests.
    FOR NOW: Returns a FAKE response to test TTS without crashing Ollama.
    """
    # --- TEMPORARY CHANGE ---
    # We are commenting out the call to the AI model to save resources.
    # try:
    #     user_message = request.json['message']
    #     stream = ollama.chat(
    #         model='phi3:mini',
    #         messages=[{'role': 'user', 'content': user_message}],
    #         stream=True
    #     )
    #     full_response = ""
    #     for chunk in stream:
    #         full_response += chunk['message']['content']
    #     return jsonify({"response": full_response})
    # except Exception as e:
    #     print(f"Error during chat: {e}")
    #     return jsonify({"error": "Failed to get a response from the model"}), 500
    
    # Instead, we send back a fixed, simple response.
    mock_response = "Hello! I am now testing my voice."
    return jsonify({"response": mock_response})
    # --- END OF TEMPORARY CHANGE ---


@app.route('/synthesize-speech', methods=['POST'])
def synthesize_speech():
    # This function remains the same
    text_to_speak = request.json['text']
    if not text_to_speak:
        return jsonify({"error": "Text cannot be empty"}), 400
    try:
        audio_buffer = io.BytesIO()
        tts.tts_to_file(text=text_to_speak, file_path=audio_buffer)
        audio_buffer.seek(0)
        return send_file(audio_buffer, mimetype='audio/wav', as_attachment=False)
    except Exception as e:
        print(f"Error during speech synthesis: {e}")
        return jsonify({"error": "Failed to synthesize speech"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)