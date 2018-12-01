# sudo pip install pyknon
# timidity -Or -o - first.mid | lame -r - first.mp3 (convert)
# for running #timidity -T 350 demo.mid

from pyknon.genmidi import Midi
from pyknon.music import NoteSeq

import sys
import random
import os
import subprocess as sub
import re
import time
sys.setrecursionlimit(10000000)


NOTES_COUNT = 100
MELODIES_COUNT = 7
# melodies contains NoteSeq objects
melodies = []

# sample notes pool // Q = Quarter notes // E = One Eigth Notes
quarters = ['C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'Bb4', 'B4']
eights = ['C8', 'C#8', 'D8', 'D#8', 'E8', 'F8', 'F#8', 'G8', 'G#8', 'A8', 'Bb8', 'B8']
sixteenth = ['C16', 'C#16', 'D16', 'D#16', 'E16', 'F16', 'F#16', 'G16', 'G#16', 'A16', 'Bb16', 'B16']
thirtySecond = ['C32', 'C#32', 'D32', 'D#32', 'E32', 'F32', 'F#32', 'G32', 'G#32', 'A32', 'Bb32', 'B32']
rest = ['R16', 'R32']

notesPoolA = sixteenth + thirtySecond + rest + eights


experimentName = sys.argv[1]
generationCount = 0
ins = 0
globalIter = 0


class Melody:
    def __init__(self, notes):
        self.notes = notes
        self.score = 1

    def mutation(self, mutationRate = 0.45):
        for i in range(len(self.notes)):
            if random.random() < mutationRate:
                self.notes = self.notes[:i] + NoteSeq(random.choice(notesPoolA)) + self.notes[i + 1:]

    def showNotes(self):
        print("\t%s%s" % (str(self.notes).ljust(int(NOTES_COUNT * 8)), self.score))

def crossover(a, b):
    child = Melody(a.notes)
    midpoint = random.randrange(len(a.notes))
    child.notes = a.notes[:midpoint] + b.notes[midpoint:]
    return child



def generateMid(melody, melodyNum, lastMelody = False):

    global generationCount
    global ins

    midi = Midi(instrument = ins)
    midi.seq_notes(melody.notes)

    path = "midi/" + experimentName + "/gen" + str(generationCount) + "/"

    if not os.path.exists(path):
        os.makedirs(path)

    if lastMelody:
        midi.write("midi/"+ experimentName + "/gen" + str(generationCount) + "/*melody" + str(melodyNum) + "*.mid")
    else:
        midi.write(path + "melody" + str(melodyNum) + ".mid")

def playMid(melodyNum):
    p = sub.Popen(['timidity','-T','340', "midi/"+ experimentName + "/gen" + str(generationCount) + "/melody" + str(melodyNum) +".mid"], stdout=sub.PIPE, stderr=sub.PIPE)
    time.sleep(5)
    p.terminate()

def showAllMelodies():
    print('\n\tNOTES'.ljust(int(NOTES_COUNT * 8)) + 'SCORE')
    for i in melodies:
            i.showNotes()
    print

def evolution():
    global globalIter
    print("EVOLUTION IS STARTING:) 100 iterations.......................................")

    for i in range(0, 1000):
        print("crossover... selection... mutation... iteration number ", globalIter)
        globalIter = globalIter + 1
        elementsForMating = []

        melodies.sort(key=lambda x : x.score, reverse=True)

        for i in range(MELODIES_COUNT):
            for j in range(melodies[i].score):
                elementsForMating.append(melodies[i])

        for i in range(MELODIES_COUNT):
            random.seed(42)
            a, b = random.sample(elementsForMating, 2)
            child = crossover(a, b)
            child.mutation()
            melodies[i] = child
    print('DONE..................................................................\n')


def geneticInput():
        global generationCount
        global ins

        showAllMelodies()

        while True:
            print('Please, write the command: (ex: "p 1")')
            command = input()
            match = re.search(r'(\w*) ?(\d*) ?(\d*)', command)

            if command == 'exit':
                break
            if match.group(1) == 'play' or match.group(1) == 'p':
                melodyNumber = int(match.group(2)) - 1
                generateMid(melodies[melodyNumber], melodyNumber)
                playMid(melodyNumber)
                showAllMelodies()

            if match.group(1) == 'score' or match.group(1) == 's':
                print('scoring...')
                time.sleep(0.5)
                melodyNumber, score = int(match.group(2)) - 1, int(match.group(3))
                melodies[melodyNumber].score = score
                showAllMelodies()

            if match.group(1) == 'instrument' or match.group(1) == 'i':
                ins = int(match.group(2))

            if match.group(1) == 'done' or match.group(1) == 'd':
                evolution()
                showAllMelodies()
                continue
            if match.group(1) == 'choose' or match.group(1) == 'c':
                melodyNumber = int(match.group(2)) - 1
                generateMid(melodies[melodyNumber], melodyNumber, True)
                playMid(melodyNumber)
                print('Great!) Enjoy your generated music!!! :D')
                time.sleep(0.5)
                return False


def main():
    # example of the representation of a dataset
    notes_all =[['F3', 'F3', 'B-4', 'F3', 'G4', 'G#4', 'F4', 'F3', 'G4', 'G3', 'E-4', 'G#3', 'F3', 'F5', 'G5', 'G#5', 'F3', 'B-5', 'G5', 'G#5', 'F3', 'B-5', 'C6', 'B-5', 'F3', 'E-6', 'C#4', 'F6', 'C4', 'F3', 'F3', 'B-4', 'F3', 'G4', 'G#4', 'F4', 'F3', 'G4', 'G3', 'E-4', 'G#3', 'F3', 'F5', 'G5', 'G#5', 'F3', 'B-5', 'G5', 'G#5', 'F3', 'B-5', 'C6', 'B-5', 'F3', 'E-6', 'E-3', 'F6', 'E3', 'F2', 'F2', 'B-4', 'F2', 'G4', 'G#4', 'B-2', 'F4', 'G4', 'C3', 'E-4', 'F2', 'F5', 'G5', 'G#5', 'F2', 'B-5', 'G5', 'G#5', 'F2', 'B-5', 'C6', 'B-5', 'F2', 'E-6', 'C#3', 'F6', 'C3', 'F2', 'F2', 'B-4', 'F2', 'G4', 'G#4', 'B-2', 'F4', 'G4', 'C3', 'E-4', 'F2', 'F5', 'G5'], ['F2', 'B-2', 'G4', 'G#4', 'F4', 'C4', 'E-4', 'F2', 'C4', 'E-4', 'F4', 'B-2', 'F2', 'B-2', 'G4', 'G#4', 'F4', 'C4', 'E-4', 'F2', 'C4', 'F4', 'C4', 'F2', 'C3', 'E-5', 'E5', 'C3', 'C5', 'G4', 'C5', 'E5', 'F5', 'B-2', 'F4', 'F4', 'F4', 'G4', 'G#4', 'B-2', 'F4', 'F4', 'C5', 'G4', 'C5', 'G#4', 'F4', 'C4', 'E-4', 'F4', 'B5', 'C6', 'G#5', 'F5', 'G#4', 'A4', 'F5', 'D5', 'C5', 'A4', 'C4', 'B-2', 'E3', 'E-4', 'D4', 'C4', 'D3', 'G#3', 'B-5', 'C6', 'F5', 'C5', 'D5', 'E-5', 'C5', 'D5', 'E-5', 'C5', 'C#3', 'B-2', 'G4', 'C5', 'G#4', 'F4', 'C4', 'E-4', 'F4', 'B5', 'C6', 'G#5', 'F5', 'G#4', 'A4', 'F5', 'D5', 'C5', 'A4', 'C4', 'B-2', 'F#3'], ['C5', 'F5', 'G5', 'F5', 'B-5', 'C6', 'G5', 'B4', 'C5', 'D5', 'A5', 'G5', 'E-5', 'E-5', 'F5', 'G5', 'C6', 'A5', 'F5', 'G5', 'D6', 'A5', 'G5', 'B4', 'C5', 'D5', 'A5', 'G5', 'E-5', 'E-5', 'F5', 'E-4', 'D4', 'C4', 'B-3', 'A3', 'G3', 'F3', 'G3', 'G3', 'D3', 'G3', 'G3', 'D3', 'G3', 'G3', 'D3', 'G3', 'G3', 'D3', 'D5', 'E-3', 'G3', 'B-3', 'D4', 'G4', 'E-3', 'G3', 'B-3', 'D4', 'F5', 'E-3', 'G3', 'B-3', 'D4', 'E-5', 'E-3', 'G3', 'D5', 'B-3', 'D4', 'C5', 'E-3', 'F3', 'D5', 'A3', 'C4', 'A4', 'E-3', 'F3', 'A3', 'C4', 'E-3', 'F3', 'A3', 'C4', 'E-3', 'F3', 'A3', 'C4', 'C5', 'D3', 'F3', 'D5', 'A3', 'C4', 'A4', 'D3', 'F3', 'A3'], ['F3', 'C4', 'E4', 'C4', 'E4', 'C4', 'E4', 'C4', 'F3', 'C4', 'E4', 'C4', 'E4', 'C4', 'E4', 'C4', 'F3', 'C4', 'E4', 'C4', 'E4', 'C4', 'E4', 'C4', 'F3', 'C5', 'C4', 'D5', 'C4', 'C4', 'C4', 'F3', 'C4', 'F4', 'A4', 'C4', 'E5', 'F4', 'A4', 'C4', 'D5', 'F4', 'A4', 'C4', 'C5', 'F3', 'C4', 'F4', 'A4', 'C4', 'E5', 'F4', 'A4', 'C4', 'D5', 'F4', 'A4', 'C4', 'C5', 'F3', 'C4', 'F4', 'A4', 'C4', 'E5', 'F4', 'A4', 'C4', 'D5', 'F4', 'A4', 'C4', 'C5', 'F3', 'C5', 'C4', 'D5', 'C4', 'C4', 'F3', 'C4', 'A5', 'E4', 'E5', 'C4', 'F5', 'D4', 'E5', 'C4', 'A5', 'B3', 'E5', 'C4', 'F3', 'C4', 'A5', 'E4', 'E5', 'C4', 'F5'], ['G2', 'G3', 'G3', 'B2', 'G3', 'G3', 'A2', 'A3', 'A3', 'B2', 'G3', 'G3', 'G2', 'G3', 'G3', 'B2', 'G3', 'G3', 'A2', 'A3', 'A3', 'B2', 'G5', 'A5', 'B5', 'G3', 'B3', 'D4', 'B3', 'G3', 'B3', 'D6', 'D4', 'B5', 'B3', 'C3', 'G3', 'B5', 'C4', 'C6', 'B3', 'B5', 'C3', 'G5', 'G3', 'A5', 'C4', 'B5', 'G3', 'G3', 'B3', 'D4', 'B3', 'G3', 'B3', 'D4', 'F#3', 'G3', 'G3', 'D4', 'G5', 'A5', 'F#3', 'B5', 'G3', 'B3', 'D4', 'B3', 'G3', 'B3', 'D6', 'D4', 'B5', 'B3', 'C3', 'G3', 'B5', 'C4', 'C6', 'G3', 'B5', 'C3', 'G5', 'G3', 'A5', 'C4', 'B5', 'G3', 'B2', 'F#3', 'B3', 'F#3', 'B2', 'F#3', 'B3', 'F#3', 'B2', 'F#3', 'B3', 'F#3'], ['D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'C2', 'C2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'C2', 'C2', 'E4', 'D2', 'F4', 'D2', 'A4', 'D2', 'B-4', 'E-2', 'G4', 'E-2', 'B-4', 'E-2', 'A4', 'D2', 'D2', 'D4', 'D2', 'D2', 'E-2', 'D4', 'D2', 'D2', 'A3', 'D2', 'D2', 'E-2', 'D2', 'E4', 'D2', 'F4', 'D2', 'A4', 'D2', 'B-4', 'E-2', 'G4', 'E-2', 'B-4', 'E-2', 'A4', 'D2', 'D2', 'D4', 'D2', 'D2', 'G4', 'E-2', 'E-2', 'D4', 'D2', 'D2', 'D2', 'D2', 'E-2', 'D2', 'D2', 'D2', 'D2', 'E-2', 'E-2', 'E-2', 'E-2', 'D2', 'D2', 'D3', 'E-2', 'E-2', 'E-3', 'E-2', 'D2', 'D2', 'D3', 'E-2', 'E-2', 'E-3', 'D2', 'E-2', 'D2', 'D2', 'A2', 'D3', 'E-2', 'E-2', 'B-2'], ['A4', 'D4', 'B-4', 'F4', 'F5', 'C4', 'G4', 'E4', 'A4', 'B-3', 'E5', 'D4', 'F4', 'A3', 'C5', 'C4', 'D5', 'G3', 'E4', 'B-3', 'F4', 'D4', 'C5', 'A2', 'A4', 'D4', 'F4', 'A4', 'F4', 'E5', 'C4', 'E4', 'G4', 'E5', 'E4', 'A4', 'B-3', 'D4', 'F4', 'D4', 'A3', 'C4', 'G4', 'E4', 'A4', 'C4', 'D4', 'A4', 'A4', 'G4', 'E4', 'C4', 'A4', 'F3', 'A3', 'C4', 'B-4', 'A3', 'A4', 'D5', 'B-3', 'D4', 'F4', 'A4', 'D4', 'D5', 'E5', 'C4', 'E4', 'G4', 'G5', 'E4', 'F5', 'A3', 'C4', 'E5', 'E4', 'C4', 'D5', 'D3', 'A3', 'F5', 'D4', 'G5', 'A3', 'A5', 'G3', 'B-3', 'D4', 'B-3', 'G4', 'G3', 'A4', 'B-3', 'B-4', 'D4', 'F5', 'B-3', 'A3', 'A4']]

    for idx, note in enumerate(notes_all):
        print(idx)
        input_notes = NoteSeq(' '.join(note))
        melodies.append(Melody(input_notes))

    os.system('clear')
    print('---------Music generation using genetic algorithm')
    time.sleep(0.6)
    print('We will be using', MELODIES_COUNT, 'melodies'),
    print('with each having', NOTES_COUNT, 'notes.')
    time.sleep(1)
    print('\nThe contents of the music pool is shown below.')
    flag = geneticInput()

main()
