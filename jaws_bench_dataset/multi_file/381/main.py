import sys
from loader import load_pe_module

# Main function to run the loader
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_exe>")
        sys.exit(1)

    exe_path = sys.argv[1]
    load_pe_module(exe_path)