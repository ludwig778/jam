import logging

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSpinBox, QWidget

from api.chord_progression import chord_prog_api
from api.midi import midi_api
from common.callbacks import update_callback
from common.state import state
from constants.app import BASE_BPM
from widgets.player import player

logger = logging.getLogger(__name__)


class SequencerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

        update_callback.register(self)

    def __str__(self):
        return "<SequencerWidget>"

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.bpm_label = QLabel("Bpm:")
        self.bpm_edit = QSpinBox()
        self.start_btn = QPushButton("start")
        self.stop_btn = QPushButton("stop")

    def modify_widgets(self):
        self.bpm_edit.setRange(30, 1000)
        self.bpm_edit.setValue(state.bpm)

    def create_layouts(self):
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.bpm_label)
        self.main_layout.addWidget(self.bpm_edit)
        self.main_layout.addWidget(self.start_btn)
        self.main_layout.addWidget(self.stop_btn)

    def setup_connections(self):
        self.start_btn.clicked.connect(self.run)
        self.stop_btn.clicked.connect(self.stop)
        self.bpm_edit.valueChanged.connect(self.set_bpm)

    def run(self):
        if not player.running:
            logger.critical("Start sequencer")
            player.start()
            player.running = True

    def stop(self):
        if player.running:
            logger.critical("Stop sequencer")
            player.terminate()
            player.running = False
            for c in range(4):
                midi_api.clean(channel=c)

    def set_bpm(self, value):
        logger.debug(f"Set BPM to {value}")
        state.bpm = value

    def update_display(self):
        pass #logger.debug(f"Update scale from {self}")
