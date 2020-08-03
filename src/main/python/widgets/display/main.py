import logging

from PySide2.QtGui import QColor
from PySide2.QtWidgets import QVBoxLayout, QWidget

from api.harmony import harmony_api
from common.callbacks import update_callback
from common.state import state
from .fretboard import FretboardPainter
from .keyboard import KeyboardPainter

logger = logging.getLogger(__name__)


class DisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

        update_callback.register(self)

    def __str__(self):
        return "<DisplayWidget>"

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.fretboard = FretboardPainter()
        self.keyboard = KeyboardPainter()

    def modify_widgets(self):
        pass

    def create_layouts(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.fretboard)
        self.main_layout.addWidget(self.keyboard)

    def setup_connections(self):
        pass

    @staticmethod
    def get_colors_by_notes(scale, chord):
        s_notes, c_notes = scale.notes, chord.notes if chord else []

        ret = {}
        RED = QColor(255, 0, 0)
        DARK_RED = QColor(180, 0, 0)
        GREEN = QColor(0, 255, 0)
        WHITE = QColor(255, 255, 255)

        for s_note in s_notes:
            if s_note in c_notes:
                ret[s_note.semitones] = RED
            else:
                ret[s_note.semitones] = DARK_RED

        if len(c_notes) > 0:
            ret[c_notes[0].semitones] = WHITE

        for c_note in c_notes:
            if c_note not in s_notes:
                ret[c_note.semitones] = GREEN

        return ret

    def update_display(self):
        logger.debug(f"Update scale from {self}")

        scale = state.current_scale
        chord = harmony_api.get_chord(
            state.current_scale,
            *state.current_chord
        )

        c_mapping = self.get_colors_by_notes(scale, chord)

        self.fretboard.notes = c_mapping
        self.keyboard.notes = c_mapping
        self.fretboard.update()
        self.keyboard.update()
