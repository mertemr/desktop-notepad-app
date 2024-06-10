from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal
from PyQt6.uic.load_ui import loadUi

from pathlib import Path

class DialogNewNote(QtWidgets.QDialog):
    NOTE_NAME = pyqtSignal(str)
    UI = Path("resources/dialog_newnote.ui").absolute()
    
    def __init__(self):
        super().__init__()
        loadUi(str(self.UI), self)
        self.init()

    def init(self):
        self.buttonBox: QtWidgets.QDialogButtonBox
        
        self.button_ok = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.button_cancel = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        
        self.note_name: QtWidgets.QLineEdit
        
        self.button_ok.clicked.connect(self.ok)
        self.button_cancel.clicked.connect(self.cancel)
        
        self.button_ok.setEnabled(False)
        self.note_name.textChanged.connect(self.check_note_name)
        
    def check_note_name(self):
        if self.note_name.text():
            self.button_ok.setEnabled(True)
        else:
            self.button_ok.setEnabled(False)
    
    def cancel(self):
        self.close()
        
    def ok(self):
        note_name = self.note_name.text()
        self.NOTE_NAME.emit(note_name)
        self.close()
    