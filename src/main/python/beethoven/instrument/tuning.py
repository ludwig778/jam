from beethoven.theory.notes import Note


class TuningDirectory(object):
    directory = {"std_6str": "E,B,G,D,A,E",
                 "std_7str": "E,B,G,D,A,E,B",
                 "std_4str": "G,D,A,E"}


class Tuning(TuningDirectory):
    def __init__(self, notes="", tuning=None):
        self.strings = []
        self.notes = notes

        if tuning:
            self.notes = self.directory.get(tuning)

        if self.notes:
            if isinstance(notes, str):
                self.notes = self.notes.split(",")

            for i, note_name in enumerate(self.notes):
                note = Note(note_name)
                index = Note._lookup_note_index(note)
                self.strings.append((i + 1, note, index))

    def __str__(self):
        return "<Tuning {}>".format(",".join(self.notes))

    __repr__ = __str__
