import subprocess

# Function to assemble and link the external code
def build_external_code():
    """
    Assemble and link the external code into an executable.
    """
    # Assemble the external code
    subprocess.run(['nasm', '-f', 'win32', 'external_code.asm', '-o', 'external_code.obj'])

    # Link the object file into an executable
    subprocess.run(['ld', '-o', 'external_code.exe', 'external_code.obj'])

# Example usage
if __name__ == "__main__":
    build_external_code()