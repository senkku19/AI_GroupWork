import win32com.client
from datetime import datetime

def safe_datetime(value):
    try:
        if isinstance(value, datetime):
            return value.isoformat()

        return datetime.fromtimestamp(value.timestamp()).isoformat()
    except Exception:
        return str(value)

class OutlookReader:
    def __init__(self):
        self.outlook = win32com.client.Dispatch("Outlook.Application")
        self.namespace = self.outlook.GetNamespace("MAPI")
        self.inbox = self.namespace.GetDefaultFolder(6)  # 6 = Inbox

    def get_last_10_emails(self):
        messages = self.inbox.Items
        messages.Sort("[ReceivedTime]", True)  # newest first

        results = []
        count = 0

        for msg in messages:
            try:
                email_data = {
                    "subject": str(msg.Subject),
                    "from": str(msg.SenderName),
                    "received": safe_datetime(msg.ReceivedTime),
                    "read": bool(not msg.UnRead),
                    "body": (msg.Body or "").replace("\r", " ").replace("\n", " ")
                }

                results.append(email_data)

                count += 1
                if count >= 10:
                    break

            except Exception:
                continue

        return results


if __name__ == "__main__":
    reader = OutlookReader()
    data = reader.get_last_10_emails()
    print(data)
