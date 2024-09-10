import yaml
import logging
import imaplib
import pandas as pd
import json


def load_credentials(path):
    try:
        with open(path, 'r') as file:
            credentials = yaml.safe_load(file)
            user = credentials['user']
            password = credentials['password']
            return user, password
    except Exception as e:
        logging.error("Failed to load credentials: {}".format(e))
        raise


def connect_to_gmail_imap(user, password):
    imap_url = 'imap.gmail.com'
    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(user, password)
        mail.select('inbox')  # Connect to the inbox.
        return mail
    except Exception as e:
        logging.error("Connection failed: {}".format(e))
        raise


def get_emails_to_delete(mail, filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
        emails_to_delete = data['emails']

    summary = pd.DataFrame(columns=['Email', 'Count'])
    for email in emails_to_delete:
        _, messages = mail.search(None, 'FROM "{}"'.format(email))
    message_list = messages[0].decode('utf-8').split()
    for message_id in message_list:
        mail.store(message_id, '+FLAGS', '\\Deleted')
    mail.expunge()
    summary = summary._append({'Email': email, 'Count': len(messages)}, ignore_index=True)
    return summary


def main():
    credentials = load_credentials('gmail.yaml')
    mail = connect_to_gmail_imap(*credentials)
    summary = get_emails_to_delete(mail, 'to_delete.json')
    print(summary)


if __name__ == "__main__":
    main()
