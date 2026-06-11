from piper import PiperVoice
import wave
from playback_audio import play_audio
import os
from datetime import datetime

what_to_say = '''
Praise the Lord, O my soul! With all that is within me, praise his holy name! Praise the Lord, O my soul! Do not forget all his kind deeds! He is the one who forgives all your sins, who heals all your diseases, who delivers your life from the Pit, who crowns you with his loyal love and compassion, who satisfies your life with good things, so your youth is renewed like an eagle’s.
'''

def text_chunks():
    yield "This starts speaking quickly. "
    yield "More text can arrive while audio is already playing."

# Try Piper!
CLIENT_ROOT:str = os.path.join(os.getcwd(), "client")
voice_model:str = os.path.join(CLIENT_ROOT, "en_GB-southern_english_female-low.onnx" )
voice_config:str = os.path.join(CLIENT_ROOT, "en_GB-southern_english_female-low.onnx.json")
southern_voice = PiperVoice.load(voice_model, config_path=voice_config)
date = datetime.now()
created_vox_filepath:str = os.path.join(CLIENT_ROOT,f"testing_piper_vox_{date.strftime('%b%d_%H-%M-%S')}.wav")
with wave.open(created_vox_filepath, "wb") as wav_file:
    southern_voice.synthesize_wav(what_to_say, wav_file)

play_audio(created_vox_filepath)

print("TTS stream... DONE")