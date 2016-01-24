# -*- coding: utf-8 -*-
#from Piece import Piece
import midi
from Markov import MarkovChain
from midiGenerator import midiGenerator

normalizer = {
    'note': {
        '-7': 11,
        '-6': 6,
        '-5': 1,
        '-4': 8,
        '-3': 3,
        '-2': 10,
        '-1': 5,
        '0': 0,
        '1': 7,
        '2': 2,
        '3': 9,
        '4': 4,
        '5': 11,
        '6': 6,
        '7': 1
    }
}



class Composer(MarkovChain):
    def __init__(self, name):
       self.name = name
       self.pieces = []
       self.pitchTM = {}
    
    def addPiece(self, filename, meta={}):
        piece = Piece(filename, meta)
        self.pieces.append(piece)
        
    def getPiece(self, i):
        return self.pieces[i]
    def getLastPiece(self):
        return self.pieces[-1]
        
    def getTM(self):
        for p in self.pieces:
            self.setTransitionMatrix(p.notes, self.pitchTM, 3)
            
    def generateMidi(self):
        gen = midiGenerator({'pitches': self.pitchTM }, {'interval': 0.15})
        gen.start()


class Piece(object):
    def __init__(self, filename, meta):
       self.meta = meta
       self.notes = []
       self.durations = []
       
       
       self.parseFile(filename)
        
        
    def parseFile(self, filename):
        file = midi.read_midifile(filename)
        rawmeta = file[0]
        noteEvents = file[1]
        tick = 0
        meta = {
            'key': 0,
            'timeSignature':[4, 4]
       }
        # activeNotes = {}
        
        #pull out meta data
        for m in rawmeta:
            if isinstance(m, midi.events.KeySignatureEvent):
                meta['key'] = m.data[0] - 256 if m.data[0] > 127 else m.data[0] # key is # of sharps < 0 < # of flats
                meta['minor'] = m.get_minor()
            elif isinstance(m, midi.events.TimeSignatureEvent):
                meta['timeSignature'] = [m.data[0], 2**m.data[1]]
            elif isinstance(m, midi.events.SetTempoEvent):
                meta['tempo'] = m.data
        
        #override with manual meta data
        meta.update(self.meta)
        self.meta = meta
        currentKey = normalizer['note'][str(self.meta['key'])] #+self.meta['minor']*3
        
        #pull out note data
        for n in noteEvents:
            if n.tick != None:
                tick += n.tick
            if isinstance(n, midi.events.NoteOnEvent) and n.data[1] != 0:
                normalized = self.normalizeNote(n.data[0], currentKey)
                self.notes.append(normalized)

    ### Makes note to relative to tonic  
    def normalizeNote(self, note, normalizer):
        return (note - normalizer) % 12




