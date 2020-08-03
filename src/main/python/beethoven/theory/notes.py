import re

from collections import namedtuple
from itertools import product


class NotAValidNote(Exception):
    pass


class NotAValidInterval(Exception):
    pass


class CouldntFindAlteration(Exception):
    pass


class NoteIntervalResolution(object):
    _NOTES = {"A": 1,
              "B": 3,
              "C": 4,
              "D": 6,
              "E": 8,
              "F": 9,
              "G": 11}
    _INTERVALS = {1: 0,
                  2: 2,
                  3: 4,
                  4: 5,
                  5: 7,
                  6: 9,
                  7: 11}
    _INTERVAL_META = {"perfect": [4, 5],
                      "unperfect": [2, 3, 6, 7]}
    _PERFECT_INTERVAL = [1, 4, 5]
    _UNPERFECT_INTERVAL = [2, 3, 6, 7]

    _ALL_NOTES = list(
        map(
            lambda x: "".join(x),
            product(
                _NOTES.keys(),
                ["b", "", "#"]
            )
        )
    )

    @classmethod
    def _resolve_note_alteration(self, alteration):
        if alteration:
            if alteration > 0:
                return alteration * "#"
            if alteration < 0:
                return abs(alteration) * "b"
        return ""

    @classmethod
    def _lookup_note_index(cls, note):
        return (cls._NOTES.get(note.note) + note.alteration) % 12

    @classmethod
    def _lookup_note_alteration(cls, alteration):
        if not alteration:
            return 0
        elif "#" in alteration:
            return alteration.count("#")
        elif "b" in alteration:
            return - alteration.count("b")
        else:
            raise CouldntFindAlteration(alteration)

    @classmethod
    def _resolve_interval_alteration(cls, alteration, degree):
        if degree in cls._PERFECT_INTERVAL:
            if not alteration:
                return ""
            else:
                return abs(alteration) * ("a" if alteration > 0 else "d")
        elif degree in cls._UNPERFECT_INTERVAL:
            if not alteration:
                return "M"
            elif alteration == -1:
                return "m"
            elif alteration > 0:
                return alteration * "a"
            elif alteration < -1:
                return abs(alteration + 1) * "d"
        else:
            raise CouldntFindAlteration((degree, alteration))

    @classmethod
    def _lookup_interval_alteration(cls, alteration, degree):
        if not alteration:
            return 0
        if "a" in alteration:
            return alteration.count("a")
        if degree in cls._UNPERFECT_INTERVAL:
            if "M" in alteration:
                return 0
            if "m" in alteration:
                return -1
            if "d" in alteration:
                return - alteration.count("d") - 1
        elif degree in cls._PERFECT_INTERVAL:
            if "d" in alteration:
                return - alteration.count("d")
        else:
            raise CouldntFindAlteration(alteration)

    @classmethod
    def _lookup_note_from_interval(cls, note, interval):
        d = interval.degree - 1
        st = interval.semitones

        base_note = note.note
        # semitones = note.unaltered_semitones
        for i, data in enumerate(list(cls._NOTES.items()) * 2):
            if data[0] == base_note:
                index_base_note = i
                break

        d = d + index_base_note
        base_st = (list(cls._NOTES.values()) * 2)[index_base_note]
        dest_note, dest_st = (list(cls._NOTES.items()) * 2)[d]

        final_alteration = (base_st + st) - dest_st + note.alteration

        final_alteration = ((base_st - dest_st + note.alteration) % 12) + st
        if final_alteration >= 12:
            final_alteration = final_alteration % 12
        elif final_alteration >= 6 or (note.alteration < 0 and final_alteration > 0):
            final_alteration -= 12

        if final_alteration > 0:
            final_note = dest_note + ("#" * final_alteration)
        elif final_alteration < 0:
            final_note = dest_note + ("b" * abs(final_alteration))
        else:
            final_note = dest_note

        return Note(final_note)

    @classmethod
    def _lookup_interval_index(cls, semitones):
        intervals = list(cls._INTERVALS.values())
        keys = list(cls._INTERVALS.keys())
        return keys[intervals.index(semitones)]

    @classmethod
    def _lookup_interval_from_notes(cls, n1, n2):
        c = Note("C")

        l1 = (n1.unaltered_semitones - c.unaltered_semitones) % 12
        l2 = (n2.unaltered_semitones - c.unaltered_semitones) % 12

        d1 = cls._lookup_interval_index(l1)
        d2 = cls._lookup_interval_index(l2)

        degree = ((7 - (d1 - d2)) % 7) + 1
        interval = cls._INTERVALS.get(degree)
        # alt_diff = n2.alteration - n1.alteration
        alt_count = ((l2 - l1) + (n2.alteration - n1.alteration)) % 12

        alt_count -= interval
        if alt_count >= 6:
            alt_count -= 12
        if alt_count <= -6:
            alt_count %= 12

        alteration = cls._resolve_interval_alteration(alt_count, degree)

        return Interval("{}{}".format(degree, alteration))


