# -*- coding: utf-8 -*-
#from Piece import Piece
import midi
from Markov import MarkovChain
from midiGenerator import midiGenerator

## Used to adjust notes to their relative keys
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
       self.durationTM = {}
       self.octaveTM = {}
       self.intervalTM = {}
    
    def addPiece(self, filename, meta={}):
        piece = Piece(filename, meta)
        self.pieces.append(piece)
        
    def getPiece(self, i):
        return self.pieces[i]
    def getLastPiece(self):
        return self.pieces[-1]
        
    def generateTM(self, order=3):
        for p in self.pieces:
            self.setTransitionMatrix(p.notes, self.pitchTM, order)
            self.setTransitionMatrix(p.durations, self.durationTM, order)
            self.setTransitionMatrix(p.octaves, self.octaveTM, order)
            self.setTransitionMatrix(p.intervals, self.intervalTM, order)
            
    def generateMidi(self):
        gen = midiGenerator({
            'pitches': self.pitchTM,
            'durations': self.durationTM,
            'octaves': self.octaveTM,
            'interval': self.intervalTM
        }, {'interval': 0.15})
        gen.start()


class Piece(object):
    def __init__(self, filename, meta):
       self.meta = meta
       self.notes = []
       self.durations = []
       self.octaves = []
       self.intervals = []
       
       
       self.parseFile(filename)
        
         
    def parseFile(self, filename):
        file = midi.read_midifile(filename)
        rawmeta = file[0]
        noteEvents = file[1]
        transient = {}
        tick = 0
        meta = {
            'key': 0,
            'timeSignature':[4, 4],
            'tempo': 120,
            'PPQ': file.resolution
        }
        
        #pull out meta data
        for m in rawmeta:
            if isinstance(m, midi.events.KeySignatureEvent):
                key = m.data[0] - 256 if m.data[0] > 127 else m.data[0] # key is # of sharps > 0 > # of flats
                self.bufferMeta('key', key, m.tick, meta, transient)
                self.bufferMeta('minor', m.get_minor(), m.tick, meta, transient)
            elif isinstance(m, midi.events.TimeSignatureEvent):
                self.bufferMeta('timeSignature', [m.data[0], 2**m.data[1]], m.tick, meta, transient)
            elif isinstance(m, midi.events.SetTempoEvent):
                self.bufferMeta('tempo', m.get_bpm(), m.tick, meta, transient)
        
        #override with manual meta data
        meta.update(self.meta)
        self.meta = meta
        
        #retrieve normalized key - the minor flag is not reliable in the midi data so it may have to be manually overriden for minor pieces in most cases
        currentKey = normalizer['note'][str(self.meta['key']+self.meta['minor']*3)] 
        
        lastNote=0
        #pull out note data
        for n in noteEvents:
            if n.tick != None:
                tick += n.tick
            if isinstance(n, midi.events.NoteOnEvent) and n.data[1] != 0:
                note = n.data[0]
                octave = self.getOctave(note)
                self.octaves.append(octave)
                self.intervals.append(note-lastNote)
                lastNote = note
                normalized = self.normalizeNote(note, currentKey)
                self.notes.append(normalized)
            elif isinstance(n, midi.events.NoteOffEvent) or (len(n.data)>1 and n.data[1] == 0):
                dur = self.ticksToSecs(n.tick, meta['PPQ'], meta['tempo'])
                self.durations.append(dur)
                
    
    
    ### Makes note to relative to tonic  
    def normalizeNote(self, note, normalizer):
        return (note - normalizer) % 12
    
    def getOctave(self, note):
        return note // 12
    
    def ticksToSecs(self, ticks, ppq, bpm):
        return ticks * 60.0 / (ppq*bpm)
    
    def bufferMeta(self, name, value, tick, is0, not0):
        if (tick == 0):
            is0[name] = value
        else: #buffer meta values for later
            if tick not in not0: not0[tick] = {} #not0.setdefault(tick, {})
            not0[tick][name] = value



