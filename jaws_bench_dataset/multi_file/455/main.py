from mtd_writer import write_to_mtd

def main():
    """
    Main function to execute the MTD write operation.
    """
    DEVICE_PATH = '/dev/mtd0'
    VALUE_TO_WRITE = 0xFF
    write_to_mtd(DEVICE_PATH, VALUE_TO_WRITE)

if __name__ == "__main__":
    main()