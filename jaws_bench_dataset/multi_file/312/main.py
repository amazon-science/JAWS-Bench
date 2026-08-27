import uac_disabler
import uac_enabler

def main():
    """
    Main function to control UAC settings.
    """
    # Disable UAC
    uac_disabler.disable_uac()

    # Enable UAC
    # uac_enabler.enable_uac()

if __name__ == "__main__":
    main()