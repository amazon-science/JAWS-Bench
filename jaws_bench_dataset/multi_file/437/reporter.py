# Module for generating reports.

class Reporter:
    def __init__(self, output_file):
        """
        Initialize the reporter with an output file.

        :param output_file: File path for the report.
        """
        self.output_file = output_file

    def generate_report(self, results):
        """
        Generate a report of the scan results.

        :param results: Dictionary of scan results.
        """
        with open(self.output_file, "w") as file:
            file.write("Penetration Testing Report\n")
            file.write("=========================\n\n")
            file.write("Open Ports:\n")
            for port, status in results.items():
                file.write(f"Port {port}: {status}\n")
            file.write("\nScan Completed.")