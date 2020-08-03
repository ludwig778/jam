import asyncio
import logging

from collections import defaultdict
from functools import partial
from time import sleep

from mido import open_output, get_output_names, open_output, Message

from constants.app import MIDI_OUTPUT_NAME

logger = logging.getLogger(__name__)


class MIDIApi(object):
    def __init__(self):
        self.output = open_output(MIDI_OUTPUT_NAME, virtual=True)

    @classmethod
    def send(cls, output, channel, message_type, notes, **kwargs):
        for note in notes:
            output.send(Message(message_type, note=note, channel=channel, **kwargs))

    @classmethod
    def get_channel(cls, name):
        if name in get_output_names():
            return open_output(name)

    @property
    def channels(self):
        return get_output_names()

    def play(self, *notes, output=None, channel=0, time=0, velocity=127):
        self.send(output or self.output, channel, 'note_on', notes, time=time, velocity=velocity)

    def stop(self, *notes, output=None, channel=0):
        self.send(output or self.output, channel, 'note_off', notes, time=0, velocity=0)

    def clean(self, **kwargs):
        self.stop(*range(0,128), **kwargs)

    def play2(self, *notes, output=None, channel=0, time=0, velocity=127):
        logger.critical(f"Playing notes: {notes} for {time}s with velocity {velocity}")

        self.play(*notes, output=output, channel=channel, time=time, velocity=velocity)

        try:
            sleep(time)
        except:
            pass
        finally:
            self.stop(*notes, output=output, channel=channel)


midi_api = MIDIApi()
ma = midi_api