import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QPushButton, QHBoxLayout, QDialog
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

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

        self.createGridLayout()
        self.createOptionsLayout()

        windowLayout = QHBoxLayout()
        windowLayout.addWidget(self.gridGroupBox)
        windowLayout.addWidget(self.optionsGroupBox)
        self.setLayout(windowLayout)

        self.show()

    def createGridLayout(self):
        self.gridGroupBox = QGroupBox()
        self.gridGroupBox.setMaximumSize(450, 450)
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setRowStretch(0, 0)

        for row in range(0,15):
            for col in range(0,15):
                text_box = CrosswordLineEdit()
                text_box.setAlignment(Qt.AlignCenter)
                text_box.setMaxLength(1)
                layout.addWidget(text_box, row, col)

        self.gridGroupBox.setLayout(layout)

    def createOptionsLayout(self):
        self.optionsGroupBox = QGroupBox()
        layout = QVBoxLayout()
        self.optionsGroupBox.setLayout(layout)

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
        color = Qt.black if s == '#' else Qt.white
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)
        self.focusNextChild()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
