

from PyQt5 import QtCore, QtGui, QtWidgets

from gui import assets_rc



class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(901, 740)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 901, 741))
        self.widget.setStyleSheet("QWidget#widget{\n"
"background-color:rgb(240, 215, 148);\n"
"border: 10px solid rgb(0, 0, 0);\n"
"}")
        self.widget.setObjectName("widget")
        self.verticalWidget = QtWidgets.QWidget(self.widget)
        self.verticalWidget.setGeometry(QtCore.QRect(480, 210, 401, 271))
        self.verticalWidget.setStyleSheet("QWidget#verticalWidget{\n"
"background-color:rgb(199, 179, 127);\n"
"border: 2px solid rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton {\n"
"background-color:white;\n"
"border: 2px solid rgb(0, 0, 0);\n"
"height:38;\n"
"}\n"
"\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgb(234, 234, 234);\n"
"    border: 2px solid rgb(165, 165, 165);\n"
"}\n"
"\n"
"\n"
"QPushButton:pressed {\n"
"    color: rgb(165, 165, 165);\n"
"    border: 2px solid rgb(165, 165, 165);\n"
"}")
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.summarizeEmail = QtWidgets.QPushButton(self.verticalWidget)
        self.summarizeEmail.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(12)
        self.summarizeEmail.setFont(font)
        self.summarizeEmail.setStyleSheet("")
        self.summarizeEmail.setCheckable(False)
        self.summarizeEmail.setAutoDefault(True)
        self.summarizeEmail.setDefault(False)
        self.summarizeEmail.setObjectName("summarizeEmail")
        self.verticalLayout_2.addWidget(self.summarizeEmail)
        self.answerEmail = QtWidgets.QPushButton(self.verticalWidget)
        self.answerEmail.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(12)
        self.answerEmail.setFont(font)
        self.answerEmail.setStyleSheet("")
        self.answerEmail.setObjectName("answerEmail")
        self.verticalLayout_2.addWidget(self.answerEmail)
        self.nothingButton = QtWidgets.QPushButton(self.verticalWidget)
        self.nothingButton.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(12)
        self.nothingButton.setFont(font)
        self.nothingButton.setStyleSheet("")
        self.nothingButton.setObjectName("nothingButton")
        self.verticalLayout_2.addWidget(self.nothingButton)
        self.positiveButton = QtWidgets.QPushButton(self.widget)
        self.positiveButton.setText("Positive Reply")
        self.positiveButton.setStyleSheet("background-color:white; border: 2px solid black;")
        self.positiveButton.hide()
        self.verticalLayout_2.addWidget(self.positiveButton)
        self.negativeButton = QtWidgets.QPushButton(self.widget)
        self.negativeButton.setText("Negative Reply")
        self.negativeButton.setStyleSheet("background-color:white; border: 2px solid black;")
        self.negativeButton.hide()
        self.verticalLayout_2.addWidget(self.negativeButton)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(690, 30, 181, 191))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/robot_mascot/robot_mascot.PNG"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.robotReplica = QtWidgets.QLabel(self.widget)
        self.robotReplica.setGeometry(QtCore.QRect(480, 60, 221, 131))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.robotReplica.setFont(font)
        self.robotReplica.setStyleSheet("background: rgb(255, 255, 255);\n"
"border: 3px solid rgb(0, 0, 0);")
        self.robotReplica.setAlignment(QtCore.Qt.AlignCenter)
        self.robotReplica.setWordWrap(True)
        self.robotReplica.setObjectName("robotReplica")
        
        self.horizontalWidget = QtWidgets.QWidget(self.widget)
        self.horizontalWidget.setGeometry(QtCore.QRect(30, 650, 441, 61))
        self.horizontalWidget.setStyleSheet("QPushButton {\n"
"background-color:white;\n"
"border: 2px solid rgb(0, 0, 0);\n"
"height:38;\n"
"}\n"
"\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgb(212, 212, 212);\n"
"    border: 2px solid rgb(165, 165, 165);\n"
"}\n"
"\n"
"\n"
"QPushButton:pressed {\n"
"    color: rgb(165, 165, 165);\n"
"    border: 2px solid rgb(165, 165, 165);\n"
"}")
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.selectEmailButton = QtWidgets.QPushButton(self.horizontalWidget)
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(12)
        self.selectEmailButton.setFont(font)
        self.selectEmailButton.setStyleSheet("")
        self.selectEmailButton.setObjectName("selectEmailButton")
        self.horizontalLayout.addWidget(self.selectEmailButton)
        self.getEmailButton = QtWidgets.QPushButton(self.horizontalWidget)
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(12)
        self.getEmailButton.setFont(font)
        self.getEmailButton.setStyleSheet("")
        self.getEmailButton.setObjectName("getEmailButton")
        self.horizontalLayout.addWidget(self.getEmailButton)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(20, 30, 431, 20))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.emailList = QtWidgets.QListWidget(self.widget)
        self.emailList.setGeometry(QtCore.QRect(30, 60, 441, 591))
        self.emailList.setObjectName("EmailList")
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(9)
        item.setFont(font)
        item.setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.emailList.addItem(item)
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setGeometry(QtCore.QRect(480, 520, 401, 181))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(9)
        self.scrollArea.setFont(font)
        self.scrollArea.setAutoFillBackground(False)
        self.scrollArea.setStyleSheet("QScrollArea#scrollArea {\n"
"background-color: rgb(255, 255, 255);\n"
"border: 3px solid rgb(0, 0, 0);\n"
"}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 395, 175))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.textBrowser = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 401, 181))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(9)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(480, 490, 291, 20))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.summarizeEmail.setText(_translate("Dialog", "SUMMARIZE EMAIlL"))
        self.answerEmail.setText(_translate("Dialog", "ANSWER EMAIL"))
        self.nothingButton.setText(_translate("Dialog", "NOTHING"))
        self.robotReplica.setText(_translate("Dialog", "Please press GET EMAILS to retrieve emails"))
        self.selectEmailButton.setText(_translate("Dialog", "SELECT EMAIL"))
        self.getEmailButton.setText(_translate("Dialog", "GET EMAILS"))
        self.label_3.setText(_translate("Dialog", "10 NEWEST EMAILS"))
        __sortingEnabled = self.emailList.isSortingEnabled()
        self.emailList.setSortingEnabled(False)
        item = self.emailList.item(0)
        item.setText(_translate("Dialog", "Inquiry"))
        self.emailList.setSortingEnabled(__sortingEnabled)
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Terminal\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Assist says, that:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">cpp</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">void QTableWidget::setCellWidget (int row, int column, QWidget * widget)  </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Sets the given widget to be displayed in the cell in the given row and column, passing the ownership of the widget to the table. If cell widget A is replaced with cell widget B, cell widget A will be deleted.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">And there is analogs to this method in the most of QAbstractItemView descendants.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">You have to subclass Q***Delegate only when you want editor widget to appear in View only when you hit EditTrigger, then vanish and let delegate render the view item in some way.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">If I correct, you wanted to see control in item view all the time and be able to hit controls without the need to enter editing mode and wait while delegate creates editor and set its state, so you do not need to make specific delegate, just set widget into the view\'s item.</span></p></body></html>"))
        self.label_4.setText(_translate("Dialog", "OUTPUT:"))
