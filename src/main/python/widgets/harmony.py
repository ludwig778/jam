import logging

from functools import partial

from PySide2.QtWidgets import (QGridLayout, QLabel, QPushButton, QVBoxLayout,
                               QWidget)

from api.harmony import harmony_api
from common.callbacks import update_callback
from common.state import state
from widgets.player import preview_player


logger = logging.getLogger(__name__)


class HarmonyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

        update_callback.register(self)

    def __str__(self):
        return "<HarmonyWidget>"

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()

    def create_widgets(self):
        self.chromatic_labels = [QLabel() for _ in range(12)]
        self.diatonic_labels = [QLabel() for _ in range(7)]

        self.chromatic_buttons = self.create_buttons(
            harmony_api.chromatic_display_chords,
            self.chromatic_button_clicked,
            12
        )

        self.diatonic_buttons = self.create_buttons(
            harmony_api.diatonic_chords.keys(),
            self.diatonic_button_clicked,
            7
        )

    def create_buttons(self, chord_types, handler, num):
        mapping = {}
        for chord_type in chord_types:
            buttons = []
            for index in range(num):
                button = QPushButton()
                button.index = index
                button.chord_type = chord_type

                button.clicked.connect(partial(
                    handler,
                    button
                ))
                buttons.append(button)

            mapping[chord_type] = buttons
        return mapping

    def modify_widgets(self):
        for label, degree in zip(
            self.diatonic_labels,
            harmony_api.diatonic_degrees
        ):
            label.setText(degree)

    def create_layouts(self):
        self.main_layout = QVBoxLayout()

        self.chromatic_grid = QGridLayout()
        self.diatonic_grid = QGridLayout()

        self.main_layout.addLayout(self.chromatic_grid)
        self.main_layout.addLayout(self.diatonic_grid)

        self.setLayout(self.main_layout)

    def add_widgets_to_layouts(self):
        for col, label in enumerate(self.chromatic_labels):
            self.chromatic_grid.addWidget(label, 0, col)

        for col, label in enumerate(self.diatonic_labels):
            self.diatonic_grid.addWidget(label, 0, col)

        for row, buttons in enumerate(self.chromatic_buttons.values(), start=1):
            for col, button in enumerate(buttons):
                self.chromatic_grid.addWidget(button, row, col)

        for row, buttons in enumerate(self.diatonic_buttons.values(), start=1):
            for col, button in enumerate(buttons):
                self.diatonic_grid.addWidget(button, row, col)

    def chromatic_button_clicked(self, button):
        logger.debug(f"Chromatic button clicked {button.chord_type}:{button.index}")
        chord_data = (button.chord_type, button.index)
        state.preview_chord = state.current_chord = chord_data
        update_callback(self)

        preview_player.play_note()

    def diatonic_button_clicked(self, button):
        logger.debug(f"Diatonic button clicked {button.chord_type}:{button.index}")
        chord_data = (button.chord_type, button.index)
        state.preview_chord = state.current_chord = chord_data
        update_callback(self)

        preview_player.play_note()

    def update_chromatic_label_display(self):
        for label, degree in zip(
            self.chromatic_labels,
            harmony_api.chromatic_degrees
        ):
            label.setText(f"{degree}")

    def update_diatonic_grid_display(self):
        for buttons in self.diatonic_buttons.values():
            for button in buttons:
                button.setEnabled(state.current_scale.is_diatonic)

    def update_display(self):
        logger.debug(f"Update scale from {self}")

        self.update_chromatic_label_display()
        self.update_diatonic_grid_display()

        harmony_api.reset_preview_chord_type()
