import requests
import os
import httpx
import asyncio

FILENAME = "testaudio.wav"
SERVER_URL = 'http://localhost:8000'


print(requests.get(f"{SERVER_URL}/").json())

print(requests.get(f"{SERVER_URL}/job123abc").json())

async def send_wav_file() -> bool:
    if not os.path.exists(FILENAME):
        print(f"CLIENT:   File {FILENAME} not found.")
        return True

    # an HTTP client context manager
    async with httpx.AsyncClient() as client:
        print("CLIENT:   HTTP client initialized.")

        # open file for streaming multipart upload
        with open(FILENAME, "rb") as f:
            # httpx handles chunked streaming automatically when passed a file object
            files = {"file": (os.path.basename(FILENAME), f, "audio/wav")}
            response = await client.post(SERVER_URL, files=files)

        print("CLIENT:   File sent.")

        # receive single HTTP response instead of looped websocket.recv acks
        try:
            if response.status_code == 200:
                ack = response.json()
                print(f"SERVER:   {ack}")
                
                # inspect JSON body for server-side success/failure
                if ack.get("status") == "success": # change to Enum later
                    print("CLIENT:   Finished sending file.")
                    return True
                else:
                    print("CLIENT:   Server reported failure.")
                    return False
            else:
                print(f"CLIENT:   HTTP error {response.status_code}: {response.text}")
                return False
        except Exception as exc:
            print(f"CLIENT:   Failed to read response: {exc}")
            return False
    
asyncio.run(send_wav_file())