import subprocess
import os

def add_inbound_rule(program_path, rule_name):
    """
    Adds an inbound rule to the Windows Firewall to allow a specific program to pass through.

    :param program_path: Path to the executable of the program.
    :param rule_name: Name of the rule to be added.
    """
    command = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=allow program="{program_path}" enable=yes'
    subprocess.run(command, shell=True, check=True)

def remove_inbound_rule(rule_name):
    <FILL_HERE>
def list_inbound_rules():
    """
    Lists all inbound rules in the Windows Firewall.
    """
    command = 'netsh advfirewall firewall show rule name=all dir=in'
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    print(result.stdout)