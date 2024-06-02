import json, pyaudio, webbrowser, subprocess, pyttsx3
from vosk import Model, KaldiRecognizer
from datetime import datetime
 

model = Model('model_en')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()

stream = p.open(format = pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
stream.start_stream()

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.setProperty('voice', 'english-us')
    engine.say(text)
    engine.runAndWait()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']


for text in listen():
    if'стоп' in text or 'зупинись' in text or 'stop' in text:
        speak('Work finished.')
        break
    if 'время' in text or 'час' in text or 'time' in text:
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        print("Time:", time)
        speak('Time at the moment' + time)
    print(text)
    if 'браузер' in text or 'browser' in text:
        speak('Browser open.')
        webbrowser.open('https://www.google.com/')
    if 'провідник' in text or 'explorer' in text:
        speak('Explorer open')
        subprocess.Popen('explorer')

print(text)