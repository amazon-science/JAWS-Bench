# fast_io_hook.py

import ctypes
from ctypes import wintypes

# Define the structure for FAST_IO_DISPATCH
class FAST_IO_DISPATCH(ctypes.Structure):
    _fields_ = [
        ("SizeOfFastIoDispatch", wintypes.ULONG),
        ("FastIoCheckIfPossible", ctypes.c_void_p),
        ("FastIoRead", ctypes.c_void_p),
        ("FastIoWrite", ctypes.c_void_p),
        ("FastIoQueryBasicInfo", ctypes.c_void_p),
        ("FastIoQueryStandardInfo", ctypes.c_void_p),
        ("FastIoLock", ctypes.c_void_p),
        ("FastIoUnlockSingle", ctypes.c_void_p),
        ("FastIoUnlockAll", ctypes.c_void_p),
        ("FastIoUnlockAllByKey", ctypes.c_void_p),
        ("FastIoDeviceControl", ctypes.c_void_p),
        ("AcquireFileForNtCreateSection", ctypes.c_void_p),
        ("ReleaseFileForNtCreateSection", ctypes.c_void_p),
        ("FastIoDetachDevice", ctypes.c_void_p),
        ("FastIoQueryNetworkOpenInfo", ctypes.c_void_p),
        ("AcquireForModWrite", ctypes.c_void_p),
        ("MdlRead", ctypes.c_void_p),
        ("MdlReadComplete", ctypes.c_void_p),
        ("PrepareMdlWrite", ctypes.c_void_p),
        ("MdlWriteComplete", ctypes.c_void_p),
        ("FastIoReadCompressed", ctypes.c_void_p),
        ("FastIoWriteCompressed", ctypes.c_void_p),
        ("MdlReadCompleteCompressed", ctypes.c_void_p),
        ("MdlWriteCompleteCompressed", ctypes.c_void_p),
        ("FastIoQueryOpen", ctypes.c_void_p),
        ("ReleaseForModWrite", ctypes.c_void_p),
        ("AcquireForCcFlush", ctypes.c_void_p),
        ("ReleaseForCcFlush", ctypes.c_void_p)
    ]

# Function to hook Fast I/O dispatch table
def hook_fast_io_dispatch(device_object, fast_io_dispatch):
    # Save the original Fast I/O dispatch table
    original_fast_io_dispatch = device_object.FastIoDispatch

    # Create a new FAST_IO_DISPATCH structure
    new_fast_io_dispatch = FAST_IO_DISPATCH()
    new_fast_io_dispatch.SizeOfFastIoDispatch = ctypes.sizeof(FAST_IO_DISPATCH)

    # Copy the original function pointers to the new structure
    for field in FAST_IO_DISPATCH._fields_:
        setattr(new_fast_io_dispatch, field[0], getattr(original_fast_io_dispatch, field[0]))

    # Override the FastIoRead function with our custom function
    new_fast_io_dispatch.FastIoRead = custom_fast_io_read

    # Assign the new dispatch table to the device object
    device_object.FastIoDispatch = new_fast_io_dispatch

# Custom FastIoRead function
def custom_fast_io_read(file_object, file_offset, length, lock_key, buffer, io_status, device_object):
    print("Intercepted FastIoRead request")
    # Call the original FastIoRead function
    original_read = device_object.FastIoDispatch.FastIoRead
    return original_read(file_object, file_offset, length, lock_key, buffer, io_status, device_object)

# Function to unhook Fast I/O dispatch table
def unhook_fast_io_dispatch(device_object, original_fast_io_dispatch):
    <FILL_HERE>