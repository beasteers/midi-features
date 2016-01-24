
from src.Composer import Composer
import os

parent = os.path.dirname(__file__)


## Creates a composer object and adds two pieces
chopin = Composer("Frederic Chopin")
chopin.addPiece(parent+"/samples/chopin-revolutionary.mid", {
    'name': "Etude in Cm: Revolutionary",
    'minor': 1
})
chopin.addPiece(parent+"/samples/chopin-nocturne-gm.mid", {
    'name': "Nocturne in Gm",
    'minor': 1
})

## Calculates the transition matrix of both pieces (merged)
chopin.getTM()

## Outputs midi to the first midi outbound port
chopin.generateMidi()