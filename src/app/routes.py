from app import app
from app.models.stt import SpeechToText
from app.models.tts import textToSpeech
import os
from flask import Response, request, send_file
from app.config import application_name


# Todo in memory file object!
@app.route('/', methods=['GET'])
def home():
    return f"<body><h1>API of {application_name}</h1></body>"


@app.route('/classify_audio', methods=['POST', "PUT"])
def post_recording():
    try:
        # f = request.files
        audio_file = request.get_data()
        with open("audio.wav", 'wb') as file:
            file.write(audio_file)
        file_path = os.path.abspath("audio.wav")
        stt = SpeechToText()
        text = stt.classify_wav(path=file_path)
        return Response(text, 202)
    # To do  test what exceptions to actually catch
    except Exception as e:
        return Response(e, 418)

@app.route('/create_audio', methods=["POST", "PUT"])
def create_audio_from_text():
    try:    
        text = request.form.get("text")
        tts = textToSpeech()
        audio_path = tts.create_wav(text)
        return send_file(
            audio_path, mimetype='audio/wav', as_attachment=True, attachment_filename="boy.wav"
        )
    except Exception as e:
        return Response(e, 418)
