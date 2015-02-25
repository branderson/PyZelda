__author__ = 'brad'
import pyaudio
import wave


class SoundStream():
    def __init__(self, pya, address=None):
        if address is not None:
            self.file = wave.open(str(address), 'rb')
        else:
            self.file = None
        self.pya = pya
        self.stream = None
        self.streaming = False
        self.address = address
        self.chunk = 1024
        self.channels = 2
        self.silence = chr(0)*self.chunk*self.channels*2

    def callback(self, in_data, frame_count, time_info, status):
        initial_pos = self.file.tell()
        data = self.file.readframes(frame_count)
        # if self.file.tell() == initial_pos:
        #     self.destroy()
        #     return False
        # if self.file.tell() == initial_pos:
        #     print("Destroying")
        #     self.destroy()
        # if len(data) != frame_count:
        #     print("Problem")
        #     return self.silence, pyaudio.paContinue
        if data == "":
            data = self.silence
            # return data, pyaudio.paComplete
        return data, pyaudio.paContinue

    def play(self, filename=None):
        if filename is not None:
            self.address = filename
            if self.stream is not None:
                self.stream.close()
        if self.address is not None:
            self.file = wave.open(str(self.address), 'rb')
            self.stream = self.pya.open(format=self.pya.get_format_from_width(self.file.getsampwidth()),
                                        channels=self.file.getnchannels(),
                                        rate=self.file.getframerate(),
                                        output=True,
                                        stream_callback=self.callback)
            # self.stream.start_stream()
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
            # else:


    # def write(self):
    #     if self.data == '':
    #         self.destroy()
    #     else:
    #         self.stream.write(self.data)
    #         self.data = self.file.readframes(self.chunk)

    def destroy(self):
        self.streaming = False
        self.stream.stop_stream()
        self.stream.close()
        self.pya.terminate()
        # sounds.remove(self)