import logging
from functools import lru_cache

from PySide2.QtWidgets import QLabel, QAbstractItemView, QHBoxLayout, QVBoxLayout, QPushButton, QListView, QListWidget, QWidget, QListWidgetItem

from api.harmony import harmony_api
from api.scale import scale_api
from common.utils import BlockSignals
from common.state import state

logger = logging.getLogger(__name__)


class ScaleContainer(QWidget):
    def __init__(self, scale):
        super().__init__()

        self.scale = scale

        self.setup_ui()
        self.update_display()

    def __repr__(self):
        return self.scale.__repr__()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()

    def create_widgets(self):
        self.text_up = QLabel()
        self.text_down = QLabel()

    def modify_widgets(self):
        self.text_up.setStyleSheet('''
            color: rgb(0, 0, 255);
            qproperty-alignment: AlignCenter;
        ''')
        self.text_down.setStyleSheet('''
            color: rgb(255, 0, 0);
            qproperty-alignment: AlignCenter;
        ''')

    def create_layouts(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.text_up)
        self.main_layout.addWidget(self.text_down)

    def update_display(self):
        self.text_up.setText(f"{self.scale.scale_name}")
        self.text_down.setText(" → ".join([
            harmony_api.get_chord(self.scale, *chord).display
            for chord in self.scale.chords
        ]))

    def update(self, scale):
        self.scale = scale
        self.update_display()

class ChordContainer(QWidget):
    def __init__(self, scale, chord):
        super().__init__()

        self.scale = scale
        self.chord = chord

        self.setup_ui()
        self.update_display()

    def __repr__(self):
        return f"{self.chord}"

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()

    def create_widgets(self):
        self.text = QLabel()

    def modify_widgets(self):
        self.text.setStyleSheet('''
            color: rgb(0, 0, 255);
            qproperty-alignment: AlignCenter;
        ''')

    def create_layouts(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.text)

    @property
    def name(self):
        return harmony_api.get_chord(self.scale, *self.chord).chord_name

    @property
    def display_string(self):
        chord_type, chord_index = self.chord
 
        if chord_type in harmony_api.diatonic_chords:
            degree = harmony_api.diatonic_degrees[chord_index]
            return f"{degree}"
        else:
            degree = harmony_api.chromatic_degrees[chord_index]
            return f"{degree}{chord_type}"
    #@lru_cache
    #def get_name(self):
    #    pass

    def update_display(self):
        self.text.setText(f"{self.name}")

    def update(self, scale=None, chord=None):
        if scale:
            self.scale = scale

        if chord:
            self.chord = chord

        self.update_display()
