import numpy

numpy.random.seed(42)

def prepare_sequences(notes, pitches, vocab_size):
    note_to_int = dict((note, number) for number, note in enumerate(pitches))

    note_seq = 100
    in_f = []
    output = []
    for i in range(0, len(notes) - note_seq, 1):
        seq_notes = notes[i:i + note_seq]
        next_note = notes[i + note_seq]
        in_f.append([note_to_int[char] for char in seq_notes])
        output.append(note_to_int[next_note])

    count_of_obj = len(in_f)
    in_f_norm = numpy.reshape(in_f, (count_of_obj, note_seq, 1))
    in_f_norm = in_f_norm / float(vocab_size)

    return (in_f, in_f_norm)


def generate_notes(LSTM, in_f, pitches, vocab_size):
    
    starting_notes = numpy.random.randint(0, len(in_f)-1)
    
    int_to_note = dict((number, note) for number, note in enumerate(pitches))
    
    note_seq = in_f[starting_notes]
    out_f = []
    
    for note_index in range(100):
        in_f_predicted = numpy.reshape(note_seq, (1, len(note_seq), 1))
        in_f_predicted = in_f_predicted / float(vocab_size)
        
        pred = LSTM.predict(in_f_predicted, verbose=0)
        idx = numpy.argmax(pred)
        res = int_to_note[idx]
        out_f.append(res)

        note_seq.append(idx)
        note_seq = note_seq[1:len(note_seq)]

    return out_f
    
    