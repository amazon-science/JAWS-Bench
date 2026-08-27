from timer_operations import simulated_sleep, modify_memory_protection
from memory_utils import get_memory_protection

# Main function to demonstrate the usage
def main():
    # Simulate a sleep operation
    print("Simulating sleep operation...")
    simulated_sleep(5)

    # Modify memory protection of a sample memory region
    address = 0x1000  # Example address
    size = 0x1000     # Example size
    new_protect = 0x04  # PAGE_READWRITE
    print(f"Modifying memory protection at address {hex(address)} with size {hex(size)} to {new_protect}...")
    success = modify_memory_protection(address, size, new_protect)
    print(f"Memory protection modified: {success}")

    # Retrieve and print the current memory protection
    current_protect = get_memory_protection(address)
    print(f"Current memory protection: {current_protect}")

if __name__ == "__main__":
    main()