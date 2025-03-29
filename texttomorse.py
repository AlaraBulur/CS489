import numpy as np
import io
import wave

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ' ': '/',  '.':'.-.-.-', ',':'--..--',
    '!': '-.-.--', '?': '..--..', '\'': '.----.'
}

def text_to_morse(text):
    text = text.upper()  # Convert to uppercase
    morse_code = []

    for char in text:
        if char == ' ':
            morse_code.append('/')  # Separate words by '/'
        elif char in MORSE_CODE_DICT:
            morse_code.append(MORSE_CODE_DICT[char])
    
    return ' '.join(morse_code)

def generate_silence(duration):
    # Generate silence (zero amplitude) for the given duration
    sample_rate = 44100
    silence = np.zeros(int(sample_rate * duration), dtype=np.int16)
    return silence

def generate_audio(morse_code):
    """Generate and return an audio stream for Morse code."""
    sample_rate = 44100  # Samples per second (standard audio sample rate)
    freq = 800  # Frequency of the beep sound in Hz
    duration_dot = 0.1  # Duration of a dot in seconds
    duration_dash = 0.3 # Duration of a dash in seconds
    silence = 0.1 # Duration of silence betweens dots, dashes, or words
    amplitude = 4096  # Amplitude of the sound

    # Create a waveform for the beep sound (sine wave)
    def generate_waveform(duration, freq):
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        waveform = amplitude * np.sin(2 * np.pi * freq * t)
        return waveform.astype(np.int16)

    # Initialize an empty list to store audio data
    audio_data = []

    # Convert Morse code to sound
    for symbol in morse_code:
        if symbol == '.':
            # Add the waveform for a dot
            audio_data.append(generate_waveform(duration_dot, freq))
            audio_data.append(generate_silence(silence*2))
        elif symbol == '-':
            # Add the waveform for a dash
            audio_data.append(generate_waveform(duration_dash, freq))
            audio_data.append(generate_silence(silence))
        elif symbol == ' ':
            audio_data.append(generate_silence(silence*2))
        elif symbol == '/':
            audio_data.append(generate_silence(silence * 4))

    # Concatenate all the waveforms into one continuous waveform
    full_audio = np.concatenate(audio_data)

    # Save the audio to a memory buffer using the wave module
    audio_stream = io.BytesIO()
    with wave.open(audio_stream, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono sound
        wav_file.setsampwidth(2)  # Sample width in bytes (2 bytes for 16-bit PCM)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(full_audio.tobytes())

    # Move the pointer back to the start of the audio stream
    audio_stream.seek(0)

    return audio_stream