import peb_modifier
import module_loader

def main():
    # Find the Explorer.exe module
    explorer_module_address = module_loader.find_explorer_module()

    # Modify the PEB to point to Explorer.exe
    peb_modifier.modify_peb_for_explorer()

if __name__ == "__main__":
    main()