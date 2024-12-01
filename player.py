import os
import sys
import pyaudio

sys.stderr.flush()
devnull = os.open(os.devnull, os.O_WRONLY)
os.dup2(devnull, sys.stderr.fileno())

with open("saves/save" + input() + ".raw", 'rb') as f:
    data = f.read()

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=2,
                rate=44100,
                output=True)

try:
    while True:
        stream.write(data)
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    