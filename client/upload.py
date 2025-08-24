import requests,os
import asyncio
import websockets
import os

# Ensure the server is running at http://localhost:8000
SERVER_URL:str = "ws://localhost:8000/ws"

# Set base path to directory of this script
BASE_PATH:str = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_PATH)

# File to upload (must be in the same directory as this script)
FILENAME:str = "voicehat_recording.wav"

def upload_file(audio_file_path:str) -> str:
    """Uploads an audio file to the server and returns the server's response."""
    with open(audio_file_path, "rb") as f:
        files = {"file": f}
        response:requests.Response = requests.post(SERVER_URL, files=files)
        print("SERVER:   Server response:", response.text)
    return response.text

async def send_wav_file():
    if not os.path.exists(FILENAME):
        print(f"SELF:   File {FILENAME} not found.")
        return

    async with websockets.connect(SERVER_URL) as websocket:
        print("SELF:   Connected to server.")
        with open(FILENAME, "rb") as f:
            while True:
                chunk = f.read(64 * 1024)  # Read in 64KB chunks
                if not chunk:
                    break
                await websocket.send(chunk)
                print("SELF:   File sent.")
                try:
                    ack = await websocket.recv()
                    print(f"SERVER:   {ack}")
                except Exception:
                    pass
        print("SELF:   Finished sending file. Closing connection.")
        # await websocket.close()


if __name__ == "__main__":
    print(f"TEST: Uploading {FILENAME} \n\tfrom {BASE_PATH} \n\tto server {SERVER_URL}")
    # upload_file(FILENAME)
    asyncio.run(send_wav_file())