import json
import pyaudio
import webbrowser
import subprocess
import pyttsx3
from vosk import Model, KaldiRecognizer
from datetime import datetime

model = Model('model_en')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.setProperty('voice', 'english')
    engine.say(text)
    engine.runAndWait()

def listen():
    partial_text = ''
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = rec.Result()
            if len(result) > 0:
                answer = json.loads(result)
                if 'partial' in answer:
                    partial_text = answer['partial']
                if 'text' in answer:
                    yield partial_text + answer['text']
                    partial_text = ''

for text in listen():
    text = text.lower()
    print(text)
    if 'стоп' in text or 'зупинись' in text or 'stop' in text:
        speak('Work finished.')
        break
    if 'время' in text or 'час' in text or 'time' in text:
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        print("Today's date:", time)
        speak('Time at the moment ' + time)
    if 'браузер' in text or 'browser' in text:
        speak('Browser open.')
        webbrowser.open('https://www.google.com/')
    if 'провідник' in text or 'explorer' in text:
        speak('Explorer open')
        subprocess.Popen('explorer')
