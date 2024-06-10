import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict

import orjson
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSignal
from PyQt6.uic.load_ui import loadUi

from dialogNewnote import DialogNewNote
from msgbox import MB_ICONEXCLAMATION, MB_YESNO, MessageBox


class NoteWindow(QtWidgets.QMainWindow):
    LOCK_NOTES = pyqtSignal()
    CLOSE_APP  = pyqtSignal()
    NOTE_DATA = pyqtSignal(dict)
    
    UI = Path("resources/gui_notes.ui").absolute()

    def __init__(self, data: Dict[str, Any], repo_file: str, parent=None):
        super().__init__()
        loadUi(str(self.UI), self)
        
        self.data = data
        self.data_notes: dict = data.get("notes", {})
        
        self._file = repo_file
        
        self.setWindowTitle(f"Repo: {self._file}")
        self.selected_note = None
        
        self.dn = None
        self.init()
        
        if self.data_notes:
            for note_name in self.data_notes:
                self.list_notes.addItem(note_name)

    def init(self):
        self.button_lock: QtWidgets.QPushButton
        self.button_lock.clicked.connect(self.lock)
        
        self.button_newNote: QtWidgets.QPushButton
        self.button_editNote: QtWidgets.QPushButton
        self.button_deleteNote: QtWidgets.QPushButton
        
        self.button_newNote.clicked.connect(self.new_note)
        self.list_notes: QtWidgets.QListWidget
        
        self.list_notes.itemSelectionChanged.connect(self.toggle_buttons)
        self.list_notes.itemDoubleClicked.connect(self.open_note)
        
        self.button_editNote.clicked.connect(self.edit_note)
        self.button_deleteNote.clicked.connect(self.delete_note)

    def toggle_buttons(self):
        state = bool(self.list_notes.selectedItems())
        self.button_editNote.setEnabled(state)
        self.button_deleteNote.setEnabled(state)
        
        self.selected_note = self.list_notes.currentItem()
        self.selected_noteText = "%d-%s" % (self.list_notes.currentRow(), self.list_notes.currentItem().text())
    
    def edit_note(self):
        self.dn = DialogNewNote()
        self.dn.setWindowTitle("Edit Note")
        self.dn.NOTE_NAME.connect(self.update_note)
        self.dn.note_name.setText(self.selected_note.text())
        self.dn.exec()
        self.dn = None
        
    def open_note(self):
        note_name = self.selected_note.text()
        note_content = self.data_notes[note_name]
        
        temp_fd, temp_path = tempfile.mkstemp(suffix=".txt")
        os.close(temp_fd)
        
        with open(temp_path, "w") as temp_file:
            temp_file.write(note_content)
        
        print(f"Opening note: {note_name}")
        
        proc = subprocess.Popen(["notepad.exe", temp_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        
        with open(temp_path, "r") as temp_file:
            note_content = temp_file.read()
        
        self.data_notes[note_name] = note_content
        
        with open(temp_path, "w") as temp_file:
            temp_file.truncate()
        os.remove(temp_path)
        
        self.NOTE_DATA.emit(self.data_notes)
        
    def update_note(self, note_name: str):
        old_note_name = self.selected_note.text()
        note_content = self.data_notes[old_note_name]
        
        del self.data_notes[old_note_name]
        self.data_notes[note_name] = note_content
        
        self.list_notes.currentItem().setText(note_name)
        
        self.NOTE_DATA.emit(self.data_notes)
        
    def new_note(self):
        self.dn = DialogNewNote()
        self.dn.NOTE_NAME.connect(self.add_note)
        self.dn.exec()
        self.dn = None
        
    def delete_note(self):
        msg = f"Bunu silmek istediğinize emin misiniz: '{self.list_notes.currentItem().text()}'"
        msgbox = MessageBox("Not sil", msg, MB_YESNO | MB_ICONEXCLAMATION)
        result = msgbox.show()
        
        if result == 6:
            note_name = self.list_notes.currentItem().text()
            del self.data_notes[note_name]
            self.list_notes.takeItem(self.list_notes.currentRow())
            self.NOTE_DATA.emit(self.data_notes)

    def add_note(self, note_name: str):
        print(self.data)
        self.data_notes[note_name] = ""
        self.list_notes.addItem(note_name)
        self.NOTE_DATA.emit(self.data_notes)

    def lock(self):
        self.LOCK_NOTES.emit()

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.CLOSE_APP.emit()
        event.accept()
