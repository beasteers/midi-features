
from src.Composer import Composer
import os
import time

# start_time = time.clock()
# print("--- %s seconds ---" % (time.clock() - start_time))
# quit()


parent = os.path.dirname(__file__)

midiOptions = {'pitch-based': True}

# testing = 'bach'
# testing = 'hp'
testing = 'chopin'

if testing == 'bach':
    # Using bach violin sonatas cuz they're mostly monophonic
    bach = Composer("J.S. Bach")
    bach.addPiece(parent+"/samples/bach/partita1-dblalle.mid", {
        'name': "Partita No. 1: Double Allemande",
        'minor': 1
    })
    bach.addPiece(parent+"/samples/bach/partita1-cour.mid", {
        'name': "Partita No. 1: Courante",
        'minor': 1
    })
    bach.addPiece(parent+"/samples/bach/partita1-dblcour.mid", {
        'name': "Partita No. 1: Double Courante",
        'minor': 1
    })
    bach.addPiece(parent+"/samples/bach/partita1-sara.mid", {
        'name': "Partita No. 1: Sarabande",
        'minor': 1
    })
    bach.addPiece(parent+"/samples/bach/sonata2-allegro.mid", {
        'name': "Partita No. 1: Allegro",
        'minor': 1
    })
    bach.generateTM(10)
    bach.generateMidi(midiOptions)
    
    
elif testing == 'hp':
    hp = Composer('John Williams')
    hp.addPiece(parent+"/samples/hp-theme-monophonic.mid", {
        'name': "Harry Potter Theme",
        'minor': 1
    })
    hp.generateTM(12)
    hp.generateMidi()
    
    
    
elif testing == 'chopin':
    # Creates a composer object and adds two pieces
    chopin = Composer("Frederic Chopin")
    chopin.addPiece(parent+"/samples/chopin-revolutionary.mid", {
        'name': "Etude in Cm: Revolutionary",
        'minor': 1
    })
    chopin.addPiece(parent+"/samples/chopin-nocturne-gm.mid", {
        'name': "Nocturne in Gm",
        'minor': 1
    })
    
    quit()
    # Calculates the transition matrix of both pieces (merged)
    chopin.generateTM(8)
    
    # Outputs midi to the first midi outbound port
    chopin.generateMidi(midiOptions)
    
    