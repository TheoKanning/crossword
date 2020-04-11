import sys
from os import path
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QPushButton, QHBoxLayout, QDialog
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal
import dictionary
from model import Puzzle, Background
import storage

FILENAME='saved/crossword.txt'

def get_box_name(row, col):
    return "{}_{}".format(row, col)

def get_coords_from_name(name):
    return [int(i) for i in name.split('_')]

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Crossword Creator'
        self.left = 2000
        self.top = 10
        self.width = 640
        self.height = 480
        self.puzzle = Puzzle()
        self.init_ui()
        self.load_crossword()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.create_grid_layout()
        self.create_options_layout()

        windowLayout = QHBoxLayout()
        windowLayout.addWidget(self.grid_group_box)
        windowLayout.addWidget(self.options_group_box)
        self.setLayout(windowLayout)

        self.show()

    def create_grid_layout(self):
        self.grid_group_box = QGroupBox()
        self.grid_group_box.setMaximumSize(450, 450)
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setRowStretch(0, 0)

        for row in range(0,15):
            for col in range(0,15):
                text_box = CrosswordLineEdit()
                text_box.setObjectName(get_box_name(row, col))
                text_box.edited.connect(self.on_box_edited)
                text_box.focused.connect(self.on_box_focused)
                layout.addWidget(text_box, row, col)

        self.grid_group_box.setLayout(layout)

    def create_options_layout(self):
        self.options_group_box = QGroupBox()
        layout = QVBoxLayout()

        save = QPushButton("Save")
        save.clicked.connect(self.save_crossword)
        layout.addWidget(save)

        self.suggestions = QLabel("Suggestions:")
        layout.addWidget(self.suggestions)

        self.options_group_box.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.puzzle.toggle_orientation()
            self.update_views()

    def load_crossword(self):
        cross = None
        if path.exists(FILENAME):
            cross = storage.load(FILENAME)
        self.puzzle = Puzzle(cross)
        self.update_views()

    def save_crossword(self):
        cross = storage.save(self.puzzle.squares, FILENAME)

    def on_box_edited(self, name, text):
        coords = get_coords_from_name(name)
        self.puzzle.update_square(coords[0], coords[1], text)
        self.update_views()

    def on_box_focused(self, name):
        row, col = get_coords_from_name(name)
        self.puzzle.update_focus(row, col)
        self.update_views()

    def update_views(self):
        for row in range(0, self.puzzle.size):
            for col in range(0, self.puzzle.size):
                square = self.puzzle.get_square(row, col)
                name = get_box_name(row, col)
                self.grid_group_box.findChild(CrosswordLineEdit, name).update(square)

        self.update_suggestions()

    def update_suggestions(self):
        (row, col) = self.puzzle.focus
        word = self.puzzle.get_word(row, col)
        suggestions = [': '.join(w) for w in dictionary.search(word)]
        self.suggestions.setText('\n'.join(suggestions))

class CrosswordLineEdit(QLineEdit):

    edited = pyqtSignal(str, str) # name, text
    focused = pyqtSignal(str)

    def __init__(self, *args):
        QLineEdit.__init__(self, *args)
        self.textEdited.connect(self.on_text_changed)
        self.setAutoFillBackground(True)
        self.setAlignment(Qt.AlignCenter)
        self.setMaxLength(1)

    def focusInEvent(self, e):
        self.focused.emit(self.objectName())
        super().focusInEvent(e)

    def on_text_changed(self, s):
        self.edited.emit(self.objectName(), s.upper())

    def update(self, square):
        self.setText(square.text)
        if square.focused:
            self.setFocus()
        if square.background == Background.WHITE:
            self.set_background_color(Qt.white)
        if square.background == Background.BLACK:
            self.set_background_color(Qt.black)
        if square.background == Background.YELLOW:
            self.set_background_color(Qt.yellow)

    def set_background_color(self, color):
        p = self.palette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    ex = App()
    sys.exit(app.exec_())
