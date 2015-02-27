__author__ = 'brad'
import pyaudio
import wave
import cStringIO


class SoundStream():
    def __init__(self, pya, address=None, streaming=True):
        if address is not None:
            self.file = wave.open(str(address), 'rb')
        else:
            self.file = None
        self.pya = pya
        self.stream = None
        self.streaming = streaming
        self.address = address
        self.chunk = 1024
        self.channels = 2
        self.complete = False

    def callback(self, in_data, frame_count, time_info, status):
        if self.streaming:
            data = self.file.readframes(frame_count)

            if len(data) < self.file.getnchannels()*self.file.getsampwidth()*frame_count:
                length = self.file.getnchannels()*self.file.getsampwidth()*frame_count - len(data)
                data += chr(0) * length
            return data, pyaudio.paContinue
        else:
            data = ''
            if not self.complete:
                data = self.file.readframes(frame_count)
            final_pos = self.file.data.tell()
            print(str(len(data)))
            if len(data) < self.file.channels*self.file.width*frame_count:
                length = self.file.channels*self.file.width*frame_count - len(data)
                data += chr(0) * length
            if self.complete:
                self.complete = False
                return data, pyaudio.paComplete
            if final_pos == 0:
                self.complete = True
            return data, pyaudio.paContinue

    def play(self, sound_file=None):
        if sound_file is not None and self.streaming:
            self.address = sound_file
            if self.stream is not None:
                self.stream.close()
        if self.streaming:
            if self.address is not None:
                self.file = wave.open(str(self.address), 'rb')
                self.stream = self.pya.open(format=self.pya.get_format_from_width(self.file.getsampwidth()),
                                            channels=self.file.getnchannels(),
                                            rate=self.file.getframerate(),
                                            output=True,
                                            stream_callback=self.callback)
        else:
            if self.stream is not None:
                self.stream.close()
            self.file = sound_file
            self.stream = self.pya.open(format=self.pya.get_format_from_width(sound_file.width),
                                        channels=sound_file.channels,
                                        rate=sound_file.framerate,
                                        output=True,
                                        stream_callback=self.callback)

        # self.stream.start_stream()
        # self.streaming = True

    def stop(self):
        # self.streaming = False
        self.stream.stop_stream()
        self.stream.close()

    def update(self):
        if self.streaming:
            if self.stream is not None:
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
        # self.streaming = False
        self.stream.stop_stream()
        self.stream.close()
        # self.pya.terminate()
        # sounds.remove(self)


class WaveFile():
    def __init__(self, address):
        self.file = wave.open(address, 'rb')
        self.width = self.file.getsampwidth()
        self.channels = self.file.getnchannels()
        self.framerate = self.file.getframerate()
        self.data = cStringIO.StringIO(self.file.readframes(self.file.getnframes()))
        self.file.close()
        self.complete = False

    def readframes(self, frame_count):
        data = self.data.read(frame_count*self.channels*self.width)
        if self.complete:
            self.data.seek(0)
            self.complete = False
        if self.data.tell() == len(self.data.getvalue()):
            self.complete = True
        return data
