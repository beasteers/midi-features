
from src.Composer import Composer
import os

parent = os.path.dirname(__file__)

chopin = Composer("Frederic Chopin")
chopin.addPiece(parent+"/samples/chopin-revolutionary.mid", {
    'name': "Etude in Cm: Revolutionary",
    'minor': 1
})
chopin.addPiece(parent+"/samples/chopin-nocturne-gm.mid", {
    'name': "Nocturne in Gm",
    'minor': 1
})

chopin.getTM()

chopin.generateMidi()