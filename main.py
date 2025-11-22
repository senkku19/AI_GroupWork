from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from gui.app_layout import Ui_Dialog 
from OutlookAPI.outlook_reader import OutlookReader
from models.LLMModel import LLMModel
import sys
import concurrent.futures as concc

class EmailProcessor():
    def __init__(self):
        EMAIL_ASSISTANT_DIR = "models/local_openllama"
        self.llm_model = LLMModel(EMAIL_ASSISTANT_DIR)

    def classify_email(self,emails):
        for email in emails:
            try:
                email['category'] = self.llm_model.classifyWork(
                email.get('from', ''), email.get('subject', ''), email.get('body', '')
                )
            except Exception as e:
                email['category'] = f"error: {str(e)}"

            try:
                email['urgency'] = self.llm_model.classifyUrgency(
                    email.get('from', ''), email.get('subject', ''), email.get('body', '')
                )
            except Exception as e:
                email['urgency'] = f"error: {str(e)}"

        return emails

    def summarize_email(self, email):
        summary = self.llm_model.createSummary(
            email.get('from'), email.get('subject'), email.get('body')
        )
        return summary
    
    def create_reply(self, email, boolean):
        reply = self.llm_model.createAnswer(
            boolean,
            email.get('from'),
            email.get('subject'),
            email.get('body')
        )
        return reply


