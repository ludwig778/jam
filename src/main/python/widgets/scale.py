import logging

from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QComboBox, QHBoxLayout, QPushButton, QWidget

from api.scale import scale_api
from common.utils import BlockSignals
from common.callbacks import update_callback

logger = logging.getLogger(__name__)


class ScaleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

        update_callback.register(self)

    def __str__(self):
        return "<ScaleWidget>"

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.scale_combo = QComboBox()
        self.root_combo = QComboBox()
        self.btn_previous = QPushButton("previous")
        self.btn_next = QPushButton("next")
        self.btn_previous_fifth = QPushButton("previous fifth")
        self.btn_next_fifth = QPushButton("next fifth")

    def modify_widgets(self):
        scale_model = QStandardItemModel()
        for name, label in scale_api.display_scales:
            if name == "label":
                item = QStandardItem(f"-- {label} --")
                item.setEnabled(name != "label")
            else:
                item = QStandardItem(name)

            scale_model.appendRow(item)

        self.scale_combo.setModel(scale_model)

        self.root_combo.addItems(scale_api.notes)

    def create_layouts(self):
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.scale_combo)
        self.main_layout.addWidget(self.root_combo)
        self.main_layout.addWidget(self.btn_previous)
        self.main_layout.addWidget(self.btn_next)
        self.main_layout.addWidget(self.btn_previous_fifth)
        self.main_layout.addWidget(self.btn_next_fifth)

    def setup_connections(self):
        self.scale_combo.currentIndexChanged.connect(self.update_scale_name)
        self.root_combo.currentIndexChanged.connect(self.update_root)
        self.btn_next.clicked.connect(self.set_next_root)
        self.btn_previous.clicked.connect(self.set_previous_root)
        self.btn_next_fifth.clicked.connect(self.set_next_root_by_fifth)
        self.btn_previous_fifth.clicked.connect(self.set_previous_root_by_fifth)

    def set_scale(self, *args):
        scale_api.set_scale(
            self.scale_combo.currentText(),
            self.root_combo.currentText()
        )

    def update_display(self):
        logger.debug("Update scale")

        scale_name, root_note = scale_api.get_scale_attributes()
        logger.debug(f"Update scale name display {[scale_name, root_note]}")

        if scale_name != self.root_combo.currentText():
            logger.debug(f"Update scale name display")

            with BlockSignals(self.root_combo):
                self.root_combo.setCurrentText(root_note)

        if root_note != self.scale_combo.currentText():
            logger.debug(f"Update root note display")

            with BlockSignals(self.scale_combo):
                self.scale_combo.setCurrentText(scale_name)

    def update_scale_name(self, *args):
        logger.debug("Update scale name")
        self.set_scale()
        update_callback(self)

    def update_root(self, *args):
        logger.debug("Update root")
        self.set_scale()
        update_callback(self)

    def set_next_root(self):
        logger.debug("Set next root")
        current_index = self.root_combo.currentIndex()
        index = scale_api.get_sharpened_index(current_index)
        self.root_combo.setCurrentIndex(index)

    def set_previous_root(self):
        logger.debug("Set previous root")
        current_index = self.root_combo.currentIndex()
        index = scale_api.get_flattened_index(current_index)
        self.root_combo.setCurrentIndex(index)

    def set_next_root_by_fifth(self):
        logger.debug("Set next root by a fifth")
        current_index = self.root_combo.currentIndex()
        for _ in range(7):
            index = scale_api.get_sharpened_index(current_index)
            current_index = index
        self.root_combo.setCurrentIndex(index)

    def set_previous_root_by_fifth(self):
        logger.debug("Set previous root by a fifth")
        current_index = self.root_combo.currentIndex()
        for _ in range(7):
            index = scale_api.get_flattened_index(current_index)
            current_index = index
        self.root_combo.setCurrentIndex(index)
