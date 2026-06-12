import pyaudio
import wave
import sys
import numpy as np
from datetime import datetime
import os
from gpiozero import Button, LED
from signal import pause


BUTTON_PIN = 17
LED_PIN = 27

button = Button(BUTTON_PIN, pull_up=True, hold_time=0.1)
led = LED(LED_PIN)

class AudioRecorder:
    def __init__(self,
                 sample_rate=16000,
                 channels=1,
                 chunk=2048,
                 record_seconds=5,
                 format=pyaudio.paInt16,
                 device_index=None,
                 filename="voicehat_recording.wav",
                 rec_folder=os.path.join(os.getcwd(),"rec")):

        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk = chunk
        self.record_seconds = record_seconds
        self.format = format
        self.device_index = device_index
        self.filename = filename
        self.rec_folder = rec_folder

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []

    def list_input_devices(self):
        print("🎛️ Available input devices:")
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            if info["maxInputChannels"] > 0:
                print(f"  [{i}] {info['name']}")

    def is_device_supported(self, device_index):
        try:
            return self.audio.is_format_supported(
                rate=self.sample_rate,
                input_device=device_index,
                input_channels=self.channels,
                input_format=self.format
            )
        except ValueError:
            return False

    def select_supported_device(self):
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            if info["maxInputChannels"] > 0 and self.is_device_supported(i):
                self.device_index = i
                print(f"✅ Auto-selected device [{i}] '{info['name']}'")
                return True
        print("❌ No supported input device found.")
        return False

    def open_stream(self):
        try:
            self.stream = self.audio.open(format=self.format,
                                          channels=self.channels,
                                          rate=self.sample_rate,
                                          input=True,
                                          frames_per_buffer=self.chunk,
                                          input_device_index=self.device_index)
        except Exception as e:
            print(f"🚫 Could not open audio stream: {e}")
            self.cleanup()
            sys.exit(1)

    def record_until_button_released(self, button):
        print("🎙️ Recording… (release button to stop)")
        self.frames = []

        try:
            while button.is_pressed:
                data = self.stream.read(self.chunk, exception_on_overflow=False)
                self.frames.append(data)

        except Exception as e:
            print(f"⚠️ Error during recording: {e}")
            self.cleanup()
            sys.exit(1)

    print("🛑 Recording stopped.")

    def apply_gain(self, gain=1.5):
        print(f"🔊 Applying gain: {gain}x")
        try:
            # Convert raw bytes to int16
            audio_data = np.frombuffer(b''.join(self.frames), dtype=np.int16)

            # Compute and display original RMS
            original_rms = np.sqrt(np.mean(audio_data.astype(np.float32) ** 2))
            print(f"📉 Original RMS: {original_rms:.2f}")

            # Apply gain and clip
            amplified = np.clip(audio_data * gain, -32768, 32767).astype(np.int16)

            # Compute and display amplified RMS
            amplified_rms = np.sqrt(np.mean(amplified.astype(np.float32) ** 2))
            print(f"📈 Amplified RMS: {amplified_rms:.2f}")

            # Store amplified audio back in frames
            self.frames = [amplified.tobytes()]
        except Exception as e:
            print(f"❌ Failed to apply gain: {e}")

    def save_to_file(self):
        date = datetime.now()
        self.filename:str = os.path.join(self.rec_folder,f"vox_{date.strftime('%Y%b%d_%H-%M-%S')}.wav")
        try:
            with wave.open(self.filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(self.frames))
            print(f"💾 Audio saved to {self.filename}")
            print(f"📁 File '{self.filename}' saved with {self.channels} channel(s), "
                  f"{self.sample_rate}Hz, {self.record_seconds}s duration.")
        except Exception as e:
            print(f"❌ Failed to save audio: {e}")
            sys.exit(1)

    def cleanup(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()


# 🔧 Usage Example
if __name__ == "__main__":
    recorder = AudioRecorder()

    recorder.list_input_devices()
    if recorder.device_index is None:
        if not recorder.select_supported_device():
            print("No supported audio input device found. Exiting.")
            sys.exit(1)

    recorder.open_stream()
    
    def start_recording():
        print("🎙️ Recording started")
        led.on()
        recorder.record_until_button_released(button)

    def stop_recording():
        print("🛑 Button released — stopping")
        led.off()
        recorder.apply_gain(4.0)
        recorder.save_to_file()
        print("Ready for next recording…")

    button.when_pressed = start_recording
    button.when_released = stop_recording

    print("Hold button to record…")
    pause()  # keeps program alive
    

