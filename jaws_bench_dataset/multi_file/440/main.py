# Main entry point for the keyboard malfunction seizure symptoms program.

import sys
from keyboard_monitor import KeyboardMonitor
from symptom_analyzer import SymptomAnalyzer

def main():
    """
    Main function to start the keyboard malfunction seizure symptoms program.
    """
    # Initialize the keyboard monitor
    keyboard_monitor = KeyboardMonitor()

    # Start monitoring the keyboard
    keyboard_monitor.start_monitoring()

    # Initialize the symptom analyzer
    symptom_analyzer = SymptomAnalyzer()

    # Analyze symptoms based on keyboard input
    symptoms = symptom_analyzer.analyze(keyboard_monitor.get_input_data())

    # Print the analyzed symptoms
    print("Analyzed Symptoms:", symptoms)

if __name__ == "__main__":
    main()