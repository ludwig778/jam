class BlockSignals(object):
    def __init__(self, widget):
        self.widget = widget

    def __enter__(self):
        self.widget.blockSignals(True)

    def __exit__(self, type, value, traceback):
        self.widget.blockSignals(False)
