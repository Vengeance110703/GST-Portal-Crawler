import whisper
from os import path

audio_folder_name = "audio"
# download_dir = os.getcwd()

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "audiocaptcha.mp3")

print(AUDIO_FILE)

model = whisper.load_model("tiny")
result = model.transcribe(AUDIO_FILE)

print(result["text"])