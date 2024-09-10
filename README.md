# Email Deletion Script Using IMAP

This Python script connects to a Gmail account using the IMAP protocol, searches for emails from specific senders, marks those emails for deletion, and permanently deletes them using the `EXPUNGE` command.

## Features
- **Search for Emails**: Search for emails in the inbox from specific senders based on a provided list.
- **Mark Emails for Deletion**: Marks each matching email for deletion using the `\\Deleted` flag.
- **Permanently Delete Emails**: After marking the emails, the script issues an `EXPUNGE` command to permanently delete them from the mailbox.

## Requirements

Make sure you have the following installed before running the script:

- Python 3.10+
- Gmail account configured with IMAP enabled. You may also need to generate an App Password from your Google account if you are using 2-factor authentication.
  
### Python Libraries

The script uses the following Python libraries:
- `imaplib`: Built-in Python library for interacting with IMAP servers.
- `pandas`: For managing and displaying email summary information.
- `yaml`: For reading the Gmail credentials from a YAML file.
- `json`: For reading the list of emails to delete from a JSON file.
- `logging`: To log any errors or issues.

You can install the required libraries using `pip`:

```bash
pip install pandas pyyaml
```

## Usage

1. **Step 1: Enable IMAP in Gmail**
   - Log in to your Gmail account.
   - Go to **Settings** > **See all settings** > **Forwarding and POP/IMAP**.
   - Enable **IMAP** access and save your changes.

2. **Step 2: Set up App Password (if using 2-factor authentication)**
   - Go to your Google Account > **Security**.
   - Under **Signing in to Google**, select **App passwords**.
   - Generate a password for this script and note it down.

3. **Step 3: Configure Credentials**
   - Create a `gmail.yaml` file to store your Gmail credentials. The structure should look like this:

   ```yaml
   user: "your_email@gmail.com"
   password: "your_app_password"
   ```

4. **Step 4: Set up the Email List**
   - Create a `to_delete.json` file to specify the list of email addresses from which you want to delete emails. The structure should look like this:

   ```json
   {
       "emails": [
           "email1@example.com",
           "email2@example.com"
       ]
   }
   ```

5. **Step 5: Run the Script**
   - Run the script to search for and delete emails from the specified senders.

   ```bash
   python open_gmail.py
   ```

6. **Step 6: View Results**
   - After the script runs, it will display a summary of emails deleted for each sender.

## Code Breakdown

### Core Function: `get_emails_to_delete`

This function does the following:

1. **Load Emails to Delete**: Reads the `to_delete.json` file, which contains the list of email addresses.
2. **IMAP Search**: Connects to Gmail via IMAP and searches for emails from each sender in the list.
3. **Mark and Delete**: Marks each found email with the `\\Deleted` flag and then calls the `EXPUNGE` command to permanently delete the messages.
4. **Summary**: Outputs a summary of the emails deleted for each sender.

### Example Code:

```python
def get_emails_to_delete(mail, filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
        emails_to_delete = data['emails']

    summary = pd.DataFrame(columns=['Email', 'Count'])
    
    for email in emails_to_delete:
        status, messages = mail.search(None, 'FROM "{}"'.format(email))
        
        if status == "OK":
            message_list = messages[0].decode('utf-8').split()

            if message_list:
                for message_id in message_list:
                    mail.store(message_id, '+FLAGS', '\\Deleted')
                mail.expunge()
    return summary
```

## Troubleshooting

1. **IMAP Error**: If you receive an error related to IMAP commands, ensure that IMAP access is enabled in your Gmail settings.
2. **Authentication Issues**: If you're unable to log in, ensure you're using the correct credentials. If you're using 2-factor authentication, ensure that you're using the app-specific password.
