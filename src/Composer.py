# -*- coding: utf-8 -*-
#from Piece import Piece
import midi, math
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
       self.velocityTM = {}
    
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
            self.setTransitionMatrix(p.velocity, self.velocityTM, order)
            
    def generateMidi(self, options):
        gen = midiGenerator({
            'pitches': self.pitchTM,
            'durations': self.durationTM,
            'octaves': self.octaveTM,
            'interval': self.intervalTM,
            'velocity': self.velocityTM
        }, options)
        gen.start()


class Piece(object):
    def __init__(self, filename, meta):
        
        self.meta = meta
        self.notes = []
        self.durations = []
        self.octaves = []
        self.intervals = []
        self.velocity = []
        
        self.pitchDensity = {}
        
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
        noteEvents.make_ticks_abs()
        
        #pull out meta data
        for m in rawmeta:
            if isinstance(m, midi.events.KeySignatureEvent):
                self.bufferMeta('key', m.get_alternatives(), m.tick, meta, transient) # key is # of sharps > 0 > # of flats
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
        
        activeKeys = {}
        # print noteEvents
        # quit()
        
        totalNotes=0
        lastNote=0
        #pull out note data
        for n in noteEvents:
            if n.tick != None:
                tick += n.tick
            if self.isNoteEvent(n) == 1: #1 is noteOn
                note = n.data[0]
                velocity = n.data[1]
                
                octave = self.getOctave(note)
                self.octaves.append(octave)
                
                self.velocity.append(velocity)
                
                self.intervals.append(note-lastNote)
                lastNote = note
                
                activeKeys[note] = n.tick
                
                normalized = self.normalizeNote(note, currentKey)
                self.notes.append(normalized)
                
                if normalized not in self.pitchDensity: self.pitchDensity[normalized] = 0
                self.pitchDensity[normalized] += 1
                totalNotes+=1
            elif self.isNoteEvent(n) == 0: #0 is noteOff
                
                ## Need to add note ordering. Notes are only added at the noteOff command
                ## Append both start tick and duration ticks to duration then sort by start ticks
                startTick = activeKeys.pop(n.data[0], None)
                if startTick != None:
                    noteTicks = n.tick - startTick
                    dur = self.ticksToSecs(noteTicks, self.meta['PPQ'], self.meta['tempo'])
                    self.durations.append((startTick, dur))
        
        # Sort durations by start time
        # Will need to do with any temporal dependent elements
        self.durations.sort(key=lambda tup: tup[0])
        self.durations = [x[1] for x in self.durations]
        
        
        for i in range(len(self.pitchDensity)):
           self.pitchDensity[i] = math.ceil(self.pitchDensity[i]/float(totalNotes)*10000)/10000           
        
        print self.meta['name']+": "
        print self.pitchDensity
        print ""
               
    ## Returns 1 if Note On, 0 if Note Off, and -1 if neither
    def isNoteEvent(self, n):
        if isinstance(n, midi.events.NoteOnEvent) and n.data[1] != 0: return 1
        elif isinstance(n, midi.events.NoteOffEvent) or (isinstance(n, midi.events.NoteOnEvent) and n.data[1] == 0): return 0
        else: return -1
    
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



