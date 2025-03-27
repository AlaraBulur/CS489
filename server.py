from flask import Flask, request, render_template, jsonify, send_file
import os
import texttomorse
import time

app = Flask(__name__)

audio_directory = os.path.join(os.getcwd(), 'static', 'audio')
if not os.path.exists(audio_directory):
    os.makedirs(audio_directory)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert_to_morse():
    input_text = request.form['text']  # Get the text input from the form
    # Convert text to Morse code
    morse_code = texttomorse.text_to_morse(input_text)
    
    # Generate the audio for the Morse code
    audio_stream = texttomorse.generate_audio(morse_code)
    
    timestamp = int(time.time() * 1000)  # Current time in milliseconds
    audio_filename = f"morse_{timestamp}.wav"
    # Save the audio to a specific location (e.g., 'static/audio')
    audio_filepath = os.path.join(audio_directory, audio_filename)

    with open(audio_filepath, 'wb') as f:
        f.write(audio_stream.read())  # Save audio to the file

    # Return the audio file URL
    return jsonify({
        'morse_code': morse_code,
        'audio_url': f'/audio/{audio_filename}'  # Path to access the audio file via Flask
    })

# Serve audio files from the '/audio' path
@app.route('/audio/<filename>')
def serve_audio(filename):
    audio_path = os.path.join(audio_directory, filename)
    if os.path.exists(audio_path):
        return send_file(audio_path, mimetype='audio/wav')
    else:
        return "Audio file not found", 404

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=8000)
