from beethoven.theory.scales import Scale


class Harmony(object):
    _C_SCALE = Scale(root="C", name="major")
    _DEGREES = ["I", "II", "III", "IV", "V", "VI", "VII"]
    _FUNCTIONS = {"tonic": ["1", "3", "6"],
                  "subdominant": ["2", "4"],
                  "dominant": ["5", "7"]}
