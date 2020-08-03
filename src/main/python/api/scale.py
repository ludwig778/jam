import logging

from functools import lru_cache

from beethoven.theory.notes import NoteIntervalResolution
from beethoven.theory.scales import Scale
from common.state import state

logger = logging.getLogger(__name__)

SHARPENED_SKIP_INDEXES = list(range(0, 21, 3)) + [5, 14]
FLATTENED_SKIP_INDEXES = list(range(2, 21, 3)) + [6, 15]


class ScaleApi(object):
    def __init__(self):
        self.scale_by_name = Scale._DIR
        self.notes = NoteIntervalResolution._ALL_NOTES

    def set_scale(self, name, root_note):
        root_note = root_note.capitalize()
        logger.critical("root_note")
        logger.critical(root_note)
        state.current_scale = self.get_scale(name, root_note)

    @lru_cache()
    def get_scale(self, name, root_note):
        scale = Scale(name=name, root=root_note)
        scale.is_diatonic = len(scale.notes) == 7
        logger.critical("get_scale")
        logger.critical(scale)
        return scale

    def get_scale_attributes(self):
        return (
            state.current_scale.name,
            state.current_scale.root.note_name
        )

    @property
    def display_scales(self):
        return Scale._DISPLAY

    def get_sharpened_index(self, index):
        for semitone in range(1, 4):
            new_index = (index + semitone) % 21
            if new_index not in SHARPENED_SKIP_INDEXES:
                break

        return new_index

    def get_flattened_index(self, index):
        for semitone in range(1, 4):
            new_index = (index - semitone) % 21
            if new_index not in FLATTENED_SKIP_INDEXES:
                break

        return new_index


scale_api = ScaleApi()
