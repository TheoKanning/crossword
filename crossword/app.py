import sys

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout

from crossword.model import Model
from crossword.view import CrosswordLineEdit, SuggestionBox

FILENAME = 'saved/crossword.txt'


def start_app():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    ex = App()
    sys.exit(app.exec_())


def get_box_name(row, col):
    return "{}_{}".format(row, col)


# todo add coords to signals and get rid of this?
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

        self.across_suggestions = SuggestionBox("Across")
        self.down_suggestions = SuggestionBox("Down")

        window_layout = QHBoxLayout()
        window_layout.addWidget(self.grid_group_box)
        window_layout.addWidget(self.across_suggestions)
        window_layout.addWidget(self.down_suggestions)
        window_layout.addWidget(self.options_group_box)

        self.setLayout(window_layout)

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

        fill = QPushButton("Fill")
        fill.clicked.connect(self.fill)
        layout.addWidget(fill)

        self.options_group_box.setLayout(layout)

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

    def fill(self):
        self.model.fill()
        self.update_views()

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
        self.across_suggestions.update_suggestions(across)
        self.down_suggestions.update_suggestions(down)