class Interval(NoteIntervalResolution):

    _INTERVAL_REGEX = re.compile(r"(?P<degree>\d+)(?P<alteration>(M+|m+|a+|d+|.?))")

    def __init__(self, interval, extended=False):
        matches = self._INTERVAL_REGEX.match(interval)
        degree = matches.group("degree")
        alteration = matches.group("alteration")
        if degree:
            self.degree = int(degree)
            if not extended:
                self.degree = self.non_extended_degree
            if self.non_extended_degree in self._UNPERFECT_INTERVAL and not alteration:
                alteration = "M"
            self.alteration = self._lookup_interval_alteration(alteration, self.non_extended_degree)
            self.semitones = self._INTERVALS.get(self.non_extended_degree) + self.alteration
            self.ascii_alt = self._resolve_interval_alteration(self.alteration, self.non_extended_degree)
        else:
            raise NotAValidInterval()

    def __eq__(self, other):
        return (
            self.degree == other.degree and
            self.alteration == other.alteration and
            self.semitones == other.semitones
        )

    @property
    def interval_name(self):
        return "{}{}".format(self.degree, self.ascii_alt)

    @classmethod
    def _reverse(cls, interval):
        degree = interval.non_extended_degree
        if degree == 1:
            return Interval("1")
        alt = interval.ascii_alt
        if "m" in alt:
            alt = alt.replace("m", "M")
        else:
            alt = alt.replace("M", "m")
        if "d" in alt:
            alt = alt.replace("d", "a")
        else:
            alt = alt.replace("a", "d")
        degree = 9 - degree
        return Interval("{}{}".format(degree, alt))

    def reverse(self):
        return self._reverse(self)

    @property
    def non_extended_degree(self):
        return ((self.degree - 1) % 7) + 1

    def get_note(self, note):
        return self._lookup_note_from_interval(note, self)

    def __str__(self):
        return "<Interval {}>".format(self.interval_name)

    __repr__ = __str__

    @classmethod
    def _lookup_interval(cls, interval):
        str_degre = re.search(r'\d+', interval).group()
        degre = int(str_degre)
        semitones = 0
        if degre > 7:
            degre = (degre % 8) + 1
            # semitones = 12
            interval = interval.replace(str_degre, str(degre))

        d = cls.intervals[interval]["d"]
        st = cls.intervals[interval]["st"] + semitones
        return d, semitones + st


class Note(NoteIntervalResolution):
    _NOTE_REGEX = re.compile(r"(?P<note>.)(?P<alteration>(#+|b+|.?))")

    def __init__(self, note):
        matches = self._NOTE_REGEX.match(note)
        note = matches.group("note")
        alteration = matches.group("alteration")
        if note:
            self.note = note
            self.alteration = self._lookup_note_alteration(alteration)
            self.unaltered_semitones = self._NOTES.get(note)
            self.semitones = (self._NOTES.get(note) + self.alteration) % 12
            self.ascii_alt = alteration
        else:
            raise NotAValidNote(note)

    def __add__(self, obj):
        if isinstance(obj, Interval):
            return self._lookup_note_from_interval(self, obj)

    def __truediv__(self, obj):
        if isinstance(obj, Note):
            return self._lookup_interval_from_notes(self, obj)

    def __eq__(self, note):
        return (self.note == note.note and
                self.semitones == note.semitones and
                self.alteration == note.alteration and
                self.ascii_alt == note.ascii_alt)

    @property
    def note_name(self):
        return "{}{}".format((self.note or "None"), self.ascii_alt)

    def __str__(self):
        return "<Note {}>".format(self.note_name)

    __repr__ = __str__

    # def __repr__(self):
    #     return (self.note, self.alteration)


class Notes(object):
    _ACCIDENTALS = namedtuple('Accidentals', ['flats', 'sharps', 'notes'])
    _SHARPS = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    _FLATS = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab"]

    def __init__(self, notes):
        self.notes = notes

    @classmethod
    def _get_all_notes(cls, start):
        # if start in cls._SHARPS:
        #     index = cls._SHARPS.index(start)
        #     return cls._SHARPS[index:12] + cls._SHARPS[0:index]
        # elif start in cls._FLATS:
        #     index = cls._FLATS.index(start)
        #     return cls._SHARPS[index:12] + cls._SHARPS[0:index]
        # return cls._SHARPS
        pass

    @classmethod
    def _get_intervals(cls, fundamental, notes):
        return [fundamental / note for note in notes]

    @classmethod
    def _get_accidentals(self, notes):
        flats, sharps, altered_notes = 0, 0, list()
        for note in notes:
            if note.alteration < 0:
                flats += 1
            elif note.alteration > 0:
                sharps += 1
            else:
                continue
            altered_notes.append(note)
        return self._ACCIDENTALS(flats, sharps, altered_notes)
