
from src.Composer import Composer
import os

parent = os.path.dirname(__file__)

## Using bach violin sonatas cuz they're mostly monophonic
bach = Composer("J.S. Bach")
bach.addPiece(parent+"/samples/bach/sonata2-allegro.mid", {
    'name': "Partita No. 1: Courante",
    'minor': 1
})
# bach.addPiece(parent+"/samples/bach/partita1-dblcour.mid", {
#     'name': "Partita No. 1: Double Courante",
#     'minor': 1
# })
bach.getTM(8)
bach.generateMidi()

## Creates a composer object and adds two pieces
# chopin = Composer("Frederic Chopin")
# chopin.addPiece(parent+"/samples/chopin-revolutionary.mid", {
#     'name': "Etude in Cm: Revolutionary",
#     'minor': 1
# })
# chopin.addPiece(parent+"/samples/chopin-nocturne-gm.mid", {
#     'name': "Nocturne in Gm",
#     'minor': 1
# })

## Calculates the transition matrix of both pieces (merged)
# chopin.getPitchTM()

## Outputs midi to the first midi outbound port
# chopin.generateMidi()