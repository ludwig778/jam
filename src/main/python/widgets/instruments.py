from functools import partial
import logging

from common.utils import BlockSignals

from api.instruments import instruments_api
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QCheckBox, QGridLayout, QLabel, QPushButton, QWidget, QComboBox

logger = logging.getLogger(__name__)

ACTIVE_WIDTH = 40
PREVIEW_WIDTH = 45


class InstrumentWidget(QWidget):
    CHANNEL = 0
    def __init__(self, **kwargs):
        super().__init__()
        self.channel = self.CHANNEL
        InstrumentWidget.CHANNEL += 1
        self.setup_ui()
        self.setup_instruments(**kwargs)

    def setup_instruments(self, active=None, preview=None, instrument=None, player=None):
        instruments_api.create(self.channel)

        if active:
            #self.set_active(active)
            self.check_active.setChecked(True)
        if preview:
            self.check_preview.setChecked(True)
        if instrument:
            self.combo_inst.setCurrentText(instrument)
        if player:
            self.combo_player.setCurrentText(player)

    def set_instrument(self, name):
        print("INSTRUMENT CHANGED")

        #if setup:
        #    with BlockSignals(self.combo_inst):
        #        self.combo_inst.setCurrentText(name)

        with BlockSignals(self.combo_player):
            self.combo_player.clear()

        players = list(instruments_api.get_players(name).keys())
        self.combo_player.addItems(players)

        instruments_api.set_instrument(self.channel, name)

    def set_player(self, name):
        print("PLAYER CHANGED")
        print(name)
        #if setup:
        #    with BlockSignals(self.combo_player):
        #        self.combo_player.setCurrentText(name)

        instruments_api.set_player(self.channel, name)

    def set_active(self, state):
        self.check_preview.setEnabled(state)
        self.combo_inst.setEnabled(state)
        self.combo_player.setEnabled(state)

        instruments_api.set_active(self.channel, state)

    def set_preview(self, state):
        instruments_api.set_preview(self.channel, state)

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.check_active = QCheckBox()
        self.check_preview = QCheckBox()
        self.combo_inst = QComboBox()
        self.combo_player = QComboBox()

    def modify_widgets(self):
        self.check_active.setFixedWidth(ACTIVE_WIDTH)
        self.check_preview.setFixedWidth(PREVIEW_WIDTH)
        self.combo_inst.addItems(instruments_api.names)

    def create_layouts(self):
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.check_active)
        self.main_layout.addWidget(self.check_preview)
        self.main_layout.addWidget(self.combo_inst)
        self.main_layout.addWidget(self.combo_player)

    def setup_connections(self):
        self.check_active.toggled.connect(self.set_active)
        self.check_preview.toggled.connect(self.set_preview)
        self.combo_inst.currentTextChanged.connect(self.set_instrument)
        self.combo_player.currentTextChanged.connect(self.set_player)

INSTRUMENTS = [
    {"active": False, "preview": True, "instrument": "Guitar"},
    {"active": False, "preview": False, "instrument": "Drums"},
    {"active": True, "preview": False, "instrument": "Guitar", "player": "Triads"},
    {}
]

class InstrumentsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

        for instrument in INSTRUMENTS:
            widget = InstrumentWidget(**instrument)
            self.instruments_layout.addWidget(widget)

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.active_label = QLabel("Active")
        self.preview_label = QLabel("Preview")
        self.inst_label = QLabel("Instrument")
        self.player_label = QLabel("Player")

    def modify_widgets(self):
        self.active_label.setFixedWidth(ACTIVE_WIDTH)
        self.preview_label.setFixedWidth(PREVIEW_WIDTH)

    def create_layouts(self):
        self.main_layout = QVBoxLayout()
        self.labels_layout = QHBoxLayout()
        self.instruments_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def add_widgets_to_layouts(self):
        self.labels_layout.addWidget(self.active_label)
        self.labels_layout.addWidget(self.preview_label)
        self.labels_layout.addWidget(self.inst_label)
        self.labels_layout.addWidget(self.player_label)

        self.main_layout.addLayout(self.labels_layout)
        self.main_layout.addLayout(self.instruments_layout)
        self.main_layout.addStretch(0)

    def setup_connections(self):
        pass
