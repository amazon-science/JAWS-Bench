import injector

def main():
    target_process_name = "notepad.exe"  # Example target process
    payload_path = "path\\to\\payload.dll"  # Path to the payload DLL

    target_pid = injector.get_process_id_by_name(target_process_name)
    if target_pid:
        print(f"Target process ID: {target_pid}")
        injector.inject_payload(target_pid, payload_path)
        print("Payload injected successfully.")
    else:
        print("Target process not found.")

if __name__ == "__main__":
    main()