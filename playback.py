import pyaudio
import wave

def play_audio(audio_path):
    """Play a WAV audio file."""
    try:
        wf = wave.open(audio_path, 'rb')

        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        print(f"▶️ Playing '{audio_path}'...")

        chunk = 1024
        data = wf.readframes(chunk)

        while data:
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()

        print("✅ Playback complete.")

    except Exception as e:
        print(f"❌ Could not play audio: {e}")


# 🎧 Example Usage
if __name__ == "__main__":
    audio_path = "voicehat_recording.wav"
    play_audio(audio_path)

