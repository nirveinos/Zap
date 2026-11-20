from puzzles import Wire,Resistor,Battery,Gate
from mapManager import Map,Wall
from Player import Player
levels = {
    1 : {
        "completed" : False,
        "map" : [10,10],
        "battery" : (10,(0,0)),
        "gate" : ((3,1),3),
        "wires" : [
            ((1, 0), ["LEFT", "DOWN"]),
            ((2, 0), ["LEFT", "RIGHT"]),
            ((2, 1), ["LEFT", "DOWN"]),
            ((2,2),["RIGHT","DOWN"]),
            ((2,3),["LEFT","RIGHT"]),
            ((3,3),["RIGHT","UP"]),

        ],
        "resistors" : [
            ((3,2),["LEFT","UP"],1)
        ],
        "walls" : [
            (1,1)
        ]

    },
    2 : None,
    3: None,
    4:None,
    5:None,
    6:None,
    7:None,
    8:None,
    9:None
}

def loadLevel(level):
    levelData = levels[level]
    mymap = Map(levelData["map"][0],levelData["map"][1])
    player = Player(mymap)
    battery = Battery(levelData["battery"][0],mymap,levelData["battery"][1])
    gate = Gate(levelData["gate"][0],mymap,levelData["gate"][1])
    for wire in levelData["wires"]:
        Wire(wire[0],wire[1],mymap)
    for resistor in levelData["resistors"]:
        Resistor(resistor[0],resistor[1],mymap,resistor[2])
    for wall in levelData["walls"]:
        Wall(mymap,wall)
    mymap.updateWires()
    return mymap,player,battery,gate