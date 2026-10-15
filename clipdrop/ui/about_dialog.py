"""About Clipmunk: version, license (GPL v3, no warranty), source code and third-party notices."""
import os
import webbrowser

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QVBoxLayout

from .. import __version__
from ..paths import app_root
from . import theme
from .dialogs import Shell, button, label

SOURCE_URL = "https://github.com/PraetorLabs01/Clipmunk"
WEBSITE_URL = "https://praetorlabshq.com/clipmunk/"


def _open_file(*names):
    """Opens the first of `names` next to Clipmunk (the installer has LICENSE.txt, the source has LICENSE)."""
    for name in names:
        path = app_root() / name
        if path.exists():
            os.startfile(str(path)) if os.name == "nt" else webbrowser.open(path.as_uri())
            return
    webbrowser.open(f"{SOURCE_URL}/blob/main/{names[-1]}")


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Clipmunk")
        s = Shell(self, f"Clipmunk {__version__}", "Trim your gaming clips, shrink them to fit Discord, and share them. "
                  "Free and open source, from Praetor Labs.", width=540)
        head = s.title.parentWidget().layout()
        head.removeWidget(s.title)
        head.removeWidget(s.subtitle)
        col = QVBoxLayout()
        col.setSpacing(6)
        col.addWidget(s.title)
        col.addWidget(s.subtitle)
        top = QHBoxLayout()
        top.setSpacing(16)
        logo = QLabel()
        logo.setPixmap(theme.logo_label_pixmap(48))
        top.addWidget(logo, 0, Qt.AlignTop)
        top.addLayout(col, 1)
        head.addLayout(top)

        lic = label("Clipmunk is free software: you can share and change it under the terms of the "
                    "<b>GNU General Public License, version 3</b>. It comes with <b>absolutely no warranty</b>, "
                    "to the extent the law allows. See the license for details.", wrap=True)
        lic.setStyleSheet(f"color:{theme.TEXT_2}; font-size:13px;")
        s.body.addWidget(lic)
        links = label(f"Source code: <a href='{SOURCE_URL}' style='color:{theme.ACCENT}'>{SOURCE_URL[8:]}</a><br>"
                      f"Website: <a href='{WEBSITE_URL}' style='color:{theme.ACCENT}'>{WEBSITE_URL[8:-1]}</a>",
                      wrap=True)
        links.setTextFormat(Qt.RichText)
        links.setOpenExternalLinks(True)
        links.setStyleSheet(f"color:{theme.TEXT_2}; font-size:13px;")
        s.body.addWidget(links)
        third = label("Clipmunk includes FFmpeg (GPL v3), Qt / PySide6 (LGPL v3), Python and other open-source "
                      "parts. Each keeps its own license; the notices list them all, with links to their source.",
                      "Faint", wrap=True)
        s.body.addWidget(third)

        lic_btn = button("License")
        lic_btn.clicked.connect(lambda: _open_file("LICENSE.txt", "LICENSE"))
        notices = button("Third-party notices")
        notices.clicked.connect(lambda: _open_file("THIRD-PARTY-NOTICES.txt"))
        close = button("Close", "Primary")
        close.setDefault(True)
        close.clicked.connect(self.accept)
        s.footer.addWidget(lic_btn)
        s.footer.addWidget(notices)
        s.footer.addStretch()
        s.footer.addWidget(close)
