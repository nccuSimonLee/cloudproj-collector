import wave
import pyaudio
from pynput import keyboard
from utils import get_file_path



class Recorder:
    def __init__(
        self,
        record_dir,
        chunksize=8192, 
        dataformat=pyaudio.paInt16, 
        channels=2, 
        rate=44100
    ):
        self.chunksize = chunksize
        self.dataformat = dataformat
        self.channels = channels
        self.rate = rate
        self.recording = False
        self.pa = pyaudio.PyAudio()
        self.record_dir = record_dir

    def start(self):
        # * Reference: https://stackoverflow.com/questions/62520952/how-to-record-audio-each-time-user-presses-a-key#answer-62629132
        # we call start and stop from the keyboard listener, so we use the asynchronous 
        # version of pyaudio streaming. The keyboard listener must regain control to 
        # begin listening again for the key release.
        if not self.recording:
            file_path = get_file_path('wav', 'record', self.record_dir)
            self.wf = wave.open(file_path, 'wb')
            self.wf.setnchannels(self.channels)
            self.wf.setsampwidth(self.pa.get_sample_size(self.dataformat))
            self.wf.setframerate(self.rate)
            
            def callback(in_data, frame_count, time_info, status):
                #file write should be able to keep up with audio data stream (about 1378 Kbps)
                self.wf.writeframes(in_data) 
                return (in_data, pyaudio.paContinue)
            
            self.stream = self.pa.open(
                format = self.dataformat,
                channels = self.channels,
                rate = self.rate,
                input = True,
                stream_callback = callback
            )
            self.stream.start_stream()
            self.recording = True
            print('recording started')
            return file_path
    
    def stop(self):
        if self.recording:         
            self.stream.stop_stream()
            self.stream.close()
            self.wf.close()
            
            self.recording = False
            print('recording finished')


class Listener(keyboard.Listener):
    def __init__(self, recorder, collector=None):
        super().__init__(on_press = self.on_press, on_release = self.on_release)
        self.recorder = recorder
        self.file_path = None
        self.collector = collector
    
    def on_press(self, key):
        if key is None: #unknown event
            pass
        elif isinstance(key, keyboard.Key): #special key event
            if key.ctrl:
                self.file_path = self.recorder.start()
        elif isinstance(key, keyboard.KeyCode): #alphanumeric key event
            if key.char == 'q': #press q to quit
                if self.recorder.recording:
                    self.recorder.stop()
                return False #this is how you stop the listener thread
                
    def on_release(self, key):
        if key is None: #unknown event
            pass
        elif isinstance(key, keyboard.Key): #special key event
            if key.ctrl:
                self.recorder.stop()
                if self.collector is not None:
                    self.collector.upload_file(self.file_path)
        elif isinstance(key, keyboard.KeyCode): #alphanumeric key event
            pass