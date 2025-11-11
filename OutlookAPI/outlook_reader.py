import win32com.client
from datetime import datetime

def read_last_20_emails():
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    inbox = namespace.GetDefaultFolder(6)  # 6 = Inbox

    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)  # newest first

    print("Last 20 Emails" + "="*80)

    count = 0
    for msg in messages:
        try:
            print(f"Subject: {msg.Subject}")
            print(f"From: {msg.SenderName}")
            print(f"Received: {msg.ReceivedTime.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Read: {'No' if msg.UnRead else 'Yes'}")
            body = (msg.Body or "").replace("\r", " ").replace("\n", " ")
            print(f"Body Preview: {body}")
            print("-"*80)
            count += 1
            if count >= 20:
                break
        except Exception as e:
            print(f" Skipped item (error: {e})")
            continue

    print(f"\n Done — displayed {count} messages.\n")

if __name__ == "__main__":
    read_last_20_emails()
