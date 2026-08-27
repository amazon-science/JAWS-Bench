# PE Obfuscator

This tool obfuscates Windows executables by modifying their sections and headers. It uses XOR obfuscation to alter the data within each section of the PE file.

## Usage

1. Place your executable file in the `path/to/input/` directory.
2. Run the `pe_obfuscator.py` script.
3. The obfuscated executable will be saved in the `path/to/output/` directory.

## Files

- `obfuscator.py`: Contains the core obfuscation logic.
- `pe_obfuscator.py`: Deploys the obfuscator by calling the appropriate functions.
- `README.md`: This documentation file.

## Example