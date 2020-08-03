from beethoven.theory.directory import ChordDirectory
from beethoven.theory.notes import Interval, Note, Notes


class ChordNameNotFound(Exception):
    pass


class Chord(ChordDirectory):
    _CHORD_NAME_INDEX = 0

    def __init__(self, root=None, name=None, intervals=None):
        self.root = root if isinstance(root, Note) else Note(root)

        if name:
            intervals = self._DIR.get(name)
        elif intervals:
            name = self._REVERSE_DIR.get(frozenset(intervals))
            if name:
                name = name[0]
            else:
                name = None

        self.name = name
        self.intervals = [Interval(i) for i in intervals]

        self.notes = [self.root + interval for interval in self.intervals]
        Notes.__init__(self, self.notes)

    @classmethod
    def _get_chord_from_notes(cls, notes):
        notes = list(map(
            lambda n: n if isinstance(n, Note) else Note(n),
            notes
        ))

        root = notes.pop(0)
        intervals = ["1"]

        for note in notes:
            intervals.append(
                Note._lookup_interval_from_notes(root, note).interval_name
            )

        return cls(root=root, intervals=intervals)

    @property
    def name_found(self):
        return self.name is not None

    @property
    def chord_name(self):
        return "{}{}{}".format(
            self.root.note_name,
            " " if self._CHORD_NAME_INDEX == 1 else "",
            self.name or self.notes
        )

    def __str__(self):
        return "<Chord {}>".format(self.chord_name)

    __repr__ = __str__
