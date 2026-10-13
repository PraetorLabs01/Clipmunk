"""'How to set up sharing': a short two-tab walkthrough for server admins and for friends with an invite."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QButtonGroup, QDialog, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QVBoxLayout, QWidget

from . import theme
from .dialogs import Shell, button, label

ADMIN_STEPS = [
    "In Discord, right-click the channel clips should go to and pick <b>Edit Channel</b>. "
    "<span style='color:{faint}'>(You need the Manage Webhooks permission. Server owners and admins have it.)</span>",
    "Open <b>Integrations</b> → <b>Webhooks</b> → <b>New Webhook</b>. Naming it “Clipmunk” helps you find it later.",
    "Press <b>Copy Webhook URL</b>.",
    "Back in Clipmunk: <b>Add channel</b>, give it a name, paste the link, pick your server's boost level, "
    "then <b>Check and add</b>.",
    "Select the channel and press <b>Copy invite</b>. Post that in your Discord server. "
    "Friends copy it, open Clipmunk, and they're set.",
]
FRIEND_STEPS = [
    "In Discord, find the Clipmunk invite your server posted. It ends in "
    "<span style='font-family:\"{mono}\"; color:{accent}'>clipmunk-invite:…</span>",
    "Copy the whole message: hover it, press <b>⋯</b> → <b>Copy Text</b>, or select it and press <b>Ctrl+C</b>.",
    "Open Clipmunk, or click back into it. It asks <b>“Add #channel to Clipmunk?”</b>. Press <b>Add</b>. "
    "<span style='color:{faint}'>(Nothing popped up? Settings → Paste invite.)</span>",
    "Compress a clip and press <b>Share to Discord</b>. It posts in that channel under your name.",
]


def _steps(items):
    w = QWidget()
    lay = QVBoxLayout(w)
    lay.setContentsMargins(0, 4, 0, 0)
    lay.setSpacing(12)
    fmt = dict(faint=theme.FAINT, accent=theme.ACCENT, mono=theme.MONO_FONT)
    for i, text in enumerate(items, 1):
        row = QHBoxLayout()
        row.setSpacing(12)
        n = QLabel(str(i))
        n.setFixedSize(26, 26)
        n.setAlignment(Qt.AlignCenter)
        n.setStyleSheet(f"background:{theme.ACCENT}; color:{theme.ON_ACCENT}; border-radius:13px; font-weight:700;")
        row.addWidget(n, 0, Qt.AlignTop)
        t = label(text.format(**fmt), wrap=True)
        t.setTextFormat(Qt.RichText)
        t.setStyleSheet(f"color:{theme.TEXT_2}; font-size:13px;")
        row.addWidget(t, 1)
        lay.addLayout(row)
    lay.addStretch()
    return w


class SharingGuide(QDialog):
    """After it closes, `action` is "add" or "paste" if the person pressed one of the shortcut buttons."""

    def __init__(self, parent=None, start="friend"):
        super().__init__(parent)
        self.action = None
        self.setWindowTitle("How to set up sharing")
        s = Shell(self, "Share clips straight into Discord",
                  "Clipmunk posts through a channel's webhook. The server admin sets it up once; "
                  "everyone else just adds an invite.", divider=True, width=600)
        tabs = QHBoxLayout()
        tabs.setSpacing(6)
        self.group = QButtonGroup(self)
        self.stack = QStackedWidget()
        for i, (text, steps) in enumerate((("Someone sent me an invite", FRIEND_STEPS),
                                           ("I run the server", ADMIN_STEPS))):
            b = QPushButton(text)
            b.setCheckable(True)
            b.setMinimumHeight(34)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet(
                f"QPushButton {{ background:{theme.SURFACE}; border:1px solid {theme.BORDER}; border-radius:8px;"
                f" padding:0 14px; color:{theme.TEXT_2}; }}"
                f"QPushButton:checked {{ background:{theme.ACCENT_SOFT}; border-color:{theme.ACCENT_LINE};"
                f" color:{theme.TEXT}; }}")
            self.group.addButton(b, i)
            tabs.addWidget(b)
            self.stack.addWidget(_steps(steps))
        tabs.addStretch()
        s.body.addLayout(tabs)
        s.body.addWidget(self.stack, 1)
        note = label("Whoever has an invite or webhook link can post to that channel, so only share them inside "
                     "your own server. If one leaks, delete the webhook in Discord and post a new invite.",
                     "Faint", wrap=True)
        s.body.addWidget(note)

        self.paste_btn = button("Paste invite now", None, "copy")
        self.paste_btn.clicked.connect(lambda: self._done("paste"))
        self.add_btn = button("Add a channel", None, "plus")
        self.add_btn.clicked.connect(lambda: self._done("add"))
        close = button("Got it", "Primary")
        close.setDefault(True)
        close.clicked.connect(self.accept)
        s.footer.addWidget(self.paste_btn)
        s.footer.addWidget(self.add_btn)
        s.footer.addStretch()
        s.footer.addWidget(close)
        self.group.idToggled.connect(self._show)
        self.group.button(1 if start == "admin" else 0).setChecked(True)
        self.resize(640, 520)

    def _show(self, i, on):
        if on:
            self.stack.setCurrentIndex(i)
            self.paste_btn.setVisible(i == 0)
            self.add_btn.setVisible(i == 1)

    def _done(self, action):
        self.action = action
        self.accept()
