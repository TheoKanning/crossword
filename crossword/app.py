import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QPushButton, QHBoxLayout, QDialog
from PyQt5.QtWidgets import QLineEdit, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Crossword Creator'
        self.left = 10
        self.top = 10
        self.width = 480
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        windowLayout = QHBoxLayout()
        windowLayout.addWidget(self.gridGroupBox)
        self.setLayout(windowLayout)

        self.show()

    def createGridLayout(self):
        self.gridGroupBox = QGroupBox()
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setRowStretch(0, 0)

        for row in range(0,15):
            for col in range(0,15):
                text_box = QLineEdit()
                text_box.setAlignment(Qt.AlignCenter)
                text_box.setMaximumSize(30,30)
                text_box.setMaxLength(1)
                text_box.setInputMask('A')
                layout.addWidget(text_box, row, col)

        self.gridGroupBox.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
