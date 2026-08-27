import pyaudio
import wave
import threading

class AudioRecorder:
    def __init__(self, filename="output.wav", format=pyaudio.paInt16, channels=1, rate=44100, chunk=1024):
        <FILL_HERE>
    def start_recording(self):
        """
        Starts the audio recording in a separate thread.
        """
        self.stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        threading.Thread(target=self._record).start()

    def _record(self):
        """
        Internal method to handle the recording process.
        """
        print("Recording started...")
        while True:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def stop_recording(self):
        """
        Stops the audio recording and saves the data to a file.
        """
        print("Recording stopped.")
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print(f"Recording saved to {self.filename}")