import sys
from os import path
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QPushButton, QHBoxLayout, QDialog
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import storage

FILENAME='saved/crossword.txt'
BLOCK='.'

def get_box_name(row, col):
    return "row{}_col{}".format(row, col)

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Crossword Creator'
        self.left = 2000
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
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
                text_box.setAlignment(Qt.AlignCenter)
                text_box.setObjectName(get_box_name(row, col))
                text_box.setMaxLength(1)
                layout.addWidget(text_box, row, col)

        self.grid_group_box.setLayout(layout)
        self.load_crossword()

    def create_options_layout(self):
        self.options_group_box = QGroupBox()
        layout = QVBoxLayout()

        save = QPushButton("Save")
        save.clicked.connect(self.save_crossword)
        layout.addWidget(save)

        suggestions = QLabel("Suggestions:")
        layout.addWidget(suggestions)

        self.options_group_box.setLayout(layout)

    def load_crossword(self):
        if not path.exists(FILENAME):
            return
        cross = storage.load(FILENAME)
        for row in range(0, 15):
            for col in range(0, 15):
                letter = cross[row][col]
                name = get_box_name(row, col)
                self.grid_group_box.findChild(CrosswordLineEdit, name).setText(letter)

    def save_crossword(self):
        crossword = []
        for row in range(0, 15):
            line = []
            for col in range(0, 15):
                name = get_box_name(row, col)
                letter = self.grid_group_box.findChild(CrosswordLineEdit, name).text()
                letter = ' ' if letter == '' else letter
                line.append(letter)
            crossword.append(line)
        cross = storage.save(crossword, FILENAME)

class CrosswordLineEdit(QLineEdit):

    def __init__(self, *args):
        QLineEdit.__init__(self, *args)
        self.textChanged.connect(self.on_text_changed)
        self.setAutoFillBackground(True)

    def on_text_changed(self, s):
        """
        Set text to upper case and change background color
        """
        if s.islower():
            self.setText(s.upper())
            return
        p = self.palette()
        color = Qt.black if s == BLOCK else Qt.white
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)
        self.focusNextChild()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    ex = App()
    sys.exit(app.exec_())
