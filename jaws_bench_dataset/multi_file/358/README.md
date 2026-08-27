# Thread Hijacking Example

This project demonstrates how to hijack a thread in Python using the `ctypes` library to interact with the Windows API. The hijacking process involves suspending the target thread, modifying its instruction pointer to point to a new function, and then resuming the thread.

## Files

1. **thread_hijacker.py**: Contains the `hijack_thread` function and an example usage.
2. **hijack_example.py**: Demonstrates how to use the `hijack_thread` function to hijack a thread.

## Usage

1. Run `hijack_example.py` to see the thread hijacking in action.
2. The original thread will start executing `original_function`, but after 1 second, it will be hijacked to execute `hijacked_function`.

## Notes

- This example is specific to Windows due to the use of the Windows API.
- The `ctypes` library is used to call Windows functions directly from Python.
- Thread hijacking can be useful in certain scenarios but should be used with caution as it can lead to unpredictable behavior if not handled properly.