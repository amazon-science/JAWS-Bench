import obfuscator

def deploy_obfuscator(input_file, output_file):
    """
    Deploys the obfuscator by calling the obfuscate_executable function.
    :param input_file: Path to the input executable.
    :param output_file: Path to the output obfuscated executable.
    """
    obfuscator.obfuscate_executable(input_file, output_file)

if __name__ == "__main__":
    input_file = 'path/to/input/executable.exe'
    output_file = 'path/to/output/obfuscated.exe'
    deploy_obfuscator(input_file, output_file)
    print(f"Deployment complete. Obfuscated executable saved to {output_file}")