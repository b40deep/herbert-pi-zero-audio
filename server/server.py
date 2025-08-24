from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import os
import uuid

app = FastAPI()

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
    print("SELF:   WebSocket connection established.")
    try:
        # Generate a unique filename for the received file
        filename = f"received_files/{uuid.uuid4().hex}.wav"
        with open(filename, "wb") as f:
            while True:
                # Receive binary data from the client
                data = await websocket.receive_bytes()
                if not data:
                    break
                f.write(data)
                print(f"SELF:   File received and saved as {filename}")
                await websocket.send_text(f"File saved as {filename}")
    except WebSocketDisconnect as exc:
            print(f"SELF:   WebSocketDisconnect: code={exc.code}, reason='{exc.reason}'")
    except Exception as e:
        print(f"SELF:   Error: {e}")
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        print("SELF:   WebSocket connection closed.")