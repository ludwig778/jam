import logging

from PySide2.QtWidgets import QLabel, QAbstractItemView, QHBoxLayout, QVBoxLayout, QPushButton, QListView, QListWidget, QWidget, QListWidgetItem

from api.chord_progression import chord_prog_api
from api.harmony import harmony_api
from api.scale import scale_api
from common.utils import BlockSignals
from common.state import state

logger = logging.getLogger(__name__)


class ProgressionListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setFlow(QListView.LeftToRight)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def get_active_tuple(self):
        item = self.currentItem()
        widget = self.itemWidget(item)

        return item, widget

    def set_active_item(self, index):
        with BlockSignals(self):
            self.setCurrentRow(index)

    def add_item(self, widget, index=None):
        logger.debug(f"add item {widget}")

        item = QListWidgetItem()
        if index:
            self.insertItem(index, item)
        else:
            self.addItem(item)

        self.setItemWidget(item, widget)
        
        item.setSizeHint(widget.sizeHint())

    def update_item(self):
        logger.debug("update item")

        item = self.currentItem()
        widget = self.itemWidget(item)

        item.setSizeHint(widget.sizeHint())

    def remove_item(self):
        logger.debug("remove item")
        index = self.currentRow()
        
        item = self.item(index)
        item = self.currentItem()

        with BlockSignals(self):
            item = self.takeItem(index)
            del item
