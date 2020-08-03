

def get_ascii_fingerboard(scale, tuning, fret_nb=12):
    DOTS = [0, 3, 5, 7, 9]
    board = ""
    notes = {note.semitones: note for note in scale.notes}
    for _string, note, index in tuning.strings:
        board += "{:^3s} ||".format(note.note_name)
        for i in range(1, fret_nb + 1):
            note = notes.get((index + i) % 12)
            board += "{:^3s}|".format(note.note_name if note else "")
        board += "\n"

    board += "    0 "
    for i in range(1, fret_nb + 1):
        board += "{:^3s} ".format(str(i) if (i % 12) in DOTS else "")
    # board += "\n"
    return board
