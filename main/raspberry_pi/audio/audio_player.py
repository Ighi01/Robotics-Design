import os
import audioio

class AudioPlayer:
    def __init__(self, audio_pin):
        self.audio_pin = audio_pin
        self.audio_pin.switch_to_output(value=False)
        self.audio = audioio.AudioOut(audio_pin)
        self.audio_wavefile = None
        self.volume = 1.0

    def play_audio(self, filename, volume=None):
        try:
            if volume is not None:
                self.volume = volume
            audio_path = os.path.join(os.path.dirname(__file__), "audio", filename)
            with open(audio_path, "rb") as mp3_file:
                self.audio_wavefile = audioio.MP3Decoder(mp3_file)
                self.audio.play(self.audio_wavefile, volume=self.volume)
                while self.audio.playing:
                    pass
        except:
            print("Error: Could not play audio file.")
