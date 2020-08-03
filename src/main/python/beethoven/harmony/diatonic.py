from random import shuffle

from beethoven.harmony.base import Harmony
from beethoven.theory.notes import Note
from beethoven.theory.scales import Scale

#
# https://en.wikipedia.org/wiki/Mode_(music)
#


class DiatonicHarmony(Harmony):
    def __init__(self, tone="C", scale="major"):
        self.setup(tone, scale=scale)
        self.current_degree = "1"

    def diatonic_substitution(self):
        for function, degrees in self._FUNCTIONS.items():
            if self.current_degree in degrees:
                degrees = degrees[:]
                degrees.remove(self.current_degree)
                shuffle(degrees)
                self.current_degree = degrees[0]

    @classmethod
    def _get_degrees(cls, scale):
        degrees = list()
        degrees_data = list(cls._DEGREES.items())
        c_degrees_data = list([i.semitones for i in cls._C_SCALE.intervals])

        triads = scale.get_chords("1,3,5")
        seventh = scale.get_chords("1,3,5,7")
        for index, interval in enumerate(scale.intervals):
            diff_st = interval.semitones - c_degrees_data[index][1]

            alteration = ""
            if diff_st > 0:
                alteration = diff_st * "#"
            elif diff_st < 0:
                alteration = abs(diff_st) * "b"

            roman_num = degrees_data[index][0]

            degrees.append({
                "degree": alteration + roman_num,
                "triad": triads[index],
                "seventh": seventh[index]
            })
        return degrees

    @classmethod
    def _get_all_degrees(cls, scale):
        degrees = dict()
        # degrees_data = list([i.semitones for i in scale.intervals])
        intervals = scale.intervals
        # c_degrees_data = list([i.semitones for i in cls._C_SCALE.intervals])
        degg = {0: "I", 2: "II", 4: "III", 5: "IV", 7: "V", 9: "VI", 11: "VII"}

        def get_alteration(alteration):
            if alteration > 0:
                return alteration * "#"
            elif alteration < 0:
                return abs(alteration) * "b"
            else:
                return ""

        def get_alt(index, alt):
            if alt == -2:
                return ({index - 2: get_alteration(0) + degg.get(index)},
                        {index - 1: get_alteration(1) + degg.get(index),
                         index: get_alteration(2) + degg.get(index)})
            if alt == -1:
                return ({index - 1: get_alteration(0) + degg.get(index)},
                        {index: get_alteration(1) + degg.get(index)})
            if alt == 0:
                return ({index: get_alteration(0) + degg.get(index)},
                        {index - 1: get_alteration(-1) + degg.get(index)})
            if alt == 1:
                return ({index + 1: get_alteration(0) + degg.get(index)},
                        {index: get_alteration(-1) + degg.get(index),
                         index - 1: get_alteration(-2) + degg.get(index)})

        final_degrees = dict()
        stuff_list = [(1, 2), (2, 4), (3, 5), (4, 7), (5, 9), (6, 11)]
        stuff_list.reverse()
        for index, semitones in stuff_list:
            interval = intervals[index]
            i_alt = interval.alteration
            def_degrees, new_degrees = get_alt(semitones, i_alt)
            degrees.update(new_degrees)
            final_degrees.update(def_degrees)

        degrees.update({0: "I"})
        degrees.update(final_degrees)
        txt = list()
        for st, degree in sorted(degrees.items()):
            txt.append(degree)
        return txt

    def modulation(self, tone, scale=None):
        self.scale = Scale(root=tone, name=scale or self.scale.name)
        self.tone = tone if isinstance(tone, Note) else tone
        self.degrees = self._get_degrees(self.scale)

    setup = modulation
