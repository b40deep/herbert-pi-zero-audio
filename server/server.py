from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import os
import uuid
import nemo.collections.asr as nemo_asr


app = FastAPI()

# Might move this class back to stt.py later, since uvicorn reloads the server on code changes and we don't want to reload the model every time. For now, it's here for simplicity.
class STTServer:
    def __init__(self):
        self.model = nemo_asr.models.ASRModel.from_pretrained(
            model_name="nvidia/parakeet-tdt-0.6b-v3"
        )

    def get_text_from_audio(self, path:str)->str:
        output = self.model.transcribe([path])
        if isinstance(output, list) and len(output) > 0:
            if hasattr(output[0], 'text'):
                return output[0].text
            return output[0]
        return "Error. Transcription failed."

# Initialize the model globally
stt_service = STTServer()

# Set base path to directory of this script
BASE_PATH:str = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_PATH)

# Create a directory to store received files
os.makedirs("received_files", exist_ok=True)

@app.get("/")
async def get():
    return HTMLResponse("<h1>WebSocket Audio Server</h1>")

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     await websocket.send_text("Hello from server")
#     await websocket.close()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("SERVER:   WebSocket connection established.")
    # Generate a unique filename for the received file
    filepath = f"received_files/{uuid.uuid4().hex}.wav"
    f = open(filepath, "wb")
    try:
        while True:
            data = await websocket.receive_bytes()
            f.write(data)
            print(f"SERVER:   Received chunk for {filepath}")
            await websocket.send_text("Chunk received")

    except WebSocketDisconnect as exc:
        print("SERVER:   Client finished sending file.")
        # 👉 File is fully transferred here — process it now
        intent:str = stt_service.get_text_from_audio(filepath)
        print(f"SERVER:   Transcription result: '{intent}'")
        print(f"SERVER:   WebSocketDisconnect: code={exc.code}, reason='{exc.reason}'")
    except Exception as e:
        print(f"SERVER:   Error: {e}")
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        print("SERVER:   WebSocket connection closed.")