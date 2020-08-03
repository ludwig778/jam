import logging

logger = logging.getLogger(__name__)

class Player(object):
    @classmethod
    def generate_partition(cls, notes):
        while True:
            yield []

class TestPlayer(Player):
    @classmethod
    def generate_partition(cls, notes):
        i = 0
        while True:
            yield [notes[i % len(notes)]]
            i += 1

class TestPlayer2(Player):
    @classmethod
    def generate_partition(cls, notes):
        i = 0
        while True:
            to_play = []
            if not i % 8:
                to_play.append(notes[0])
            yield to_play
            i += 1

class PianoPlayer(Player):
    @classmethod
    def generate_partition(cls, notes):
        i = 0
        while True:
            to_play = []
            if not i % 4:
                to_play = notes
            yield to_play
            i += 1

class DrumPlayer(Player):
    @classmethod
    def generate_partition(cls, notes):
        i = 0
        while True:
            to_play = []
            if not i % 8:
                to_play.append(36)
            if not (i + 4) % 8:
                to_play.append(39)
            #if not i % 2:
            to_play.append(49)
            yield to_play
            i += 1

class NonePlayer(Player):
    pass

class Instrument(object):
    pass

class NoneInstrument(Instrument):
    PLAYERS = {
        #"": NonePlayer
        "": Player
    }

class GuitarInstrument(Instrument):
    PLAYERS = {
        "Test": TestPlayer,
        "Triads": TestPlayer2,
        "Sevenths": Player
    }

class BassInstrument(Instrument):
    PLAYERS = {
        "Straight line": Player,
        "Jazz line": Player
    }

class KeyboardInstrument(Instrument):
    PLAYERS = {
        "Straigh": PianoPlayer,
        "Oom pah": Player
    }

class DrumInstrument(Instrument):
    PLAYERS = {
        "Simple": DrumPlayer,
        "Shuffle": DrumPlayer
    }



class InstrumentsApi(object):
    INSTRUMENTS = {
        "": NoneInstrument,
        "Guitar": GuitarInstrument,
        "Bass": BassInstrument,
        "Keyboard": KeyboardInstrument,
        "Drums": DrumInstrument
    }

    def __init__(self):
        self.active = []
        self.preview = []
        self._instruments = {}

    @property
    def active_instruments(self):
        return [(c, self._instruments.get(c).get("player")) for c in self.active]

    @property
    def preview_instruments(self):
        return [(c, self._instruments.get(c).get("player")) for c in self.preview]

    def create(self, channel):
        self._instruments[channel] = {
            "instrument": NoneInstrument,
            "player": NonePlayer
        }

    def set_active(self, channel, state):
        if state and channel not in self.active:
            self.active.append(channel)
        elif not state and channel in self.active:
            self.active.remove(channel)

    def set_preview(self, channel, state):
        if state and channel not in self.preview:
            self.preview.append(channel)
        elif not state and channel in self.preview:
            self.preview.remove(channel)
    
    def set_instrument(self, channel, name=""):
        instrument = self.INSTRUMENTS.get(name)
        first_player = list(instrument.PLAYERS.keys())[0]
        print("SET INST")
        print(channel, name)
        self._instruments[channel] = {
            "instrument": instrument,
            "player": instrument.PLAYERS.get(first_player)
        }
        print(self._instruments.get(channel))

    def set_player(self, channel, name):
        print("SET INST")
        print(channel, name)
        instrument = self._instruments.get(channel)["instrument"]
        player = instrument.PLAYERS.get(name) or NonePlayer

        self._instruments[channel]["player"] = player
        print(self._instruments.get(channel))

    @property
    def names(self):
        return list(self.INSTRUMENTS.keys())

    def get_instrument(self, name):
        return self.INSTRUMENTS

    def get_players(self, instrument):
        return self.INSTRUMENTS.get(instrument).PLAYERS

instruments_api = InstrumentsApi()
