import logging

from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QPainter
from PySide2.QtWidgets import QWidget

from common.context import app_context
from constants.fretboard import (FRET_NUMBER, FRET_WIDTH, INLAY_DIAMETER,
                                 NOTE_CIRCLE, NUT_OFFSET, NUT_WIDTH,
                                 OFFSET_EDGE, OFFSET_LAST_FRET, STRING_NUMBER,
                                 STRING_WIDTH, STRINGS)

logger = logging.getLogger(__name__)


class FretboardPainter(QWidget):
    def __init__(self):
        super().__init__()
        self.notes = {}

    def update_sizing(self):
        self.fret_spacing = (
            self.width() - NUT_OFFSET - NUT_WIDTH - OFFSET_LAST_FRET - FRET_WIDTH * FRET_NUMBER
        ) / FRET_NUMBER

    def paintEvent(self, event):
        self.painter = QPainter()
        self.painter.begin(self)

        self.update_sizing()
        self.paint_table()
        self.paint_frets()
        self.paint_inlays()
        self.paint_strings()
        self.paint_target_notes()

        self.painter.end()

    def paint_table(self):
        self.painter.setBrush(QColor(255, 255, 255))
        self.painter.setBrush(Qt.NoBrush)
        self.painter.drawPixmap(0, 0, app_context.maple_fretboard)
        self.painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

    def paint_frets(self):
        height = self.height()
        self.painter.drawRect(NUT_OFFSET, 0, NUT_WIDTH, height - 1)

        for fret in range(1, FRET_NUMBER + 1):
            fret_pos = self.fret_spacing * fret + FRET_WIDTH * (fret - 1) + NUT_OFFSET + NUT_WIDTH
            self.painter.drawRect(fret_pos, 0, FRET_WIDTH, height - 1)

    def draw_inlay(self, x, y):
        self.painter.drawEllipse(x, y, INLAY_DIAMETER, INLAY_DIAMETER)

    def paint_inlays(self):
        height = self.height()
        spacing_offset = NUT_OFFSET + NUT_WIDTH + (self.fret_spacing - NOTE_CIRCLE) / 2

        for fret in range(FRET_NUMBER + 1):
            x_pos = (self.fret_spacing + FRET_WIDTH) * (fret - 1) + spacing_offset
            y_pos = (height - INLAY_DIAMETER) / 2

            if not fret:
                continue

            elif fret % 12 in (3, 5, 7, 9):
                self.draw_inlay(x_pos, y_pos)

            if fret % 12 == 0:
                self.draw_inlay(x_pos, y_pos - height / 4)
                self.draw_inlay(x_pos, y_pos + height / 4)

    def paint_strings(self):
        width = self.width()
        str_height = (self.height() - (OFFSET_EDGE * 2)) / (STRING_NUMBER - 1)

        for i in range(STRING_NUMBER):
            self.painter.drawRect(
                0,
                OFFSET_EDGE + (str_height * i) - (STRING_WIDTH / 2),
                width - 1,
                STRING_WIDTH
            )

    def paint_target_notes(self):
        str_height = (self.height() - OFFSET_EDGE * 2) / (STRING_NUMBER - 1)
        spacing_offset = NUT_OFFSET + NUT_WIDTH + (self.fret_spacing - NOTE_CIRCLE) / 2

        for string_index, string_semitones in enumerate(STRINGS):
            string_pos = OFFSET_EDGE + (str_height * string_index) - (NOTE_CIRCLE / 2)

            if string_semitones in self.notes:
                self.painter.setBrush(self.notes.get(string_semitones))
                self.painter.drawEllipse(
                    NUT_OFFSET + (NUT_WIDTH - NOTE_CIRCLE) / 2,
                    string_pos, NOTE_CIRCLE, NOTE_CIRCLE
                )

            for fret in range(1, FRET_NUMBER + 1):
                fretted_note = (string_semitones + fret) % 12
                if fretted_note in self.notes:
                    self.painter.setBrush(self.notes.get(fretted_note))
                    self.painter.drawEllipse(
                        (self.fret_spacing + FRET_WIDTH) * (fret - 1) + spacing_offset,
                        string_pos, NOTE_CIRCLE, NOTE_CIRCLE
                    )
