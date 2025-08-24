# pi zero audio

## setup:
- setup the venv `python -m venv .venv`
- install `client_requirements.txt` for client, `server_requirements.txt` for server, and both if you're testing.

## usage:
- `check_sample_rate.py` checks the sample rate that the microphone you have can record at. so that when you record with `class_record_test.py`, you can specify a sample rate that works within that code.
- `class_record_test.py` records 5 seconds of audio. currently it saves the file as `voicehat_recording.wav`
- `playback.py` plays back that audio. you can change the name of the file in both `class_record_test.py` and `playback.py`.


#### for development:
- `uvicorn server.server:app --reload` to load the server
- `python ./client/upload.py` to test uploading to the server

## todo:
get audio from mic:
- button press to record audio
- ✅ `v1` record audio to local file

send audio to server:
- ✅ `v2` set up a backend server
- ✅ `v2` stream input audio to the server [fastapi]
- ✅ `v2` save the sent audio on the server 

get audio response from server:
- get back response when server sends it
- save the response to local file
- ✅ `v1` play audio response
