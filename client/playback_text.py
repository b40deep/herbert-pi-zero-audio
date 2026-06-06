from RealtimeTTS import TextToAudioStream, SystemEngine

def text_chunks():
    yield "This starts speaking quickly. "
    yield "More text can arrive while audio is already playing."


if __name__ == "__main__":
    # Initialize the TTS engine
    tts_engine = SystemEngine() # 
    # tts_engine = CoquiEngine() # downloading a 1.8GB model - might fail on Pi Zero due to memory constraints, but let's see. Failed: needs torchaudio

    # Create a TextToAudioStream instance
    tts_stream = TextToAudioStream(tts_engine)

    # Example text to convert to audio
    text = "Hello, this is a test of the real-time text-to-audio streaming system from RealtimeTTS."

    # Start streaming the audio generated from the text
    print("TTS stream... START")
    tts_stream.feed(text)
    # tts_stream.feed(list(text_chunks()))
    tts_stream.play(fast_sentence_fragment=True)  # Play asynchronously so we can feed more text while it's playing
    tts_stream.stop()
    print("TTS stream... DONE")    
    
    
    text = "can it continue on and create for these words?"
    tts_stream.feed(text)
    # tts_stream.feed(list(text_chunks()))
    tts_stream.play(fast_sentence_fragment=True)  # Play asynchronously so we can feed more text while it's playing
    print("TTS stream... DONE")