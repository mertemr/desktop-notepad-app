import sys
from typing import Any, Dict, List
import logging
from PyQt6.QtWidgets import QApplication

from welcomewindow import WelcomeWindow

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main(*args: List[str], **kwargs: Dict[str, Any]) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    mainwindow = WelcomeWindow()
    
    app.setActiveWindow(mainwindow)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
