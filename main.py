from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from gui.app_layout import Ui_Dialog 
from OutlookAPI.outlook_reader import OutlookReader
from models.LLMModel import LLMModel
import sys

# EmailProcessor class to handle email classification, summarization, and reply generation
class EmailProcessor():
    def __init__(self):
        EMAIL_ASSISTANT_DIR = "../AI_GroupWork/models/email_assistant"
        #EMAIL_ASSISTANT_DIR = "../AI_GroupWork/models/local_openllama"  # For testing with base model
        self.llm_model = LLMModel(EMAIL_ASSISTANT_DIR)

    def classify_email(self, emails):
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

# Worker thread for classification
class ClassificationWorker(QThread):
    finished = pyqtSignal(list)  # Signal to emit when done
    error = pyqtSignal(str)       # Signal to emit on error

    def __init__(self, processor, emails):
        super().__init__()
        self.processor = processor
        self.emails = emails

    def run(self):
        try:
            # Perform classification in a thread
            classified_emails = self.processor.classify_email(self.emails)
            self.finished.emit(classified_emails)
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.selected_email = None

        self.outlook_reader = OutlookReader()
        
        # Loads the model here
        self.email_processor = EmailProcessor() 
        
        self.worker = None 

        # Connect button to function
        self.ui.getEmailButton.clicked.connect(self.get_emails)
        self.ui.selectEmailButton.clicked.connect(self.select_email)
        self.ui.nothingButton.clicked.connect(self.close)
        self.ui.answerEmail.clicked.connect(self.answer_email)
        self.ui.positiveButton.clicked.connect(self.answer_positive)
        self.ui.negativeButton.clicked.connect(self.answer_negative)
        self.ui.summarizeEmail.clicked.connect(self.summarize_email)
    
    #Helps to enable or disable action buttons
    def enable_action_buttons(self, boolean):
        self.ui.summarizeEmail.setEnabled(boolean)
        self.ui.answerEmail.setEnabled(boolean)
        self.ui.nothingButton.setEnabled(boolean)
        self.ui.positiveButton.setEnabled(boolean)
        self.ui.negativeButton.setEnabled(boolean)
        self.ui.selectEmailButton.setEnabled(boolean)
        self.ui.getEmailButton.setEnabled(boolean)
    


    #Fetch emails and start classification in a separate thread
    def get_emails(self):
        self.ui.robotReplica.setText("Fetching emails...")
        self.ui.selectEmailButton.setEnabled(False)
        self.ui.getEmailButton.setEnabled(False)

        try:
            emails = self.outlook_reader.get_last_10_emails()
        except Exception as e:
            self.ui.robotReplica.setText(f"Error fetching emails: {str(e)}")
            self.ui.getEmailButton.setEnabled(True)
            return
    
        if not emails:
            self.ui.robotReplica.setText("No emails found.")
            self.ui.getEmailButton.setEnabled(True)
            return

        self.ui.robotReplica.setText("Classifying emails, please wait...")

        # Starts the worker thread for classification
        self.worker = ClassificationWorker(self.email_processor, emails)
        self.worker.finished.connect(self.on_classification_finished)
        self.worker.error.connect(self.on_classification_error)
        self.worker.start()

    #The make_gui_safe method to sanitize text for GUI display
    def make_gui_safe(self, text):
        text = text.replace("‘", "'").replace("’", "'")
        text = text.replace("“", '"').replace("”", '"')
        text = text.replace("—", "-").replace("•", "-")
        return text
    
    # Callback when classification is finished
    def on_classification_finished(self, classified_emails):
        self.populate_email_list_and_update_ui(classified_emails)
        self.worker = None # Clear the worker reference

    # Callback when there is an error during classification
    def on_classification_error(self, error_msg):
        self.ui.robotReplica.setText(f"Error classifying: {error_msg}")
        self.ui.getEmailButton.setEnabled(True)
        self.worker = None

    # Populates the email list in the GUI
    def populate_email_list(self, emails):
        self.ui.emailList.clear()
        for email in emails:
            item_text = f"Subject: {email['subject']} | Category: {email.get('category', 'N/A')} | Urgency: {email.get('urgency', 'N/A')}"
            item_text = self.make_gui_safe(item_text)
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

    # Combines populating email list and updating UI
    def populate_email_list_and_update_ui(self, emails):
        self.populate_email_list(emails)
        self.ui.robotReplica.setText("Please select an email...")

    #This method ensures only one email is checked at a time
    # And updates the selected_email attribute
    def ensure_onlyone_checked(self, item):
        if item.checkState() == Qt.Checked:
            for email in range(self.ui.emailList.count()):
                list_item = self.ui.emailList.item(email)
                if list_item != item:
                    list_item.setCheckState(Qt.Unchecked)
                self.selected_email = item.data(Qt.UserRole)
        else:
            self.selected_email = None
    
    # Handles email selection and updates UI accordingly
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
    
    # Handles the answer email action and updates UI
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
    
    # Handles generating a positive reply
    def answer_positive(self):
        if self.selected_email is None:
            self.ui.robotReplica.setText("No email selected to reply to.")
            return  
        
        # Update UI to show progress
        self.ui.robotReplica.setText("Generating positive reply...") 
        self.ui.positiveButton.hide()
        self.ui.negativeButton.hide()
        self.ui.answerEmail.show()  
        self.ui.nothingButton.show()
        self.ui.summarizeEmail.show()   
        self.enable_action_buttons(False)

        # Generate the reply
        try:
            QtWidgets.QApplication.processEvents() 
            reply = self.email_processor.create_reply(self.selected_email, True)
            reply = self.make_gui_safe(reply)
            self.ui.outputText.setHtml(reply)
            self.ui.robotReplica.setText("Positive reply generated.")
        except Exception as e:
            self.ui.robotReplica.setText(f"Error generating reply: {str(e)}")
        
        self.enable_action_buttons(True)

    # Handles generating a negative reply   
    def answer_negative(self):
        if self.selected_email is None:
            self.ui.robotReplica.setText("No email selected to reply to.")
            return
        
        self.ui.robotReplica.setText("Generating negative reply...") 
        self.ui.positiveButton.hide()
        self.ui.negativeButton.hide()
        self.ui.answerEmail.show()  
        self.ui.nothingButton.show()
        self.ui.summarizeEmail.show()
        self.enable_action_buttons(False)

         # Generate the reply
        try:
            QtWidgets.QApplication.processEvents()
            reply = self.email_processor.create_reply(self.selected_email, False)
            reply = self.make_gui_safe(reply)
            self.ui.outputText.setHtml(reply)
            self.ui.robotReplica.setText("Negative reply generated.")
        except Exception as e:
            self.ui.robotReplica.setText(f"Error generating reply: {str(e)}")
        
        self.enable_action_buttons(True)
    
    # Handles summarizing the selected email
    def summarize_email(self):
        if not self.selected_email:
            self.ui.robotReplica.setText("No email selected to summarize.")
            return
        
        self.ui.robotReplica.setText("Generating summary...")
        self.enable_action_buttons(False)
        try:
            QtWidgets.QApplication.processEvents()
            summary = self.email_processor.summarize_email(self.selected_email)
            summary = self.make_gui_safe(summary)
            self.ui.outputText.setHtml(summary)
            self.ui.robotReplica.setText("Summary generated.")
        except Exception as e:
            self.ui.robotReplica.setText(f"Error generating summary: {str(e)}")   

        self.enable_action_buttons(True)           
                
# Start the application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())