class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.selected_email = None

        self.outlook_reader = OutlookReader()
        self.email_processor = EmailProcessor()
        self.executor = concc.ProcessPoolExecutor(max_workers=1)
        self.future = None
        self.poll_timer = None

        # Connect button to function
        self.ui.getEmailButton.clicked.connect(self.get_emails)
        self.ui.selectEmailButton.clicked.connect(self.select_email)
        self.ui.nothingButton.clicked.connect(self.close)
        self.ui.answerEmail.clicked.connect(self.answer_email)
        self.ui.positiveButton.clicked.connect(self.answer_positive)
        self.ui.negativeButton.clicked.connect(self.answer_negative)
        self.ui.summarizeEmail.clicked.connect(self.summarize_email)



    def get_emails(self):
        self.ui.robotReplica.setText("Fetching and classifying emails...")
        self.ui.selectEmailButton.setEnabled(False)
        self.ui.getEmailButton.setEnabled(False)

        try:
            emails = self.outlook_reader.get_last_10_emails()
        except Exception as e:
            self.ui.robotReplica.setText(f"Error fetching emails: {str(e)}")
            return
    
        if not emails:
            self.ui.robotReplica.setText("No emails found.")
            return

        self.ui.robotReplica.setText("Classifying emails, please wait...")

        self.future = self.executor.submit(self.email_processor.classify_email, emails)
        if self.poll_timer is None:
            self.poll_timer = QtCore.QTimer(self)
            self.poll_timer.setInterval(200)
            self.poll_timer.timeout.connect(self.check_future)

        self.poll_timer.start()
    
    def check_future(self):
        if self.future is None:
            return
        
        if self.future.done():
            try:
                classified_emails = self.future.result()
            except Exception as e:
                self.ui.robotReplica.setText(f"Error classifying emails: {str(e)}")
                print(f"Error in future: {str(e)}")
                return
            
            self.populate_email_list_and_update_ui(classified_emails)
            self.future = None


    def populate_email_list(self, emails):
        self.ui.emailList.clear()
        for email in emails:
            item_text = f"Subject: {email['subject']} | Category: {email.get('category', 'N/A')} | Urgency: {email.get('urgency', 'N/A')}"
            item = QtWidgets.QListWidgetItem(item_text)
            font = QtGui.QFont()
            font.setFamily("Terminal")
            font.setPointSize(9)
            item.setFont(font)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable)
            
            item.setCheckState(Qt.Unchecked)
            item.setData(Qt.UserRole, email)
            self.ui.emailList.addItem(item)
    
        self.ui.selectEmailButton.setEnabled(True)
        self.ui.getEmailButton.setEnabled(True)

        #Makesure only one email can be selected at a time
        self.ui.emailList.itemClicked.connect(self.ensure_onlyone_checked)

    def populate_email_list_and_update_ui(self, emails):
        self.populate_email_list(emails)
        self.ui.robotReplica.setText("Please select an email...")

    def ensure_onlyone_checked(self, item):
        if item.checkState() == Qt.Checked:
            for email in range(self.ui.emailList.count()):
                list_item = self.ui.emailList.item(email)
                if list_item != item:
                    list_item.setCheckState(Qt.Unchecked)
                self.selected_email = item.data(Qt.UserRole)
        else:
            self.selected_email = None
    
    def select_email(self):
        if self.selected_email:
            self.ui.robotReplica.setText("What would you like me to do with the selected email?")
            self.ui.summarizeEmail.setEnabled(True)
            self.ui.answerEmail.setEnabled(True)
            self.ui.nothingButton.setEnabled(True)
        else:
            self.ui.robotReplica.setText("No email selected. Please select an email.")
            self.ui.summarizeEmail.setEnabled(False)
            self.ui.answerEmail.setEnabled(False)
            self.ui.nothingButton.setEnabled(False)

    def answer_email(self):
        self.ui.robotReplica.setText("How would you like me to reply?")
        self.ui.summarizeEmail.setEnabled(False)
        self.ui.summarizeEmail.hide()
        self.ui.answerEmail.setEnabled(False)
        self.ui.answerEmail.hide()
        self.ui.nothingButton.setEnabled(False)
        self.ui.nothingButton.hide()

        self.ui.positiveButton.show()
        self.ui.negativeButton.show()
    
    def answer_positive(self):
        if self.selected_email is None:
            self.ui.robotReplica.setText("No email selected to reply to.")
            return  
        self.ui.robotReplica.setText("Generating positive reply...") 
        self.ui.positiveButton.hide()
        self.ui.negativeButton.hide()
        self.ui.answerEmail.setEnabled(True)
        self.ui.answerEmail.show()  
        self.ui.nothingButton.setEnabled(True)
        self.ui.nothingButton.show()
        self.ui.summarizeEmail.setEnabled(True)
        self.ui.summarizeEmail.show()   

        try:
            reply = self.email_processor.create_reply(self.selected_email, True)
            self.ui.outputText.setHtml(reply)
            self.ui.robotReplica.setText("Positive reply generated.")
        except Exception as e:
            self.ui.robotReplica.setText(f"Error generating reply: {str(e)}")


    def answer_negative(self):

        if self.selected_email is None:
            self.ui.robotReplica.setText("No email selected to reply to.")
            return
        
        self.ui.robotReplica.setText("Generating negative reply...") 
        self.ui.positiveButton.hide()
        self.ui.negativeButton.hide()
        self.ui.answerEmail.setEnabled(True)
        self.ui.answerEmail.show()  
        self.ui.nothingButton.setEnabled(True)
        self.ui.nothingButton.show()
        self.ui.summarizeEmail.setEnabled(True)
        self.ui.summarizeEmail.show()

        try:
            reply = self.email_processor.create_reply(self.selected_email, False)
            self.ui.outputText.setHtml(reply)
            self.ui.robotReplica.setText("Negative reply generated.")
        except Exception as e:
            self.ui.robotReplica.setText(f"Error generating reply: {str(e)}")
    
    def summarize_email(self):
        if not self.selected_email:
            self.ui.robotReplica.setText("No email selected to summarize.")
            return
        
        self.ui.robotReplica.setText("Generating summary...")
        try:
            summary = self.email_processor.summarize_email(self.selected_email)
            self.ui.outputText.setHtml(summary)
            self.ui.robotReplica.setText("Summary generated.")
        except Exception as e:
            self.ui.robotReplica.setText(f"Error generating summary: {str(e)}")


class EmailWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal(list)

    def __init__(self, emails, llm_model):
        super().__init__()
        self.emails = emails
        self.llm_model = llm_model

    def run(self):
        for email in self.emails:
            email['category'] = self.llm_model.classifyWork(
                email['from'], email['subject'], email['body']
            )
            email['urgency'] = self.llm_model.classifyUrgency(
                email['from'], email['subject'], email['body']
            )
        self.finished.emit(self.emails)
      
                

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())