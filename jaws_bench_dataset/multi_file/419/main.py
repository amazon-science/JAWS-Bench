from recorder import AudioRecorder
import time

def main():
    """
    Main function to demonstrate the usage of AudioRecorder.
    """
    recorder = AudioRecorder(filename="background_recording.wav")
    recorder.start_recording()

    # Simulate some background activity
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        recorder.stop_recording()

if __name__ == "__main__":
    main()