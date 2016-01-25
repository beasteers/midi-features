# -*- coding: utf-8 -*-

import rtmidi
import random
import time

class midiGenerator(object):
    def __init__(self, tms, options={}):
        self.options = {
            'interval': 0.15,
        }
        self.options.update(options)

        self.running = False
        self.tm = tms
        self.queue = {}
        self.lastNote = 0
        
        for name, tm in self.tm.iteritems():
            self.queue[name] = self.getRandomQueue(tm['matrix'], [])
        
        #initialize midi output
        self.midiout = rtmidi.MidiOut()
        if self.midiout.get_ports():
            self.midiout.open_port(0)
        else:
            self.midiout.open_virtual_port("Midi Generator Virtual Port")
     
     
    
    def getRandomQueue(self, arr, queue):
        if type(arr) is dict:
            i = random.choice(arr.keys())
            if type(arr[i]) is not dict: return queue
            queue.append(i)
            print i
            return self.getRandomQueue(arr[i], queue)
        else:
            return queue
     
    ## traverse down n(length of queue) dimensions and get weighted random value
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
    
    
    ## Send midi note on/off
    
    def noteOn(self, n, vel=127):
        self.midiout.send_message([0x90, n, vel])
    def noteOff(self, n):
        self.midiout.send_message([0x80, n, 0])
       
    
    def getNext(self, name, default=None):
        if name in self.tm:
            return self.getRecursive(self.tm[name]['matrix'], self.queue[name])
        else:
            return default
    
    ## Start/Stop Midi
    
    def start(self):
        self.running = True
        while self.running:
            self.run()
    
    def stop(self):
        self.running = False
        
    ## Repeated procedure to play midi
    def run(self):
        
        ### based off pitches matrix
        #note = self.getNext('pitches') + self.getNext('octaves')*12
        
        ### based off interval matrix
        self.lastNote += self.getNext('interval')
        note = self.lastNote + self.getNext('octaves')*12
        
        self.noteOn(note)
        dur = self.getNext('durations', self.options['interval'])
        time.sleep(dur)
        self.noteOff(note)
    
        
       
    
    
    