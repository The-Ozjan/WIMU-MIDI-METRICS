import music21 as m21


def find_time_signature(midi_file_path: str):
    """
    Gathers information about time signature from a MIDI file

    midi_file_path: specify a path to the file you want to analyze

    returns: list of time offsets when the data appears, list of time signature values throughout the file
    """
    midi_stream = m21.converter.parse(midi_file_path)
    tsList = midi_stream.flatten().getTimeSignatures()

    offsets = []
    ratios = []
    for signature in tsList:
        offsets.append(signature.offset)
        ratios.append(signature.ratioString)

    return offsets, ratios
