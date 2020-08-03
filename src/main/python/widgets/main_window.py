import logging

from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import (QMainWindow, QShortcut, QTabWidget, QVBoxLayout,
                               QWidget)

from api.chord_progression import chord_prog_api
from api.harmony import harmony_api
from api.scale import scale_api
from common.callbacks import update_callback
from common.context import app_context
from common.state import state
from constants.app import BASE_BPM
from widgets.chord_progression.main import ChordProgressionWidget
from widgets.display.main import DisplayWidget
from widgets.harmony import HarmonyWidget
from widgets.instruments import InstrumentsWidget
from widgets.scale import ScaleWidget
from widgets.sequencer import SequencerWidget

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindow")
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.setup_state()
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.add_actions_to_toolbar()
        self.setup_connections()
        self.setup_app()

    def setup_state(self):
        state.bpm = BASE_BPM

    def create_widgets(self):
        self.main_widget = QWidget()

        self.display_widget = DisplayWidget()
        self.harmony_widget = HarmonyWidget()
        self.instruments_widget = InstrumentsWidget()

        self.scale_widget = ScaleWidget()
        self.sequencer_widget = SequencerWidget()
        self.chord_prog_widget = ChordProgressionWidget()

    def modify_widgets(self):
        css_file = app_context.stylesheet
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

    def create_layouts(self):
        self.main_layout = QVBoxLayout(self.main_widget)

        self.tab_layout = QTabWidget()
        self.main_layout.addWidget(self.tab_layout)

    def add_widgets_to_layouts(self):
        self.setCentralWidget(self.main_widget)

        self.tab_layout.addTab(self.instruments_widget, "Instruments")
        self.tab_layout.addTab(self.harmony_widget, "Harmony")
        self.tab_layout.addTab(self.display_widget, "Display")

        self.main_layout.addWidget(self.scale_widget)
        self.main_layout.addWidget(self.sequencer_widget)
        self.main_layout.addWidget(self.chord_prog_widget)

    def add_actions_to_toolbar(self):
        pass

    def setup_connections(self):
        QShortcut(QKeySequence("e"), self, self.close_app)
        QShortcut(QKeySequence("SPACE"), self, self.sequencer_widget.run)

    def setup_app(self):
        scale = chord_prog_api.scale
        chord = chord_prog_api.chord

        scale_api.set_scale(scale.name, scale.root.note_name)
        harmony_api.set_chord(*chord)

        update_callback()

    def close_app(self):
        self.sequencer_widget.stop()
        self.close()
