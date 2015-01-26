__author__ = 'brad'
import pyaudio
import wave


class SoundStream():
    def __init__(self, address):
        self.file = wave.open(str(address), 'rb')
        self.pya = pyaudio.PyAudio()
        self.stream = None
        self.streaming = False
        self.address = address
        self.chunk = 1024
        self.channels = 2
        self.silence = chr(0)*self.chunk*self.channels*2

    def callback(self, in_data, frame_count, time_info, status):
        data = self.file.readframes(frame_count)
        if data == "":
            data = self.silence
        return data, pyaudio.paContinue

    def play(self):
        self.file = wave.open(str(self.address), 'rb')
        self.stream = self.pya.open(format=self.pya.get_format_from_width(self.file.getsampwidth()),
                                    channels=self.file.getnchannels(),
                                    rate=self.file.getframerate(),
                                    output=True,
                                    stream_callback=self.callback)
        self.stream.start_stream()
        self.streaming = True

    def stop(self):
        self.streaming = False
        self.stream.stop_stream()
        self.stream.close()

    def update(self):
        if self.streaming:
            if not self.stream.is_active():
                self.stream.close()
                self.play()

    # def write(self):
    #     if self.data == '':
    #         self.destroy()
    #     else:
    #         self.stream.write(self.data)
    #         self.data = self.file.readframes(self.chunk)

    def destroy(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pya.terminate()
        # sounds.remove(self)