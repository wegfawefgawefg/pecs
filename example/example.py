import simpleaudio as sa
import wave
import numpy as np
from enum import Enum
from PIL import Image

# Uncomment these lines to make the example work without installing the package
import sys

sys.path.append("../")
from phecs import AssetCache, loader

################    DEFINE YOUR LOADERS    ################


def load_image(path):
    return Image.open(path)


def load_audio(path):
    with wave.open(path, "rb") as wav_file:
        # Extract Audio Frames and parameters
        audio_data = wav_file.readframes(wav_file.getnframes())
        params = {
            "num_channels": wav_file.getnchannels(),
            "bytes_per_sample": wav_file.getsampwidth(),
            "sample_rate": wav_file.getframerate(),
        }
        return (audio_data, params)


################    DEFINE YOUR ASSETS    ################


@loader(load_image, path="assets/images/")
class Images(Enum):
    CHIPS = "chips.png"
    FOOD = "food.png"
    GEAR = "gear.png"


@loader(load_audio, path="assets/audio/")
class Audio(Enum):
    GO = "go.wav"
    AWAY = "away.wav"


################    USE IT    ################


# little utility function to play a sound
def play_audio(audio_data, params):
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    play_obj = sa.play_buffer(audio_array, **params)
    play_obj.wait_done()


assets = AssetCache()
assets.preload([Images.CHIPS, Audio.AWAY])

image_asset = assets.get(Images.FOOD)
image_asset.show()

sound_asset, sound_params = assets.get(Audio.GO)
play_audio(sound_asset, sound_params)


print("clearing cache...")
assets.clear_cache()
