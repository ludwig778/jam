import json
import os.path

from beethoven.settings import ROOT_DIR


def get_directory():
    with open(os.path.join(ROOT_DIR, "theory", "directory.json")) as fd:
        return json.loads(fd.read())


DIRECTORY = get_directory()


def add_major_label(intervals):
    return [
        "{}{}".format(
            interval,
            "M" if interval in ["2", "3", "6", "7"] else ""
        ) for interval in intervals.split(',')
    ]


def get_scales_directory():
    directory, display_directory, reverse_directory = {}, [], {}
    for scale in DIRECTORY.get("scales"):
        if "label" in scale:
            display_directory.append(("label", scale.get("label")))
            continue
        intervals, names = (add_major_label(scale.get("intervals")),
                            scale.get("names"))
        for name in names:
            if name:
                directory.update({name: intervals})
        display_directory.append((names[0], intervals))
        reverse_directory.update({frozenset(intervals): names})
    return directory, display_directory, reverse_directory


def get_chords_directory():
    directory, display_directory, reverse_directory = {}, [], {}
    for scale in DIRECTORY.get("chords"):
        if "label" in scale:
            continue
        intervals, names = (add_major_label(scale.get("intervals")),
                            scale.get("names"))
        for name in names:
            if name:
                directory.update({name: intervals})
        display_directory.append((names[0], intervals))
        reverse_directory.update({frozenset(intervals): names})
    return directory, display_directory, reverse_directory


class ScaleDirectory(object):
    _DIR, _DISPLAY, _REVERSE_DIR = get_scales_directory()


class ChordDirectory(object):
    _DIR, _DISPLAY, _REVERSE_DIR = get_chords_directory()
