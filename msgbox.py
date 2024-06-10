from typing import Optional

import win32gui

from win32con import MB_OK, MB_ICONINFORMATION, MB_YESNO, MB_ICONQUESTION, MB_ICONERROR, MB_ICONEXCLAMATION

class MessageBox:
    def __init__(
        self,
        title: str,
        message: str,
        type: Optional[int] = MB_OK | MB_ICONINFORMATION,
    ):
        self.title = title
        self.message = message
        self.type = type

    def show(self) -> int:
        return win32gui.MessageBox(0, self.message, self.title, self.type)
