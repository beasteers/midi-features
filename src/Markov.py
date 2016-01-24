# -*- coding: utf-8 -*-

class MarkovChain(object):
    
    def setTransitionMatrix(self, stream, tm = {}, order = 3):
        tm.setdefault('order', order)
        tm.setdefault('matrix', {})
        
        ## Use sliding window to traverse stream
        for i in range(len(stream)-tm['order']):
            self.incRecursive(tm['matrix'], stream, tm['order'], i)
    
    ## Recurse thru set # of dimensions and increment value at end
    def incRecursive(self, arr, stream, d, i):
        if d == 0: #we're here, increment counter
            if stream[i] not in arr: arr[stream[i]] = 0 #default value
            arr[stream[i]] += 1
            
        else: #go deeper!!
            if stream[i] not in arr: arr[stream[i]] = {} #default value
            self.incRecursive(arr[stream[i]], stream, d-1, i+1)
    
        
