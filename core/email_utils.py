import os

def read_last_email_counter(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return int(file.read().strip())
    return 0

def write_last_email_counter(filename, counter):
    with open(filename, 'w') as file:
        file.write(str(counter))

def generate_unique_email(base_email, counter):
    return f"{base_email.split('@')[0]}+{counter}@{base_email.split('@')[1]}"
