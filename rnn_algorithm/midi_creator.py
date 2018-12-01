from music21 import instrument, note, stream, chord

def create_midi(out_f):
    diff = 0
    out_note_seq = []

    for pred in out_f:
        if ('.' in pred) or pred.isdigit():
            notes_in_chord = pred.split('.')
            notes = create_chord(notes_in_chord)
            chord_ = chord.Chord(notes)
            chord_.diff = diff
            out_note_seq.append(chord_)
        else:
            note_ = note.Note(pred)
            note_.diff = diff
            note_.storedInstrument = instrument.Piano()
            out_note_seq.append(note_)
        diff += 0.5

    midi_stream = stream.Stream(out_note_seq)

    midi_stream.write('midi', fp='predicted/song.mid')

def create_chord(notes_in_chord):
    notes = []
    for current_note in notes_in_chord:
        note_ = note.Note(int(current_note))
        note_.storedInstrument = instrument.Piano()
        notes.append(note_)

