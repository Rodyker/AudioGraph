import array
import os
import sys
import threading
import pyaudio

sys.stderr.flush()
devnull = os.open(os.devnull, os.O_WRONLY)
os.dup2(devnull, sys.stderr.fileno())

class Output:
    def __init__(self, repeat, flip_x= False, flip_y= False, flip_x_y= False):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                    channels=2,
                                    rate=44100,
                                    output=True)
        
        self.stop_flag = False

        self.sound = []
        self.wave_out = array.array('f', [0, 0]).tobytes()

        self.repeat = repeat
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.flip_x_y = flip_x_y

        self.audio_player = threading.Thread(target=self.output)
        self.audio_player.start()

        self.capture_thread = threading.Thread(target=self.capture)
        self.capture_thread.start()

    def capture(self):
        while not self.stop_flag:
            if input() == 'q':
                self.stop_flag = True
                continue
            i = 0
            while os.path.exists("saves/save%s.raw" % i):
                i += 1
            print(i)
            if not os.path.exists("saves"):
                os.makedirs("saves")
            fh = open("saves/save%s.raw" % i, "wb")
            fh.write(self.wave_out)
            fh.close()
            continue

    def output(self):
        while not self.stop_flag:
            self.stream.write(self.wave_out)

    def sound_set(self, sound):
        self.sound = sound

    def sound_clear(self):
        self.sound = []

    def sound_append(self, x, y):
        if self.flip_x_y:
            x, y = y, x
        for _ in range(self.repeat):
            self.sound.append((-1 if self.flip_x else 1) * x)
            self.sound.append((-1 if self.flip_y else 1) * y)

    def update_wave(self):
        self.wave_out = (array.array('f', self.sound)).tobytes()

    def close(self):
        self.stop_flag = True
        self.audio_player.join()
        self.capture_thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()