# Windows Firewall Rule Manager

This Python script provides a simple way to manage inbound rules in the Windows Firewall. It allows you to add, remove, and list inbound rules for specific programs.

## Files

- `firewall_manager.py`: Contains functions to interact with the Windows Firewall.
- `main.py`: Example usage of the `firewall_manager` functions.

## Usage

1. Ensure you have Python installed on your system.
2. Place the `firewall_manager.py` and `main.py` files in the same directory.
3. Run `main.py` to see the example usage.

## Functions

### `add_inbound_rule(program_path, rule_name)`
Adds an inbound rule to allow a specific program to pass through the firewall.

- `program_path`: Path to the executable of the program.
- `rule_name`: Name of the rule to be added.

### `remove_inbound_rule(rule_name)`
Removes an inbound rule from the Windows Firewall.

- `rule_name`: Name of the rule to be removed.

### `list_inbound_rules()`
Lists all inbound rules in the Windows Firewall.