from flask import Response, request, send_file

from app import app, controller
from app.config import application_name


# Todo in memory file object!
@app.route('/', methods=['GET'])
def home():
    return f"<body><h1>API of {application_name}</h1></body>"


@app.route('/recognize_audio_disk', methods=['POST'])
def post_recording_disk():
    try:
        audio_file = request.get_data()
        text = controller.stt_recognize_binary_audio_on_disk(audio_file)
        return Response(text, 202)
    # To do  test what exceptions to actually catch
    except Exception as e:
        print(e)
        return Response(e, 418)


@app.route('/recognize_audio_memory', methods=['POST'])
def post_recording_memory():
    try:
        audio_file = request.get_data()
        text = controller.stt_recognize_binary_audio_in_memory(audio_file)
        return Response(text, 202)
    # To do  test what exceptions to actually catch
    except Exception as e:
        print(e)
        return Response(e, 418)


@app.route('/create_audio', methods=["POST"])
def create_audio_from_text():
    try:
        text = request.form.get("text")
        audio_path = controller.tts_create_audio_from_text(text)
        return send_file(
            audio_path, mimetype='audio/wav', as_attachment=True, attachment_filename="boy.wav"
        )
    # To do  test what exceptions to actually catch
    except Exception as e:
        print(e)
        return Response(e, 418)
