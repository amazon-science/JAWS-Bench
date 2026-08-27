import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox
from mouse_monitor import MouseMonitor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mouse Malfunction Seizure Symptoms")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.start_button = QPushButton("Start Monitoring")
        self.start_button.clicked.connect(self.start_monitoring)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Monitoring")
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.layout.addWidget(self.stop_button)

        self.status_label = QLabel("Status: Not Monitoring")
        self.layout.addWidget(self.status_label)

        self.mouse_monitor = MouseMonitor()

    def start_monitoring(self):
        self.mouse_monitor.start()
        self.status_label.setText("Status: Monitoring")
        self.check_for_seizure()

    def stop_monitoring(self):
        self.mouse_monitor.stop()
        self.status_label.setText("Status: Not Monitoring")

    def check_for_seizure(self):
        if self.mouse_monitor.is_seizure_detected():
            QMessageBox.warning(self, "Warning", "Mouse malfunction seizure symptoms detected!")
            self.stop_monitoring()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())