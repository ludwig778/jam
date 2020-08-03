from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QPainter
from PySide2.QtWidgets import QWidget

from constants.keyboard import (A_FIRST, BLACK_KEY_RATIO, NOTE_CIRCLE,
                                OCTAVE_NUMBER)


class KeyboardPainter(QWidget):
    def __init__(self):
        super().__init__()
        self.notes = {}

    def paintEvent(self, event):
        self.painter = QPainter()
        self.painter.begin(self)

        self.update_sizing()
        self.paint_base()
        self.paint_white_keys()
        self.paint_black_keys()
        self.paint_target_notes()

        self.painter.end()

    def update_sizing(self):
        self.white_key_num = OCTAVE_NUMBER * 7 + 1
        if A_FIRST:
            self.white_key_num += 2

        self.white_key_width = self.width() / self.white_key_num
        self.black_key_width = self.white_key_width * BLACK_KEY_RATIO
        self.half_black_key_width = self.black_key_width / 2

    def paint_base(self):
        width, height = self.width(), self.height()
        self.painter.setBrush(Qt.NoBrush)
        self.painter.setBrush(QColor(255, 255, 255))
        self.painter.drawRect(0, 0, width - 1, height - 1)

    def paint_white_keys(self):
        height = self.height()
        self.painter.setBrush(QColor(255, 255, 255))

        for key_num in range(1, self.white_key_num):
            x_pos = self.white_key_width * key_num
            self.painter.drawLine(x_pos, 0, x_pos, height - 1)

    def paint_black_keys(self):
        height = self.height()
        self.painter.setBrush(QColor(0, 0, 0))

        for key_num in range(1, self.white_key_num):
            if (key_num + 5 if A_FIRST else key_num) % 7 in [0, 3]:
                continue

            black_key_offset = key_num * self.white_key_width - self.half_black_key_width
            self.painter.drawRect(black_key_offset, 0, self.black_key_width, height * 0.7)

    def paint_target_notes(self):
        height = self.height()
        key_offset = 6 if A_FIRST else 1
        mapping = {0: 1, 1: 3, 2: 4, 3: 6, 4: 8, 5: 9, 6: 11}

        for key_num in range(1, self.white_key_num):
            note_index = (key_num + key_offset) % 7
            note_semitones = mapping.get(note_index)
            if note_semitones in self.notes:
                self.painter.setBrush(self.notes.get(note_semitones))
                self.painter.drawEllipse(
                    key_num * self.white_key_width - (self.white_key_width + NOTE_CIRCLE) / 2,
                    height * 0.84,
                    NOTE_CIRCLE,
                    NOTE_CIRCLE
                )

            if (key_num + key_offset - 1) % 7 in [0, 3]:
                continue
            note_semitones = (note_semitones + 1) % 12
            if note_semitones in self.notes:
                self.painter.setBrush(self.notes.get(note_semitones))
                self.painter.drawEllipse(
                    key_num * self.white_key_width - NOTE_CIRCLE / 2,
                    height * 0.60,
                    NOTE_CIRCLE,
                    NOTE_CIRCLE
                )
