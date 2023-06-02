import re

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QGroupBox, QSizePolicy
from PyQt6.QtWidgets import QLineEdit, QVBoxLayout, QLabel, QScrollArea


from crossword.model import Background

BACKGROUND_COLORS = {
    Background.WHITE: "white",
    Background.BLACK: "black",
    Background.HIGHLIGHT: "#a7faf2"
}


class SuggestionBox(QGroupBox):
    """
    Layout that has a title and a scrollable list of word/score suggestions
    """

    def __init__(self, title):
        QGroupBox.__init__(self)
        layout = QVBoxLayout()

        label = QLabel(title)
        label.setObjectName("suggestion_box_label")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)

        self.suggestions = QLabel()
        scroll.setWidget(self.suggestions)
        layout.addWidget(scroll, )

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
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        policy = QSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding)
        self.setSizePolicy(policy)

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

        background = BACKGROUND_COLORS[square.background]
        text_color = "black" if square.bold else "gray"

        # not sure why setting a style in crossword.qss prevents changing background color later
        self.setStyleSheet(f"""
        background-color: {background};
        color: {text_color};
        border: 1px solid #000;
        font-size: 16px;
        """)
