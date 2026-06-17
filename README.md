# pi zero audio 
currently called Jambula.
formerly called Commando, Herbert

## sound options
this is I think the biggest nag on this whole project. I have found 3 options so far:
+ i2s amp [what i'm using currently - the max98357a]
  - has startup pops, and pops at the start and end of playback. it's annoying enough to not be practical.
+ simple filter circuit & pam8493 amp 
  - similar to the i2s version, but worse audio overall. I'd built this some time ago.
+ dac board & 8403
  - seen a [guy](https://www.youtube.com/watch?v=7BXO9UfTfYI) do this and thought i'd save money by using cheaper alternatives, but I might end up having to do this.

review each option's resultant sound issues.

## pi setup
- if using the full-fat raspbian which comes with GUI, then enable VNC:
  - `ssh username@IPAdress` 
  - then `sudo raspi-config` > interface options > enable VNC > finish
- increase swap:
  - depending on your OS, you'll need to do something different. see [here](https://pimylifeup.com/raspberry-pi-swap-file/) for details.
- disable wifi power-saving which is [enabled by default](https://raspberrypi.stackexchange.com/questions/96606/make-iw-wlan0-set-power-save-off-permanent)
  - ``` bash
    $ sudo crontab -e
    # which opens the root crontab in your chosen editor...
    # add the following line at the bottom of the root crontab:
    @reboot /usr/sbin/iw wlan0 set power_save off > /home/<user>/power_save_log.txt 2>&1
    # be sure to substitute a valid folder name for '<user>' in the line above
    ```

## git setup
- vscode won't work so we'll have to pull the code updates manually via terminal rather than a simple button in vscode.
- to set up git and github (gh):
  - `sudo apt install git -y` if it's not already on
  - then `git config --global user.name "raspbelly"`
  - then `git config --global user.email "raspbelly@belly.bell"`
  - then `ssh-keygen -t ed25519 -C "raspbelly@belly.bell"`
  - then `cat ~/.ssh/id_ed25519.pub`
  - then go to `https://github.com/settings/keys` and create a new SSH key. Paste in the public key including the `ssh-ed25519 ` prefix. 
  - then you're good to go. [ref](https://medium.com/@thedyslexiccoder/installing-github-on-a-raspberry-pi-4-44a1ca04a558)
- go to the herbert repo
  - `cd Desktop` then clone it if you don't have it. `git clone https://github.com/b40deep/herbert-pi-zero-audio.git`
  - then `cd herbert-pi-zero-audio/`
  - then pull the latest changes whenever you push them from another device
  - `git pull`
  - then done.
- For first time, do the setup by following this README.
  - set up both the client and the server.
  - then run the server [first, so models can load], and then the client.
  - then done.
- to push new code, do:
	- `git add .`
	- `git commit -m "message"`
	- `git push`

## repo setup:
- setup the venv `python -m venv .venv`
- activate the venv if you're using SSH / not using vscode `source venv/bin/activate`
- client requirements:
  - for raspbelly pie, PyAudio is tricky sometimes because it has to build wheels which fail if deps aren't available. try installing this first OUTSIDE of the venv `sudo apt-get install portaudio19-dev`. You might also need `libportaudio2` and `espeak-ng`. But start with portaudio alone.
  - then you can install pyaudio properly `pip install pyaudio`.
  - do `pip install -r client_requirements.txt` for client (and for server too, if you're testing both).
- server requirements:
  - do `pip install -r server_requirements.txt` for server.

## usage:
- `check_sample_rate.py` checks the sample rate that the microphone you have can record at. so that when you record with `class_record_test.py`, you can specify a sample rate that works within that code.
- `class_record_test.py` records 5 seconds of audio. currently it saves the file as `voicehat_recording.wav`
- `playback.py` plays back that audio. you can change the name of the file in both `class_record_test.py` and `playback.py`.


#### for development:
- Update: `python ./server/server.py` to load the server. I've passed all the parameters (reload, host, and port) inside the code itself.
  - [old] to listen widely, we'll use `uvicorn server.server:app --reload --host 0.0.0.0 --port 8000`
- `python ./client/upload.py` to test uploading from the client to the server

## todo:
get audio from mic:
- button press to record audio 
  - added to `client/main_record_upload.py` not yet tested until I solder on the btn and led.
- ✅ `v1` record audio to local file

send audio to server:
- ✅ `v2` set up a backend server
- ✅ `v2` stream input audio to the server [fastapi]
- ✅ `v2` save the sent audio on the server 

get audio response from server:
- get back response when server sends it
- save the response to local file
- ✅ `v1` play audio response
- alternative: use TTS engine on the Zero2W to play text sent from the server.
  - i've created `client/playback_text.py` to do that using SystemEngine (apprnly espeak on Linux). 
  - need to first solder on the DAC/AMP and then will test this.

