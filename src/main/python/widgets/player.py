import asyncio
import logging
from time import sleep

from PySide2.QtCore import QThread
from api.midi import midi_api

from common.state import state

logger = logging.getLogger(__name__)

from api.chord_progression import chord_prog_api, harmony_api
from api.instruments import instruments_api
from common.callbacks import update_callback
from constants.app import BASE_BPM


def get_notes(scale, chord, first_midi=56):
    base_st = first_midi

    logger.critical(state.preview_chord)
    chord = harmony_api.get_chord(scale, *chord)
    logger.critical(chord)
    logger.critical(chord.notes)

    notes = []
    last_note = None

    for note in chord.notes:
        note_st = note.semitones + base_st
        if not last_note:
            last_note = note_st
        elif note_st < last_note:
            note_st += 12
        notes.append(note_st)

    logger.critical(base_st)
    logger.critical(notes)

    return notes
        

class PlayerThread(QThread):
    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        while 1:
            #logger.critical(chord_prog_api.scale)
            #logger.critical(chord_prog_api.chord)
            #logger.critical(60 / state.bpm)
            logger.critical(state.preview_chord)
            notes = get_notes(chord_prog_api.scale, chord_prog_api.chord)
            
            generators = {}
            for channel, inst in instruments_api.active_instruments:
                logger.critical(f"PLAY INSTRUMENT {inst} {channel}")
                partition = inst.generate_partition(notes)
                inst.channel = channel
                generators[channel] = partition
                #inst.play("STUFFS")

            for i in range(16):

                played = {}
                for channel, gen in generators.items():
                    to_play = next(gen)
                    if to_play:
                        played[channel] = to_play

                for channel, notes in played.items():
                    logger.critical(f"PLAY INSTRUMENT {channel} {notes}")
                    midi_api.play(*notes, channel=channel)

                logger.critical((60 / state.bpm) / 4)
                sleep((60 / state.bpm) / 4)

                for channel, notes in played.items():
                    logger.critical(f"STOP INSTRUMENT {channel} {notes}")
                    midi_api.stop(*notes, channel=channel)

            chord_prog_api.next()
            update_callback(self)


class PreviewPlayerThread(QThread):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()

    def play_note(self):
        self.loop.run_in_executor(None, self._play_notes)

    def _play_notes(self):
        logger.critical("PLAY NOTE")
        logger.critical(state.preview_chord)
        notes = get_notes(state.current_scale, state.preview_chord)
        
        for channel, inst in instruments_api.preview_instruments:
            logger.critical(f"PLAY INSTRUMENT {inst} {channel}")
            midi_api.play(*notes, channel=channel)

        logger.critical(60 / state.bpm)
        sleep(60 / state.bpm)

        for channel, inst in instruments_api.preview_instruments:
            logger.critical(f"PLAY INSTRUMENT {inst} {channel}")
            midi_api.stop(*notes, channel=channel)

        logger.critical(chord.notes)

        logger.critical("STOP PLAY NOTE")


player = PlayerThread()
preview_player = PreviewPlayerThread()
