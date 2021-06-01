import re

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QLabel, QScrollArea

from crossword.model import Background


class SuggestionBox(QGroupBox):
    """
    Layout that has a title and a scrollable list of word/score suggestions
    """

    def __init__(self, title):
        QGroupBox.__init__(self)
        layout = QVBoxLayout()

        label = QLabel(title)
        layout.addWidget(label)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)

        self.suggestions = QLabel()
        scroll.setWidget(self.suggestions)
        layout.addWidget(scroll)

        self.setLayout(layout)

    def update_suggestions(self, suggestions):
        """
        Takes a list of (word, score) tuples and presents them in the suggestion box
        """
        suggestions = [': '.join(w) for w in suggestions]
        self.suggestions.setText('\n'.join(suggestions))


class CrosswordLineEdit(QLineEdit):
    """
    Crossword-specific LineEdit with input filters
    """
    edited = pyqtSignal(str, str)  # name, text
    focused = pyqtSignal(str)

    def __init__(self, *args):
        QLineEdit.__init__(self, *args)
        self.textEdited.connect(self.on_text_changed)
        self.setAutoFillBackground(True)
        self.setAlignment(Qt.AlignCenter)

    def focusInEvent(self, e):
        self.focused.emit(self.objectName())
        super().focusInEvent(e)

    def on_text_changed(self, s):
        pattern = re.compile('[^a-zA-Z.]')  # remove anything except letters and periods
        s = pattern.sub('', s)
        if len(s) > 1:
            s = s[-1]
        self.edited.emit(self.objectName(), s.upper())

    def update(self, square):
        self.setText(square.text)
        if square.focused:
            self.setFocus()

        if square.background == Background.WHITE:
            self.set_background_color(Qt.white)
        elif square.background == Background.BLACK:
            self.set_background_color(Qt.black)
        elif square.background == Background.YELLOW:
            self.set_background_color(Qt.yellow)

        if square.bold:
            self.setStyleSheet("color: black")
        else:
            self.setStyleSheet("color: gray")

    def set_background_color(self, color):
        p = self.palette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)
