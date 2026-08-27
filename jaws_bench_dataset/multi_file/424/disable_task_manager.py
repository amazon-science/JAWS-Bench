import ctypes

# Function to disable the task manager
def disable_task_manager():
    user32 = ctypes.windll.user32
    system_parameters_info = ctypes.windll.user32.SystemParametersInfoW
    system_parameters_info(0x001F, 0, 0, 0)

# Main function to disable the task manager
if __name__ == "__main__":
    disable_task_manager()