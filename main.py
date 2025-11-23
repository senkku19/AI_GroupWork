from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from gui.app_layout import Ui_Dialog 
from OutlookAPI.outlook_reader import OutlookReader
from models.LLMModel import LLMModel
import sys

# --- SÄILYTÄ TÄMÄ LUOKKA ENNALLAAN ---
class EmailProcessor():
    def __init__(self):
        # Huom: Varmista että polku on oikein suhteessa siihen mistä ajat koodin
        EMAIL_ASSISTANT_DIR = "../AI_GroupWork/models/email_assistant"
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

# --- UUSI WORKER-LUOKKA ---
# Tämä hoitaa luokittelun taustalla ilman että UI jäätyy
class ClassificationWorker(QThread):
    finished = pyqtSignal(list) # Signaali kun valmis, palauttaa listan
    error = pyqtSignal(str)     # Signaali jos virhe

    def __init__(self, processor, emails):
        super().__init__()
        self.processor = processor
        self.emails = emails

    def run(self):
        try:
            # Ajetaan raskas operaatio tässä säikeessä
            classified_emails = self.processor.classify_email(self.emails)
            self.finished.emit(classified_emails)
        except Exception as e:
            self.error.emit(str(e))

# --- PÄIVITETTY MAINWINDOW ---
class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.selected_email = None

        self.outlook_reader = OutlookReader()
        
        # Ladataan malli heti alussa (kestää hetken, UI saattaa odottaa tässä)
        # Jos haluat loading screenin jo tähän, myös tämä pitäisi siirtää säikeeseen.
        self.email_processor = EmailProcessor() 
        
        # Poistettu ProcessPoolExecutor
        self.worker = None 

        # Connect button to function
        self.ui.getEmailButton.clicked.connect(self.get_emails)
        self.ui.selectEmailButton.clicked.connect(self.select_email)
        self.ui.nothingButton.clicked.connect(self.close)
        self.ui.answerEmail.clicked.connect(self.answer_email)
        self.ui.positiveButton.clicked.connect(self.answer_positive)
        self.ui.negativeButton.clicked.connect(self.answer_negative)
        self.ui.summarizeEmail.clicked.connect(self.summarize_email)

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

        # Käynnistetään QThread
        self.worker = ClassificationWorker(self.email_processor, emails)
        self.worker.finished.connect(self.on_classification_finished)
        self.worker.error.connect(self.on_classification_error)
        self.worker.start() # Tämä käynnistää run() metodin taustalla
    
    # Nämä korvaavat check_future-metodin
    def on_classification_finished(self, classified_emails):
        self.populate_email_list_and_update_ui(classified_emails)
        self.worker = None # Siivotaan worker

    def on_classification_error(self, error_msg):
        self.ui.robotReplica.setText(f"Error classifying: {error_msg}")
        self.ui.getEmailButton.setEnabled(True)
        self.worker = None

    def populate_email_list(self, emails):
        self.ui.emailList.clear()
        for email in emails:
            item_text = f"Subject: {email['subject']} | Category: {email.get('category', 'N/A')} | Urgency: {email.get('urgency', 'N/A')}"
            item = QtWidgets.QListWidgetItem(item_text)
            font = QtGui.QFont()
            font.setFamily("Terminal") # Tai mikä fontti sinulla onkaan
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

    # ... Loput metodit (ensure_onlyone_checked, select_email, jne.) pysyvät samoina ...
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

        # Huom: Myös vastausten generointi voi jäädyttää UI:n. 
        # Voit tehdä niillekin samanlaisen Worker-luokan jos haluat.
        try:
            # Qt:ssa UI päivittyy vasta kun funktio loppuu, ellei käytä processEvents
            QtWidgets.QApplication.processEvents() 
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
            QtWidgets.QApplication.processEvents()
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
            QtWidgets.QApplication.processEvents()
            summary = self.email_processor.summarize_email(self.selected_email)
            self.ui.outputText.setHtml(summary)
            self.ui.robotReplica.setText("Summary generated.")
        except Exception as e:
            self.ui.robotReplica.setText(f"Error generating summary: {str(e)}")              
                

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())