import logging

from PySide2.QtWidgets import QLabel, QAbstractItemView, QHBoxLayout, QVBoxLayout, QPushButton, QListView, QListWidget, QWidget, QListWidgetItem

from api.chord_progression import chord_prog_api
from api.harmony import harmony_api
from api.scale import scale_api
from common.utils import BlockSignals
from common.state import state
from common.callbacks import update_callback
from .list_widget import ProgressionListWidget
from .harmony_items import ScaleContainer, ChordContainer

logger = logging.getLogger(__name__)


class ChordProgressionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

        for scale in chord_prog_api.scales:
            self.scale_list.add_item(
                ScaleContainer(scale)
            )

        for chord in chord_prog_api.chords:
            self.chord_list.add_item(
                ChordContainer(chord_prog_api.scale, chord)
            )

        self.scale_list.set_active_item(0)
        update_callback.register(self)

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.scale_list = ProgressionListWidget()
        self.chord_list = ProgressionListWidget()

        self.add_scale_button = QPushButton("add scale")
        self.update_scale_button = QPushButton("update scale")
        self.remove_scale_button = QPushButton("remove scale")

        self.add_chord_button = QPushButton("add chord")
        self.update_chord_button = QPushButton("update chord")
        self.remove_chord_button = QPushButton("remove chord")

        self.clear_chords_button = QPushButton("clear chords")

    def modify_widgets(self):
        self.scale_list.setFixedHeight(70)
        self.chord_list.setFixedHeight(45)

    def create_layouts(self):
        self.main_layout = QVBoxLayout()

        self.scale_buttons_layout = QHBoxLayout()
        self.chord_buttons_layout = QHBoxLayout()

        self.main_layout.addLayout(self.scale_buttons_layout)
        self.main_layout.addLayout(self.chord_buttons_layout)

        self.setLayout(self.main_layout)

    def add_widgets_to_layouts(self):
        self.main_layout.insertWidget(1, self.scale_list)
        self.main_layout.insertWidget(3, self.chord_list)

        self.scale_buttons_layout.addWidget(self.add_scale_button)
        self.scale_buttons_layout.addWidget(self.update_scale_button)
        self.scale_buttons_layout.addWidget(self.remove_scale_button)

        self.chord_buttons_layout.addWidget(self.add_chord_button)
        self.chord_buttons_layout.addWidget(self.update_chord_button)
        self.chord_buttons_layout.addWidget(self.remove_chord_button)
        self.chord_buttons_layout.addWidget(self.clear_chords_button)

    def setup_connections(self):
        self.add_scale_button.clicked.connect(self.add_scale)
        self.add_chord_button.clicked.connect(self.add_chord)
        self.update_scale_button.clicked.connect(self.update_scale)
        self.update_chord_button.clicked.connect(self.update_chord)
        self.remove_scale_button.clicked.connect(self.remove_scale)
        self.remove_chord_button.clicked.connect(self.remove_chord)
        self.clear_chords_button.clicked.connect(self.clear_chords)

        self.scale_list.model().rowsMoved.connect(self.drag_and_drop_scale)
        self.chord_list.model().rowsMoved.connect(self.drag_and_drop_chord)

        self.scale_list.itemSelectionChanged.connect(self.change_scale)
        self.chord_list.itemSelectionChanged.connect(self.change_chord)

    def drag_and_drop_scale(self, *args):
        start, end = args[1], args[4]
        if start < end:
            end -= 1
        chord_prog_api.switch_scale(start, end)

        _, widget = self.scale_list.get_active_tuple()
        widget.update_display()

        logger.critical(f"scale drop {start} = {end}")

    def drag_and_drop_chord(self, *args):
        start, end = args[1], args[4]
        if start < end:
            end -= 1
        chord_prog_api.switch_chord(start, end)

        _, widget = self.scale_list.get_active_tuple()
        widget.update_display()

        logger.critical(f"chord drop {start} = {end}")

    def add_scale(self):
        logger.debug("add scale")
        logger.debug(chord_prog_api.indexes)
        logger.debug(self.scale_list.currentRow())
        scale = chord_prog_api.add_scale()
        self.scale_list.add_item(ScaleContainer(scale), chord_prog_api.index.scale)

        self.scale_list.set_active_item(
            chord_prog_api.index.scale
        )
        self.change_scale()
        logger.debug(self.scale_list.currentRow())
        logger.critical(f"PROG {chord_prog_api._prog}")

    def update_scale(self):
        logger.debug("update scale")
        
        chord_prog_api.update_scale()
        
        item = self.scale_list.currentItem()
        widget = self.scale_list.itemWidget(item)
        widget.update(scale=chord_prog_api.scale)
        
        self.scale_list.update_item()

        scale = chord_prog_api.scale

        #for i in range(self.chord_list.count()):
        for i, chord in enumerate(chord_prog_api.chords):
            item = self.chord_list.item(i)
            widget = self.chord_list.itemWidget(item)

            widget.update(scale=scale, chord=chord)

            item.setSizeHint(widget.sizeHint())

    def remove_scale(self):
        logger.debug("remove scale")
        if chord_prog_api.remove_scale():
            self.scale_list.remove_item()

            self.scale_list.set_active_item(
                chord_prog_api.index.scale
            )
            self.change_scale()

        logger.critical(chord_prog_api._prog)
        logger.critical(chord_prog_api.index.scale)

    def change_scale(self):
        row = self.scale_list.currentRow()
        chord_prog_api.index.scale = row
        chord_prog_api.index.chord = 0

        item = self.scale_list.currentItem()
        widget = self.scale_list.itemWidget(item)

        state.current_scale = widget.scale

        with BlockSignals(self.chord_list):
            self.chord_list.clear()
    
        for chord in chord_prog_api.chords:
            self.chord_list.add_item(
                ChordContainer(widget.scale, chord)
            )

        logger.debug(f"change scale {widget.scale} {row}")

        self.chord_list.setCurrentRow(0)
        update_callback(self)

    def add_chord(self):
        logger.debug("add chord")

        chord = chord_prog_api.add_chord()
        self.chord_list.add_item(
            ChordContainer(chord_prog_api.scale, chord),
            chord_prog_api.index.chord
        )

        self.chord_list.set_active_item(chord_prog_api.index.chord)

        _, widget = self.scale_list.get_active_tuple()
        widget.update_display()
        self.scale_list.update_item()

        logger.critical(f"PROG {chord_prog_api._prog} {chord_prog_api.index.scale} {chord_prog_api.index.chord}")

    def update_chord(self):
        logger.debug("update chord")
        chord_prog_api.update_chord()

        item = self.chord_list.currentItem()
        widget = self.chord_list.itemWidget(item)
        widget.update(chord=chord_prog_api.chord)

        self.chord_list.update_item()

        _, widget = self.scale_list.get_active_tuple()
        widget.update_display()
        self.scale_list.update_item()

    def remove_chord(self):
        logger.debug("remove chord")
        if chord_prog_api.remove_chord():
            self.chord_list.remove_item()

            self.chord_list.set_active_item(
                chord_prog_api.index.chord
            )

            _, widget = self.scale_list.get_active_tuple()
            widget.update_display()
            self.scale_list.update_item()

            self.change_chord()

    def change_chord(self):
        row = self.chord_list.currentRow()
        item = self.chord_list.currentItem()
        widget = self.chord_list.itemWidget(item)
        try:
            chord = widget.chord
            logger.debug(f"change chord {chord} {row}")
        except Exception as e:
            print(e)
            print("ROW1", row)
            print("ROW2", item)
            chord = chord_prog_api.chord
            self.change_scale()

            update_callback(self)
            row = self.chord_list.currentRow()
            item = self.chord_list.currentItem()
            widget = self.chord_list.itemWidget(item)
            print("ROW3", row)
            print("ROW4", item)
            print("ROW4", widget)
            print("ROW4", chord_prog_api.index.indexes)
            raise

        state.current_chord = widget.chord

        chord_prog_api.index.chord = row

        update_callback(self)

    def clear_chords(self):
        logger.debug("clear chords")
        chord_prog_api.clear_chords()

        with BlockSignals(self.chord_list):
            self.chord_list.clear()

        self.chord_list.add_item(
            ChordContainer(chord_prog_api.scale, chord_prog_api.chord),
            0
        )


        _, widget = self.scale_list.get_active_tuple()
        widget.update_display()
        self.scale_list.update_item()

    def update_display(self):


        with BlockSignals(self.scale_list):
            if self.scale_list.currentRow() != chord_prog_api.index.scale:
                self.scale_list.set_active_item(
                    chord_prog_api.index.scale
                )
        
        with BlockSignals(self.chord_list):
            self.chord_list.set_active_item(
                chord_prog_api.index.chord
            )
