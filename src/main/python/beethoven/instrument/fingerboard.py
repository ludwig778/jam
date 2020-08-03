from beethoven.instrument.tuning import Tuning
from beethoven.theory.notes import Note

FRET_SPACING = 4


class String(object):
    def __init__(self, note):
        self.note = Note(note)

    def get_ascii(self, notes, frets, **kwargs):
        mask = kwargs.get("mask", None)
        base = kwargs.get("base", None)
        ret = list()
        first_fret = frets[0]
        base = base or notes[0]
        fret_format = "{:^" + str(FRET_SPACING) + "s}"
        notes_datas = {note.semitones: (note.note_name, (base / note).interval_name) for note in notes}
        curr_st = self.note.semitones + first_fret
        label_index = 1 if kwargs.get("show_interval") else 0
        for index in range(*frets):
            fret_text = notes_datas.get(curr_st)
            if fret_text and (mask is None or index in mask):
                txt = fret_text[label_index]
                if label_index == 1:
                    txt = txt.replace("M", "")
                data = fret_format.format(txt)
            else:
                data = fret_format.format("")
            ret.append(data)
            curr_st = (curr_st + 1) % 12
        return "|".join(ret)

    def __str__(self):
        return "<String {}>".format(self.note.note_name)

    __repr__ = __str__


class FingerBoard(object):
    def __init__(self, tuning="std_6str", **kwargs):
        self.strings = list()
        self.setup(tuning)
        self.kwargs = kwargs

    def get_ascii(self, notes, frets=[0, 5], masks=None, **kwargs):
        masks = masks or {}
        for index, string in enumerate(self.strings):
            mask = masks.get(len(self.strings) - index - 1)
            mask = mask and range(mask[0], mask[1] + 1) or None
            print(string.get_ascii(notes, frets, **{"mask": mask, **kwargs, **self.kwargs}))

        fret_format = "{:^" + str(FRET_SPACING) + "s}"
        ret = list()
        for fret in range(*frets):
            if (fret % 12) in [0, 3, 5, 7, 9]:
                ret.append(fret_format.format(str(fret)))
            else:
                ret.append(fret_format.format(""))

        print()

    def setup(self, tuning):
        self.tuning = Tuning(tuning=tuning)
        for i in self.tuning.notes:
            self.strings.append(String(i))

    def set_strings(self, tuning):
        self.tuning = Tuning(tuning=tuning)


def main():
    f = FingerBoard(tuning='std_6str',
                    show_interval=True)
    from scale import Scale
    scale = Scale(root='F', name='major')

    mask_array = [
        {0: [1, 5], 1: [1, 5], 2: [2, 5], 3: [2, 5], 4: [3, 6], 5: [3, 6]},
        {i: [5, 8] for i in range(6)},
        {0: [8, 12], 1: [8, 12], 2: [8, 12], 3: [9, 12], 4: [10, 13], 5: [10, 13]},
        {i: [12, 15] for i in range(6)}
    ]
    for i, chord in enumerate(scale.get_chords("1,3,5")):
        for mask in mask_array:
            True or f.get_ascii(
                chord.notes,
                masks=mask,
                base=scale.root,
                frets=[1, 16]
            )
        f.get_ascii(
            chord.notes,
            base=scale.root,
            frets=[1, 16]
        )
        input()
        print()


if __name__ == "__main__":
    main()
