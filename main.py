from flask import Flask, request, jsonify,send_file,send_from_directory,make_response
from flask_cors import CORS
from pytube import YouTube
import os
import json


app = Flask(__name__)
CORS(app)

PASSWORD = 'anmalima601262'

video_resolutions = {}
audio_resolutions = {}


@app.route('/')
def inicio():
    return 'Bienvenido'

@app.route('/descargar', methods=['POST'])
def descargar():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header == 'Bearer anmalima601262':
        data = request.json
        link = data.get('texto')
        itag = data.get('itag')
        print(f"Link recibido: {link}")
        print(f"ITAG recibido: {itag}")
        yt = YouTube(link)
        video = yt.streams.get_by_itag(itag)

        if video.includes_audio_track:
            print("El video contiene audio")
            download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            file_path = os.path.join(download_path, video.default_filename)
            # Descargar el archivo de video
            video.download(download_path)
            print('Descargado')
            response = send_file(file_path, as_attachment=True)
            return response
        else:
            return jsonify({'message': 'El video no contiene audio'})
    else:
        return jsonify({'message': 'No autorizado'})


if __name__ == '__main__':
   app.run(debug=True, port=os.getenv("PORT", default=5000))
