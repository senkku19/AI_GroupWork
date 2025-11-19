from PyQt5 import QtWidgets
from app_layout import Ui_Dialog  # your UI file name

import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)

    Dialog.show()

    sys.exit(app.exec_())
