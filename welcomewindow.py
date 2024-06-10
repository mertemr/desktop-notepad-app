import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional

import orjson
from PyQt6 import QtWidgets
from PyQt6.uic.load_ui import loadUi

from msgbox import MessageBox, MB_ICONERROR, MB_OK
from dialogPassword import DialogPassword
from notewindow import NoteWindow

RECENTS_FILE = Path("recents.json").absolute()
RECENTS: List[str] = orjson.loads(RECENTS_FILE.read_bytes()) if RECENTS_FILE.exists() else []

DATA = {
    "notes": {},
    "password": "",
}

def hash_password(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()

class WelcomeWindow(QtWidgets.QWidget):
    UI = Path("resources/welcome.ui").absolute()
    def __init__(self):
        super().__init__()
        loadUi(str(self.UI), self)
        
        self.init()
        self.show()

    def init(self):
        self.button_createRepo: QtWidgets.QPushButton
        self.button_openRepo: QtWidgets.QPushButton

        self.button_createRepo.clicked.connect(self.create_repo)
        self.button_openRepo.clicked.connect(self.open_repo)
        
        self.recent_repos: QtWidgets.QListWidget
        self.recent_repos.itemDoubleClicked.connect(self.open_repo)
        
        self.button_clearRecents: QtWidgets.QPushButton
        self.button_clearRecents.clicked.connect(self.clear_recents)
        
        if RECENTS:
            for recent in RECENTS:
                if not Path(recent).exists():
                    continue
                self.recent_repos.addItem(recent)
            self.button_clearRecents.setEnabled(True)
        
        self.repo_password = ""
        self.gui_dialogPassword = None
        
        self.gui_note = None
    
    def clear_recents(self):
        self.recent_repos.clear()
        RECENTS.clear()
        RECENTS_FILE.unlink(missing_ok=True)
        self.button_clearRecents.setEnabled(False)
        
    def update_recents(self):
        RECENTS.clear()
        RECENTS.extend(self.recent_repos.item(i).text() for i in range(self.recent_repos.count()))
        RECENTS_FILE.write_bytes(orjson.dumps(RECENTS))
    
    def set_password(self, password: str):
        self.repo_password = password

    def create_repo(self):
        file = QtWidgets.QFileDialog.getSaveFileName(
            self, "Create Repository", "", "Note Repository (*.nepo)"
        )[0]

        if not file:
            return
            
        self.gui_dialogPassword = DialogPassword()
        self.gui_dialogPassword.PASSWORD.connect(self.set_password)
        self.gui_dialogPassword.exec()
                
        if not self.repo_password:
            return MessageBox("Error", "Depoya bir şifre belirleyin.", MB_ICONERROR | MB_OK).show()
        
        DATA["password"] = hash_password(self.repo_password).hex()
        
        f = Path(file).absolute()
        f.touch(exist_ok=True)
        
        if f.name not in RECENTS:
            self.recent_repos.addItem(str(f))
        self.update_recents()
        f.write_bytes(orjson.dumps(DATA))
        self.open_notes(DATA, repo_file=f)

    def open_repo(self, item: Optional[QtWidgets.QListWidgetItem] = None):
        if item:
            select_file = item.text()
        else:
            select_file = QtWidgets.QFileDialog.getOpenFileName(
                self, "Open Repository", "", "Note Repository (*.nepo)"
            )[0]

        if not select_file or not Path(select_file).exists():
            return
        
        self.gui_dialogPassword = DialogPassword(mode="open")
        self.gui_dialogPassword.PASSWORD.connect(self.set_password)
        self.gui_dialogPassword.exec()
        
        if not self.repo_password:
            return

        data = orjson.loads(Path(select_file).read_bytes())
        hash = hash_password(self.repo_password).hex()
        
        print(data)
        
        if hash != data["password"]:
            del data
            return MessageBox("Error", "Password is incorrect.", MB_ICONERROR | MB_OK).show()
        
        self.open_notes(data, repo_file=select_file)
    
    def open_notes(self, data: Dict[str, Any], repo_file: str = "") -> None:
        self.gui_note = NoteWindow(data, repo_file, self)
        self.gui_note.LOCK_NOTES.connect(self.lock_notes)
        self.gui_note.CLOSE_APP.connect(self.close)
        self.gui_note.NOTE_DATA.connect(self.update_notes)
        self.unlock_notes()
        
    def update_notes(self, data: Dict[str, Any]):
        print(DATA)
        DATA["notes"] = data
        Path(self.gui_note._file).write_bytes(orjson.dumps(DATA))
        
    def unlock_notes(self):
        self.raisewindow(self.gui_note)
        self.hide()
    
    def lock_notes(self):
        self.raisewindow(self)
        self.gui_note.hide()
    
    @staticmethod
    def raisewindow(window: QtWidgets.QWidget):
        window.show()
        window.activateWindow()
        window.raise_()
        window.setFocus()
        