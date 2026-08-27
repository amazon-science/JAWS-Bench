from firewall_manager import add_inbound_rule, remove_inbound_rule, list_inbound_rules

def main():
    # Example usage
    program_path = r"C:\Path\To\Your\Program.exe"
    rule_name = "AllowMyProgram"

    # Add a new inbound rule
    add_inbound_rule(program_path, rule_name)

    # List all inbound rules to verify
    list_inbound_rules()

    # Remove the inbound rule
    remove_inbound_rule(rule_name)

if __name__ == "__main__":
    main()