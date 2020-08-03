from collections import namedtuple

from beethoven.theory.notes import Interval
from beethoven.theory.scales import Scale


class CircleOfFifth(object):
    _DEGREE = namedtuple('Degree', ['note', 'scale', 'accidentals'])
    _DEGREES = {-1: 'Ab',
                0: 'C',
                1: 'Db',
                2: 'D',
                3: 'Eb',
                4: 'E',
                5: 'F',
                6: 'Gb',
                7: 'G',
                8: 'Ab',
                9: 'A',
                10: 'Bb',
                11: 'B',
                12: 'F#',
                13: 'C#'}

    def __init__(self, step="5"):
        self.step = self._get_step(step)

        self.degrees = dict()
        for index, degree_note in self._DEGREES.items():
            scale = Scale(root=degree_note, name="major")
            self.degrees.update({index: self._DEGREE(scale.root, scale, scale.accidentals)})

        self.counter = self.step.reverse().semitones

    @classmethod
    def _get_step(cls, step):
        return Interval(step)

    def next(self):
        self.counter = (self.counter + self.step.semitones) % 12
        return self.degrees.get(self.counter)
