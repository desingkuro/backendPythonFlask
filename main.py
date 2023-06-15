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

def recibir():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header == 'Bearer anmalima601262':
        if request.method == 'POST':
            link = request.form['texto']
            yt = YouTube(link)
            video_resolutions = {}
            audio_resolutions = {}
            streams = yt.streams
            print('entro')
            for stream in streams:
                if 'mp4' in stream.mime_type:
                    if stream.type == 'video':
                        if stream.resolution not in video_resolutions:
                            video_resolutions[stream.resolution] = stream.mime_type
                    elif stream.type == 'audio':
                        if stream.abr not in audio_resolutions:
                            audio_resolutions[stream.abr] = stream.mime_type
            result = {
                'video': video_resolutions,
                'audio': audio_resolutions
            }
            return jsonify(result)
        else:
            return jsonify({'message': 'false'})
    else:
        return jsonify({'message': 'no autorizado'})

@app.route('/link', methods=['POST', 'GET'])
def link():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header == 'Bearer anmalima601262':
        if request.method == 'POST':
            texto = request.form['texto']
            print('Recibido: ' + texto)
            yt = YouTube(texto)
            audio = yt.streams.filter(only_audio=True).first()
            download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            file_path = os.path.join(download_path, audio.default_filename)
            print('Descargando')
            # Descargar el archivo de audio
            audio.download(download_path)
            print('Descargado')

            # descarga el 
            response = send_file(file_path, as_attachment=True)

            return response
        else:
            return 'No se envió nada'
    else:
        return 'Acceso no autorizado', 401

from flask import jsonify, send_file, make_response

from flask import jsonify, send_file, make_response
import os

@app.route('/descargar', methods=['POST'])
def descargar():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header == 'Bearer anmalima601262':
        data = request.json
        link = data.get('texto')
        itag = data.get('itag')
        yt = YouTube(link)
        stream = yt.streams.get_by_itag(itag)
        
        # Descargar el archivo y establecer el encabezado Content-Disposition
        file_path = f'descarga.{stream.subtype}'
        response = make_response(send_file(stream.url))
        filename = os.path.basename(file_path)
        response.headers.set('Content-Disposition', 'attachment', filename=filename)
        return response
    else:
        return jsonify({'message': 'no autorizado'})





if __name__ == '__main__':
    app.run(debug=True, port=5600)
