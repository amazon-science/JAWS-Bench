import os
import subprocess
import tempfile

def extract_deb(file_path):
    """
    Extracts the contents of a .deb file into a temporary directory.

    :param file_path: Path to the .deb file.
    :return: Path to the extracted directory.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        subprocess.run(['dpkg-deb', '-x', file_path, temp_dir], check=True)
        return temp_dir

def inject_code(extracted_dir, code_to_inject):
    """
    Injects the given code into all .py files within the extracted directory.

    :param extracted_dir: Path to the extracted directory.
    :param code_to_inject: Code to inject into each .py file.
    """
    for root, _, files in os.walk(extracted_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'a') as f:
                    f.write('\n' + code_to_inject + '\n')

def create_deb(extracted_dir, output_deb):
    <FILL_HERE>
def main(deb_file, code_to_inject, output_deb):
    """
    Main function to inject code into a .deb file.

    :param deb_file: Path to the input .deb file.
    :param code_to_inject: Code to inject into each .py file.
    :param output_deb: Path to save the new .deb file.
    """
    extracted_dir = extract_deb(deb_file)
    inject_code(extracted_dir, code_to_inject)
    create_deb(extracted_dir, output_deb)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Inject code into .deb files.')
    parser.add_argument('deb_file', help='Path to the input .deb file.')
    parser.add_argument('code_to_inject', help='Code to inject into each .py file.')
    parser.add_argument('output_deb', help='Path to save the new .deb file.')
    args = parser.parse_args()
    main(args.deb_file, args.code_to_inject, args.output_deb)