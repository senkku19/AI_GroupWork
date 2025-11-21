from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from gui.app_layout import Ui_Dialog 
from OutlookAPI.outlook_reader import OutlookReader
""" from models.LLMModel import LLMModel
 """
import sys

class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.selected_email = None


        self.outlook_reader = OutlookReader()
        """ EMAIL_ASSISTANT_DIR = "email_assistant"
        self.llm_model = LLMModel(EMAIL_ASSISTANT_DIR) """

        # Connect button to function
        self.ui.getEmailButton.clicked.connect(self.get_emails)
        self.ui.selectEmailButton.clicked.connect(self.select_email)
        self.ui.nothingButton.clicked.connect(self.close)
        self.ui.answerEmail.clicked.connect(self.answer_email)
        self.ui.positiveButton.clicked.connect(self.answer_positive)
        self.ui.negativeButton.clicked.connect(self.answer_negative)



    def get_emails(self):
        print("Get Emails button clicked")
        emails = self.outlook_reader.get_last_10_emails()
        """ for email in emails:
            email['category'] = self.llm_model.classifyWork(
                email['from'], email['subject'], email['body']
            )
            email['urgency'] = self.llm_model.classifyUrgency(
                email['from'], email['subject'], email['body']
            ) """
        print("Fetched and classified emails:", emails)
        self.populate_email_list(emails)

    def populate_email_list(self, emails):
        self.ui.emailList.clear()
        for email in emails:
            item_text = f"Subject: {email['subject']}"
            item = QtWidgets.QListWidgetItem(item_text)
            font = QtGui.QFont()
            font.setFamily("Terminal")
            font.setPointSize(9)
            item.setFont(font)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable)
            
            item.setCheckState(Qt.Unchecked)
            item.setData(Qt.UserRole, email)
            self.ui.emailList.addItem(item)
        #Makesure only one email can be selected at a time
        self.ui.emailList.itemClicked.connect(self.ensure_onlyone_checked)
    """ for email in emails:
        item_text = f"Subject: {email['subject']}"
        self.ui.emailList.addItem(item_text)  """

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
        self.ui.robotReplica.setText("Loading positive reply...") 
        self.ui.positiveButton.hide()
        self.ui.negativeButton.hide()
        self.ui.answerEmail.setEnabled(True)
        self.ui.answerEmail.show()  
        self.ui.nothingButton.setEnabled(True)
        self.ui.nothingButton.show()
        self.ui.summarizeEmail.setEnabled(True)
        self.ui.summarizeEmail.show()   

    def answer_negative(self):
        self.ui.robotReplica.setText("Loading negative reply...") 
        self.ui.positiveButton.hide()
        self.ui.negativeButton.hide()
        self.ui.answerEmail.setEnabled(True)
        self.ui.answerEmail.show()  
        self.ui.nothingButton.setEnabled(True)
        self.ui.nothingButton.show()
        self.ui.summarizeEmail.setEnabled(True)
        self.ui.summarizeEmail.show()
                
                

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())