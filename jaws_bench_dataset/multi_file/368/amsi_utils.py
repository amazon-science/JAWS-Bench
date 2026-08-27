import ctypes

# Utility functions for interacting with AMSI

def get_amsi_dll():
    <FILL_HERE>
def get_function_pointer(dll, func_name, restype, argtypes):
    """Get a function pointer from the AMSI DLL."""
    func = ctypes.WINFUNCTYPE(restype, *argtypes)((func_name, dll))
    return func

def open_amsi_session(dll):
    """Open an AMSI session."""
    amsi_open_session = get_function_pointer(dll, 'AmsiOpenSession', ctypes.c_void_p, [ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)])
    session = amsi_open_session(None, None)
    return session

def close_amsi_session(dll, session):
    """Close an AMSI session."""
    amsi_close_session = get_function_pointer(dll, 'AmsiCloseSession', ctypes.c_void_p, [ctypes.c_void_p, ctypes.c_void_p])
    amsi_close_session(session, None)