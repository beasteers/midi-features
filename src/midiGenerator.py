# -*- coding: utf-8 -*-

import rtmidi
import random
import time

class midiGenerator(object):
    def __init__(self, tms, options={}):
        self.options = {
            'interval': 0.15
        }
        self.options.update(options)

        self.running = False
        
        self.octave = 4
        self.pitches = tms['pitches']
        self.queue = {
            'pitches': [0 for a in range(self.pitches['order'])] ##should get other way
        }
        
        #initialize midi output
        self.midiout = rtmidi.MidiOut()
        if self.midiout.get_ports():
            self.midiout.open_port(0)
        else:
            self.midiout.open_virtual_port("Midi Generator Virtual Port")
        
        
    def getRecursive(self, arr, queue, j=0):
        if j < len(queue):
            return self.getRecursive(arr[queue[j]], queue, j+1)
        else:
            i = self.weightedRandom(arr)
            del queue[0]
            queue.append(i)
            return i
        
    def weightedRandom(self, arr):
        weights = list(arr.values())
        rnd = random.random() * sum(weights)
        for i, w in arr.iteritems():
            rnd -= w
            if rnd < 0:
                return i
    
    
    ########################
    ## Send midi note on/off
    ########################
    def noteOn(self, n, vel=127):
        self.midiout.send_message([0x90, n, vel])
    def noteOff(self, n):
        self.midiout.send_message([0x80, n, 0])
       
    
    def getNextNote(self):
        return self.getRecursive(self.pitches['matrix'], self.queue['pitches'])
    
    
    ########################
    ## Start/Stop Midi
    ########################    
    def start(self):
        self.running = True
        while self.running:
            self.run()
    
    def stop(self):
        self.running = False
        
    
    def run(self):
        note = self.getNextNote() + self.octave*12
        print note
        self.noteOn(note)
        time.sleep(self.options['interval'])
        self.noteOff(note)
    
        
       
    
    
    