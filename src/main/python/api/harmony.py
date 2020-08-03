import logging

from collections import namedtuple
from functools import lru_cache

from beethoven.harmony.diatonic import DiatonicHarmony
from beethoven.theory.chords import Chord
from beethoven.theory.scales import Scale
from common.state import state

logger = logging.getLogger(__name__)

chord_tuple = namedtuple("Chord", "root type degree kind first_semitone")


class HarmonyApi(object):
    def __init__(self):
        self.diatonic_chords = {
            "diatonic_triads": "1,3,5",
            "diatonic_sevenths": "1,3,5,7"
        }
        self.chromatic_display_chords = ["maj7", "min7", "7", "min7b5"]
        self.chromatic_chord_types = [
            "7", "dim7", "dim7 dim3", "maj7", "maj7#5",
            "min7", "7b5", "min maj7", "min7b5", "min dim7"
        ]
        self.chromatic_degrees = [
            "I", "bII", "II", "bIII", "III", "IV",
            "bV", "V", "bVI", "VI", "bVII", "VII"
        ]
        self.diatonic_degrees = DiatonicHarmony._DEGREES

        state.preview_chord = ("diatonic_sevenths", 0)

    def __str__(self):
        return "<HarmonyApi>"

    def get_chromatic_scale(self):
        return self._get_chromatic_scale(
            state.current_scale.notes[0].note_name
        )
    
    @lru_cache()
    def _get_chromatic_scale(self, root_note):
        return Scale(name="chromatic scale", root=root_note)

    @lru_cache()
    def get_chord(self, scale, chord_type, index):
        if chord_type in self.diatonic_chords:
            chords = self._get_diatonic_chords(
                scale, chord_type
            )
            chord = chords[index]
            degree = self.diatonic_degrees[index]
            chord.display = f"{degree}"
        else:
            chord = self.get_chromatic_chord(
                scale.root.note_name,
                chord_type,
                index
            )
            degree = self.chromatic_degrees[index]
            chord.display = f"{degree}{chord.name}"

        # chord display string extra formatting
        #chord.display = chord.chord_name
        return chord

    @lru_cache()
    def _get_chord(self, root_note, name):
        return Chord(root=root_note, name=name)

    def get_chromatic_chord(self, scale_root_note, chord_name, index):
        chromatic_scale = self._get_chromatic_scale(scale_root_note)

        return self._get_chord(
            chromatic_scale.notes[index].note_name,
            chord_name
        )

    @lru_cache()
    def _get_diatonic_chords(self, scale, chord_type):
        return scale.get_chords(
            self.diatonic_chords[chord_type]
        )

    def get_diatonic_chord(self, chord_type, index):
        return self._get_diatonic_chords(
            state.current_scale,
            chord_type
        )[index]

    def reset_preview_chord_type(self):
        if not state.current_scale.is_diatonic and state.preview_chord[0] in self.diatonic_chords:
            state.preview_chord = ("maj7", 0)
            logger.debug(f"Set preview chord to {state.preview_chord}")

    def get(self, scale_name, root_note):
        logger.debug(f"Update harmony from {self} : {scale_name} {root_note}")

    def set_chord(self, chord_type, index):
        state.current_chord = (chord_type, index) 
        #self.get_chord(
        #    state.current_scale,
        #    chord_type,
        #    index
        #)


harmony_api = HarmonyApi()
