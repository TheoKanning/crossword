import re
import sys

from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QVBoxLayout, QLabel, QScrollArea

from crossword.model import Model, Background

FILENAME = 'saved/crossword.txt'


def start_app():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    ex = App()
    sys.exit(app.exec_())


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
        self.width = 1000
        self.height = 480
        self.model = Model(filename=FILENAME, size=15)
        self.init_ui()
        self.update_views()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.create_grid_layout()
        self.create_options_layout()

        across_group_box, across_suggestions = self.create_suggestions_layout("Across")
        self.across_suggestions = across_suggestions
        down_group_box, down_suggestions = self.create_suggestions_layout("Down")
        self.down_suggestions = down_suggestions

        windowLayout = QHBoxLayout()
        windowLayout.addWidget(self.grid_group_box)
        windowLayout.addWidget(across_group_box)
        windowLayout.addWidget(down_group_box)
        windowLayout.addWidget(self.options_group_box)

        self.setLayout(windowLayout)

        self.show()

    def create_grid_layout(self):
        self.grid_group_box = QGroupBox()
        self.grid_group_box.setMaximumSize(450, 450)
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setRowStretch(0, 0)

        for row in range(0, 15):
            for col in range(0, 15):
                text_box = CrosswordLineEdit()
                text_box.setObjectName(get_box_name(row, col))
                text_box.edited.connect(self.on_box_edited)
                text_box.focused.connect(self.on_box_focused)
                text_box.installEventFilter(self)
                layout.addWidget(text_box, row, col)

        self.grid_group_box.setLayout(layout)

    def create_options_layout(self):
        self.options_group_box = QGroupBox()
        layout = QVBoxLayout()

        save = QPushButton("Save")
        save.clicked.connect(self.save_crossword)
        layout.addWidget(save)

        self.options_group_box.setLayout(layout)

    # todo put this into a separate class?
    def create_suggestions_layout(self, label_text):
        suggestion_box = QGroupBox()
        layout = QVBoxLayout()

        label = QLabel(label_text)
        layout.addWidget(label)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)

        suggestions = QLabel()
        scroll.setWidget(suggestions)
        layout.addWidget(scroll)

        suggestion_box.setLayout(layout)
        return suggestion_box, suggestions

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.model.toggle_orientation()
            self.update_views()

    def eventFilter(self, obj, event):
        # filter to keep LineEdits from consuming arrow keys
        if event.type() == QEvent.KeyPress:
            if event.key() in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Right, Qt.Key_Left]:
                if event.key() == Qt.Key_Up:
                    self.model.move_up()
                elif event.key() == Qt.Key_Down:
                    self.model.move_down()
                elif event.key() == Qt.Key_Left:
                    self.model.move_left()
                elif event.key() == Qt.Key_Right:
                    self.model.move_right()
                self.update_views()
                return True
        return False

    def save_crossword(self):
        self.model.save(FILENAME)

    def on_box_edited(self, name, text):
        coords = get_coords_from_name(name)
        self.model.update_square(coords[0], coords[1], text)
        self.update_views()

    def on_box_focused(self, name):
        row, col = get_coords_from_name(name)
        self.model.update_focus(row, col)
        self.update_views()

    def update_views(self):
        for row in range(0, self.model.size):
            for col in range(0, self.model.size):
                square = self.model.get_square(row, col)
                name = get_box_name(row, col)
                self.grid_group_box.findChild(CrosswordLineEdit, name).update(square)

        self.update_suggestions()

    def update_suggestions(self):
        across, down = self.model.get_suggestions()
        suggestions = [': '.join(w) for w in across]
        self.across_suggestions.setText('\n'.join(suggestions))
        suggestions = [': '.join(w) for w in down]
        self.down_suggestions.setText('\n'.join(suggestions))


class CrosswordLineEdit(QLineEdit):
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
        pattern = re.compile('[^a-zA-z\.]')  # remove anything except letters and periods
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
        if square.background == Background.BLACK:
            self.set_background_color(Qt.black)
        if square.background == Background.YELLOW:
            self.set_background_color(Qt.yellow)

    def set_background_color(self, color):
        p = self.palette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)
