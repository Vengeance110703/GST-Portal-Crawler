import whisper
from os import path

# AUDIO_FILE_1 = path.join(path.dirname(path.realpath(__file__)), "audiocaptcha.mp3")
# AUDIO_FILE_2 = path.join(path.dirname(path.realpath(__file__)), "audiocaptcha (1).mp3")
# AUDIO_FILE_3 = path.join(path.dirname(path.realpath(__file__)), "audiocaptcha (2).mp3")
# AUDIO_FILE_4 = path.join(path.dirname(path.realpath(__file__)), "audiocaptcha (3).mp3")

# model = whisper.load_model("base.en")
# result_1 = model.transcribe(AUDIO_FILE_1)
# result_2 = model.transcribe(AUDIO_FILE_2)
# result_3 = model.transcribe(AUDIO_FILE_3)
# result_4 = model.transcribe(AUDIO_FILE_4)

# print(result_1["text"])
# print(result_2["text"])
# print(result_3["text"])
# print(result_4["text"])

captcha = "A1 3 1 3 0"
captcha = captcha.replace(" ", "")
captcha = captcha.replace(",", "")
if not captcha.isalnum():
    print(captcha)
