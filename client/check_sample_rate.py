import pyaudio
p = pyaudio.PyAudio()
device_index = 1  # Adjust if needed

for rate in [8000, 11025, 16000, 22050, 44100, 48000]:
    try:
        if p.is_format_supported(rate,
            input_device=device_index,
            input_channels=1,
            input_format=pyaudio.paInt16):
            print(f"✅ {rate} Hz supported")
        else:
            print(f"❌ {rate} Hz not supported")
    except:
        print(f"⚠️ {rate} Hz caused an exception")
p.terminate()

