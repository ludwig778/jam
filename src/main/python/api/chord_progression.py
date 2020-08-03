import logging
from collections import namedtuple
from dataclasses import dataclass

from api.scale import scale_api
from api.harmony import harmony_api
from common.state import state
from copy import copy

logger = logging.getLogger(__name__)

@dataclass
class Index:
    scale: int = 0
    chord: int = 0

    @property
    def indexes(self):
        return self.scale, self.chord

    def set_indexes(self, scale, chord):
        self.scale = scale
        self.chord = chord

    def reset(self):
        self.scale = 0
        self.chord = 0


progression = [
    ("major", "C", [
        ("diatonic_sevenths", 0),
        #("diatonic_sevenths", 5),
        #("diatonic_sevenths", 4),
    ]),
    #("natural minor", "A#", [
    #    ("diatonic_sevenths", 2),
    #    ("diatonic_sevenths", 5)
    #]),
    #("major", "C", [
    #    ("diatonic_sevenths", 2)
    #])
]

class ChordProgressionApi(object):
    def __init__(self):
        self._prog = []
        self.index = Index()
        self.extract_progression()

    def extract_progression(self):
        for scale_name, root_note, chords in progression:
            scale = scale_api.get_scale(scale_name, root_note)
            scale_container = self._add_scale(scale, chords)
            self._prog.append(scale_container)

    def log_stuff(self, annotation):
        logger.debug(f"========= {annotation} =========")
        logger.debug(chord_prog_api.indexes)
        logger.debug(self._prog)
        chords = [
			harmony_api.get_chord(self._prog[self.index.scale], *chord)
			for chord in self._prog[self.index.scale].chords
		]
        logger.debug(chords)
        logger.debug([
            harmony_api.get_chord(self._prog[self.index.scale], *chord).display
            for chord in self._prog[self.index.scale].chords])
        logger.debug(f" --------     END      --------")

    def add_scale(self):
        self.log_stuff("BEFORE add_scale")
        self.index.scale += 1
        self.index.chord = 0

        scale = self._add_scale(
            state.current_scale,
            [("diatonic_sevenths", 0)]
        )

        self._prog.insert(self.index.scale + 0, scale)

        self.log_stuff("AFTER add_scale")

        return scale

    def _add_scale(self, scale, chords, append=False):
        scale = copy(scale)
        scale.chords = []

        for chord in chords:
            scale.chords.append(
                self._add_chord(scale, chord)
            )

        return scale

    def add_chord(self):
        self.log_stuff("BEFORE add_chord")
        self.index.chord += 1

        chord_container = self._add_chord(
            state.current_scale,
            state.preview_chord
        )

        self._prog[self.index.scale].chords.insert(self.index.chord, chord_container)

        self.log_stuff("AFTER add_chord")

        return chord_container

    def _add_chord(self, scale, chord):
        return chord

    def update_chord(self):
        self.log_stuff("BEFORE update_chord")
        self._prog[self.index.scale].chords[self.index.chord] = state.preview_chord
        self.log_stuff("AFTER update_chord")
    
    def remove_chord(self):
        self.log_stuff("BEFORE remove_chord")
        is_removed = False
        index = self.index.chord

        next_index = None
        if index < len(self.chords) - 1:
            next_index = index
        elif index:
            next_index = index - 1

        if next_index is not None:
            #del self._prog[self.index.scale].chords[]
            del self.chords[self.index.chord]
            self.index.chord = next_index

            is_removed = True

        self.log_stuff("AFTER remove_chord")

        return is_removed

    def update_scale(self):
        self.log_stuff("BEFORE update_scale")
        old_scale = self._prog[self.index.scale]

        scale = state.current_scale

        if not scale.is_diatonic:
            chords = []
            for chord in self.scale.chords:
                chord_type, chord_index = chord
                if chord_type in harmony_api.diatonic_chords:
        
        
                    ch_scale = harmony_api._get_chromatic_scale(old_scale.root.note_name)

                    ch_note_index = ch_scale.notes.index(old_scale.notes[chord_index])
                    ch_chord_type = harmony_api.get_chord(old_scale, chord_type, chord_index).name

                    chord = (ch_chord_type, ch_note_index)

                chords.append(chord)
            scale.chords = chords
        else:
            scale.chords = self.scale.chords
        
        self._prog[self.index.scale] = scale

        self.log_stuff("AFTER update_scale")
    
    def remove_scale(self):
        self.log_stuff("BEFORE remove_scale")
        is_removed = False
        index = self.index.scale

        next_index = None
        if index < len(self._prog) - 1:
            next_index = index
        elif index:
            next_index = index - 1

        if next_index is not None:
            del self._prog[self.index.scale]
            self.index.scale = next_index

            is_removed = True

        self.log_stuff("AFTER remove_scale")

        return is_removed

    def clear_chords(self):
        self.log_stuff("BEFORE clear_chords")
        current_chord = self.chord

        self._prog[self.index.scale].chords = [current_chord]

        self.index.chord = 0

        self.log_stuff("AFTER clear_chords")

    def reset(self):
        self.index.reset()

    @property
    def indexes(self):
        return self.index.indexes

    @property
    def scales(self):
        return self._prog

    @property
    def scale(self):
        return self._prog[self.index.scale]

    @property
    def chords(self):
        return self.scale.chords

    @property
    def chord(self):
        return self.chords[self.index.chord]

    def next(self):
        #self.log_stuff("BEFORE next")
        indexes = self._get_next(*self.index.indexes)

        self.index.set_indexes(*indexes)
        indexes = self._get_next(*indexes)
        #self.log_stuff("AFTER next")
        #self.log_stuff("next")

    def _get_next(self, scale_index, chord_index):
        chords = self.scale.chords

        if chord_index + 1 >= len(chords):
            chord_index = 0
            scale_index = (scale_index + 1) % len(self._prog)
        else:
            chord_index += 1

        return scale_index, chord_index

    @staticmethod
    def _switch_item(item_list, start, end):
        item = item_list.pop(start)
        item_list.insert(end, item)

    @property
    def prog(self):
        return [
            harmony_api.get_chord(self._prog[self.index.scale], *chord).display
            for chord in self._prog[self.index.scale].chords
        ]

    def switch_scale(self, start, end):
        self.log_stuff("BEFORE switch_scale")
        self._switch_item(self._prog, start, end)
        self.index.scale = end
        self.log_stuff("AFTER switch_scale")

    def switch_chord(self, start, end):
        self.log_stuff("AFTER switch_chord")
        self._switch_item(self.chords, start, end)
        self.index.chord = end
        self.log_stuff("AFTER switch_chord")


chord_prog_api = ChordProgressionApi()
