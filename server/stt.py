import nemo.collections.asr as nemo_asr

class STTServer:
    def __init__(self):
        self.model = nemo_asr.models.ASRModel.from_pretrained(
            model_name="nvidia/parakeet-tdt-0.6b-v3"
        )

    def transcribe(self, path):
        output = self.model.transcribe([path])
        return output[0].text

stt = STTServer()
print(stt.transcribe("server/2086-149220-0033.wav"))
