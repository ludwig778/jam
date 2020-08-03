from beethoven.theory.chords import Chord
from beethoven.theory.directory import ScaleDirectory
from beethoven.theory.notes import Interval, Note, Notes


class CouldntFindScaleByName(Exception):
    pass


class Scale(Notes, ScaleDirectory):
    # _REVERSE_DIRECTORY = OrderedDict(
    #     {
    #         tuple(Interval(interval).interval_name for interval in v.split(',')): k
    #         for k, v in _DIRECTORY.items()
    #     }
    # )

    def __init__(self, root=None, degrees="", name=None, notes=None):
        if root and (name or degrees):
            self.root = Note(root)
            if name:
                degrees = self._DIR.get(name)
                self.name = name

            if not (isinstance(degrees, list) or isinstance(degrees, frozenset)):
                degrees = degrees.split(",")

            self.intervals = [Interval(degree) for degree in degrees]
            self.degrees = [interval.interval_name for interval in self.intervals]
            self.notes = [interval.get_note(self.root) for interval in self.intervals]
        elif notes:
            self.root = notes[0]
            self.notes = notes
            self.intervals = self._get_intervals(self.root, self.notes)
            self.degrees = [interval.interval_name for interval in self.intervals]
            scale_name = self._resolve_scale_name(self.intervals)
            if scale_name:
                self.name = scale_name
        self.accidentals = self._get_accidentals(self.notes)

    @property
    def scale_name(self):
        return "{} {}".format(self.root.note_name, getattr(self, 'name', None) or self.degrees)

    def __str__(self):
        return "<Scale {}>".format(self.scale_name)

    __repr__ = __str__

    def change_root(self, root):
        if self.name:
            return Scale(root=root, name=self.name)
        else:
            return Scale(root=root, degrees=self.degrees)

    @classmethod
    def _resolve_scale_name(cls, intervals):
        intervals_tuple = tuple([interval.interval_name for interval in intervals])
        return cls._REVERSE_DIR.get(intervals_tuple, None)

    def get_mode(self, degree):
        degree %= len(self.notes)
        notes = self.notes[degree:] + self.notes[:degree]
        return Scale(notes=notes)

    def get_modes(self):
        return list(map(self.get_mode, list(range(len(self.notes)))))

    def get_chords(self, degrees="1,3,5,7"):
        if isinstance(degrees, str):
            degrees = list(map(int, degrees.split(',')))

        notes = self.notes
        scale_len = len(notes)

        chords = list()
        for index in range(scale_len):
            chords.append(Chord._get_chord_from_notes([notes[(index + degree - 1) % scale_len] for degree in degrees]))
        return chords

    def __sub__(self, diff_scale):
        self_keys = [note.semitones for note in self.notes]
        return [note for semitone, note in diff_scale.notes.items() if semitone not in self_keys]

    def __truediv__(self, diff_scale):
        self_notes = [note.note_name for note in self.notes]
        return [note for semitone, note in diff_scale.notes.items() if note.note_name not in self_notes]
