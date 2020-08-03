from fbs_runtime.application_context.PySide2 import (ApplicationContext,
                                                     cached_property)
from PySide2.QtGui import QPixmap


class Context(ApplicationContext):
    @cached_property
    def maple_fretboard(self):
        return QPixmap(self.get_resource('fretboard/maple.png'))

    @cached_property
    def stylesheet(self):
        return self.get_resource('style.css')


app_context = Context()
