from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal
from PyQt6.uic.load_ui import loadUi

from pathlib import Path

class DialogPassword(QtWidgets.QDialog):
    PASSWORD = pyqtSignal(str)
    UI = Path("resources/dialog_password.ui").absolute()
    
    def __init__(self, mode: str = "new", parent=None):
        super().__init__()
        loadUi(str(self.UI), self)
        self.init()
        
        if mode == "open":
            self.input_passwordCheck.hide()
            self.input_password.setPlaceholderText("Enter password")
            self.input_password.textChanged.disconnect()
            self.input_password.textChanged.connect(lambda: self.button_ok.setEnabled(bool(self.input_password.text())))

    def init(self):
        self.buttonBox: QtWidgets.QDialogButtonBox
        
        self.button_ok = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.button_cancel = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        
        self.input_password: QtWidgets.QLineEdit
        self.input_passwordCheck: QtWidgets.QLineEdit
        
        self.input_password.textChanged.connect(self.check_password)
        self.input_passwordCheck.textChanged.connect(self.check_password)
        
        self.checkbox_showPassword: QtWidgets.QCheckBox
        self.checkbox_showPassword.stateChanged.connect(self.show_password)

        self.button_ok.clicked.connect(self.ok)
        self.button_cancel.clicked.connect(self.cancel)
        
        self.input_password.clear()
        self.input_passwordCheck.clear()
        self.checkbox_showPassword.setChecked(False)
        self.button_ok.setEnabled(False)
    
    def show_password(self):
        if self.checkbox_showPassword.isChecked():
            self.input_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.input_passwordCheck.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.input_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.input_passwordCheck.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def check_password(self):
        password = self.input_password.text()
        password_check = self.input_passwordCheck.text()

        if password == password_check:
            self.button_ok.setEnabled(True)
        else:
            self.button_ok.setEnabled(False)
    
    def ok(self):
        password = self.input_password.text()
        self.PASSWORD.emit(password)
        
        self.close()

    def cancel(self):
        self.close()
