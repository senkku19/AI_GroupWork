import win32com.client
from datetime import datetime
from bs4 import BeautifulSoup

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

    # To clean HTML content from email body
    def clean_html(self, raw_html):
        soup = BeautifulSoup(raw_html, "html.parser")
        for tag in soup(["script", "style", "head"]):
            tag.decompose()
        return ' '.join(soup.get_text(separator=" ").split())

    def get_last_10_emails(self):
        messages = self.inbox.Items
        messages.Sort("[ReceivedTime]", True)  # newest first

        results = []
        msg = messages.GetFirst()
        count = 0

        while msg and count < 10:
            try:
                raw_body = msg.HTMLBody if msg.HTMLBody else msg.Body
                clened_body = self.clean_html(raw_body)
                body_limited = clened_body[-2048:] 
                email_data = {
                    "subject": str(msg.Subject),
                    "from": str(msg.SenderName),
                    "received": safe_datetime(msg.ReceivedTime),
                    "read": bool(not msg.UnRead),
                    "body": body_limited
                }

                results.append(email_data)

                count += 1
                msg = messages.GetNext()
            except Exception:
                msg = messages.GetNext()
                continue

        return results


if __name__ == "__main__":
    reader = OutlookReader()
    data = reader.get_last_10_emails()
    print(data)
