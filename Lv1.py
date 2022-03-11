from panda3d.core import CollisionTube, CollisionNode
from panda3d.core import *
from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from direct.interval.LerpInterval import *

loadPrcFileData("", "load-file-type p3assimp")                                # type: ignore

doors = {
    "D1": {
        "x":[3.30,4.70], "y":[-0.63,0.29],
        "status": "Open"},
    "D2": {
        "x":[3.30,4.70], "y":[14.52,15.03],
        "status": "Open"},
    "D3": {
        "x":[-3.82,-3.09], "y":[6.6,8.2],
        "status": "Open"},
    "D4": {
        "x":[10.78,11.94], "y":[6.6,8.2],
        "status": "Open"},
    "D5": {
        "x":[11.02,21.4], "y":[-0.63,0.29],
        "status": "Open"},
    "D6": {
        "x":[15.4,17], "y":[14.52,15.03],
        "status": "Open"},
    "D7": {
        "x":[24.4,25.9], "y":[14.52,15.03],
        "status": "Open"},
    "D8": {
        "x":[29.36,30.27], "y":[6.6,8.2],
        "status": "Open"},
    "D9": {
        "x":[36.5,38.1], "y":[-0.63,0.29],
        "status": "Open"},
    "D10": {
        "x":[44.43,45.1], "y":[6.6,8.2],
        "status": "Open"},
    "D11": {
        "x":[36.5,38.1], "y":[14.52,15.03],
        "status": "Open"},
    "D12": {
        "x":[44.43,45.1], "y":[22.3,23.9],
        "status": "Open"},
    "D13": {
        "x":[31.9,33.5], "y":[31,31.57],
        "status": "Open"},
    "D14": {
        "x":[20.31,20.95], "y":[22.3,23.9],
        "status": "Open"},
    "D15": {
        "x":[7.8,9.4], "y":[31,31.57],
        "status": "Open"},
    "D16": {
        "x":[-3.82,-3.09], "y":[22.3,23.9],
        "status": "Open"},
}

class Lv1():
    def __init__(self):
        base.player.actor.setPos(0,-3,0)                                      # type: ignore                                 

        self.environment = loader.loadModel("obj/lv1.obj")                    # type: ignore
        self.environment.reparentTo(render)                                   # type: ignore
        self.environment.setPos(0, 0, 0)
        self.environment.setHpr(0,90,0)
        
        self.environment.setScale(0.003, 0.002, 0.003)

        self.name = "Lv1"
        
        self.score = 0

        self.gameOver = None
        self.skipLevel = None
        self.cleared = None

        self.nextLevel = "Lv2"

        self.crossHair = OnscreenImage(image='pack.png', pos=(0, 0, 0),scale = 0.04)
        self.crossHair.setTransparency(TransparencyAttrib.MAlpha)
        
        # Sound
        self.playingSound = base.loader.loadSfx("Sounds/playing.ogg")         # type: ignore
        self.playingSound.setLoop(True)
        self.playingSound.setVolume(0.1) # 0.1
        
        self.doorSound = base.loader.loadSfx("Sounds/doorClosing.ogg")        # type: ignore
        self.doorSound.setLoop(False)
        self.doorSound.setVolume(0.04) # 0.04
        
        # Game-Over Screen
        self.gameOverBackdrop = DirectFrame(frameColor = (0, 0, 0, 1),
                                             frameSize = (-1, 1, -1, 1),
                                             parent = render2d)               # type: ignore
        self.gameOverBackdrop.hide()
        
        self.gameOverScreen = DirectFrame(frameColor = (1, 1, 1, 0))
        self.gameOverScreen.hide()
        
        title = DirectLabel(text = "GameOver!",
                            scale = 0.1,
                            pos = (0, 0, 0.4),
                            parent = self.gameOverScreen,
                            relief = None,
                            text_font = base.font,                            # type: ignore
                            text_fg = (1, 1, 1, 1))
        
        self.finalScoreLabel = DirectLabel(text = "",
                                   parent = self.gameOverScreen,
                                   scale = 0.1,
                                   pos = (0, 0, 0.2),
                                   text_font = base.font,                     # type: ignore
                                   relief = None,
                                   text_fg = (1, 1, 1, 1))
        
        self.message = DirectLabel(text = "",
                        parent = self.gameOverScreen,
                        scale = 0.1,
                        pos = (0, 0, 0),
                        text_font = base.font,                                # type: ignore
                        relief = None,
                        text_fg = (1, 1, 1, 1))
        
        btn = DirectButton(text = "Restart",
                           command = base.startGame,                          # type: ignore
                           pos = (0, 0, -0.2),
                           parent = self.gameOverScreen,
                           scale = 0.07,
                           text_font = base.font,                             # type: ignore
                           clickSound = loader.loadSfx("Sounds/UIClick.ogg"), # type: ignore
                           frameTexture = base.buttonImages,                  # type: ignore  
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)
        
        btn = DirectButton(text = "Quit",
                           command = base.quit,                               # type: ignore
                           pos = (0, 0, -0.4),
                           parent = self.gameOverScreen,
                           scale = 0.07,
                           text_font = base.font,                             # type: ignore
                           clickSound = loader.loadSfx("Sounds/UIClick.ogg"), # type: ignore
                           frameTexture = base.buttonImages,                  # type: ignore
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)
        
        # Outer Walls
        wallSolid = CollisionTube(-9.0, 0, 0, 50.3, 0, 0, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)                                 # type: ignore
        wall.setY(-5.9)
        # wall.show()

        wallSolid = CollisionTube(-9.0, 0, 0, 50.3, 0, 0, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)                                 # type: ignore
        wall.setY(37.2)
        # wall.show()

        wallSolid = CollisionTube(0, -5.9, 0, 0, 37.2, 0, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)                                 # type: ignore
        wall.setX(-9.0)
        # wall.show()

        wallSolid = CollisionTube(0, -5.9, 0, 0, 37.2, 0, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)                                 # type: ignore
        wall.setX(50.3)
        # wall.show()
        
        # Doors 1 - 5 - 9
        wallGap = CollisionNode("D1")
        wallGap.addSolid(CollisionTube(2.9, 0, 0, 5.1, 0, 0, 0.2))
        door = render.attachNewNode(wallGap)                                  # type: ignore
        door.setY(-0.1)
        door.stash()
        door.show()
        
        wallGap = CollisionNode("D5")
        wallGap.addSolid(CollisionTube(19.5, 0, 0, 21.7, 0, 0, 0.2))
        door = render.attachNewNode(wallGap)                                  # type: ignore
        door.setY(-0.1)
        door.stash()
        # door.show()
        
        wallGap = CollisionNode("D9")
        wallGap.addSolid(CollisionTube(36.2, 0, 0, 38.4, 0, 0, 0.2))
        door = render.attachNewNode(wallGap)                                  # type: ignore
        door.setY(-0.1)
        door.stash()
        # door.show()
        
        # Wall
        wallNode = CollisionNode("wall")
        wallNode.addSolid(CollisionTube(-3.1, 0, 0, 2.9, 0, 0, 0.2))
        wallNode.addSolid(CollisionTube(5.1, 0, 0, 19.5, 0, 0, 0.2))
        wallNode.addSolid(CollisionTube(21.7, 0, 0, 36.2, 0, 0, 0.2))
        wallNode.addSolid(CollisionTube(38.4, 0, 0, 44.4, 0, 0, 0.2))
        wall = render.attachNewNode(wallNode)                                 # type: ignore
        wall.setY(-0.05)
        # wall.show()
        
        # Doors 2 - 6 - 7 - 11
        wallGap = CollisionNode("D2")
        wallGap.addSolid(CollisionTube(2.9, 0, 0, 5.1, 0, 0, 0.2))
        door = render.attachNewNode(wallGap)                                  # type: ignore
        door.setY(14.75)
        door.stash()
        # door.show()
        
        wallGap = CollisionNode("D6")
        wallGap.addSolid(CollisionTube(15.1, 0, 0, 17.3, 0, 0, 0.2))
        door = render.attachNewNode(wallGap)                                  # type: ignore
        door.setY(14.75)
        door.stash()
        # door.show()
        
        wallGap = CollisionNode("D7")
        wallGap.addSolid(CollisionTube(24.1, 0, 0, 26.2, 0, 0, 0.2))
        door = render.attachNewNode(wallGap)                                  # type: ignore
        door.setY(14.75)
        door.stash()
        # door.show()
        
        wallGap = CollisionNode("D11")
        wallGap.addSolid(CollisionTube(36.2, 0, 0, 38.4, 0, 0, 0.2))
        door = render.attachNewNode(wallGap)                                  # type: ignore
        door.setY(14.75)
        door.stash()
        # door.show()
        
        # Wall
        wallNode = CollisionNode("wall")
        wallNode.addSolid(CollisionTube(-3.1, 0, 0, 2.9, 0, 0, 0.2))
        wallNode.addSolid(CollisionTube(5.1, 0, 0, 15.1, 0, 0, 0.2))
        wallNode.addSolid(CollisionTube(17.3, 0, 0, 24.1, 0, 0, 0.2))
        wallNode.addSolid(CollisionTube(26.2, 0, 0, 36.2, 0, 0, 0.2))
        wallNode.addSolid(CollisionTube(38.4, 0, 0, 44.4, 0, 0, 0.2))
        wall = render.attachNewNode(wallNode)                                 # type: ignore
        wall.setY(14.8)
        # wall.show()
        
        # Doors 15 - 13
        wallGap = CollisionNode("D15")
        wallGap.addSolid(CollisionTube(7.5, 0, 0, 9.7, 0, 0, 0.2))
        door = render.attachNewNode(wallGap)                                  # type: ignore
        door.setY(31.4)
        door.stash()
        # door.show()
        
        wallGap = CollisionNode("D13")
        wallGap.addSolid(CollisionTube(31.6, 0, 0, 33.8, 0, 0, 0.2))
        door = render.attachNewNode(wallGap)                                  # type: ignore
        door.setY(31.4)
        door.stash()
        # door.show()
        
        # Wall
        wallNode = CollisionNode("wall")
        wallNode.addSolid(CollisionTube(-3.1, 0, 0, 7.5, 0, 0, 0.2))
        wallNode.addSolid(CollisionTube(9.7, 0, 0, 31.6, 0, 0, 0.2))
        wallNode.addSolid(CollisionTube(33.8, 0, 0, 44.4, 0, 0, 0.2))
        wall = render.attachNewNode(wallNode)                                 # type: ignore
        wall.setY(31.4)
        # wall.show()
        
        # Doors 3 - 16
        wallGap = CollisionNode("D3")
        wallGap.addSolid(CollisionTube(0, 6.3, 0, 0, 8.5, 0, 0.2))
        door = render.attachNewNode(wallGap)                                  # type: ignore
        door.setX(-3.4)
        door.stash()
        # door.show()
        
        wallGap = CollisionNode("D16")
        wallGap.addSolid(CollisionTube(0, 22, 0, 0, 24.2, 0, 0.2))
        door = render.attachNewNode(wallGap)                                  # type: ignore
        door.setX(-3.4)
        door.stash()
        # door.show()
        
        # Wall
        wallNode = CollisionNode("wall")
        wallNode.addSolid(CollisionTube(0, -0.1, 0, 0, 6.3, 0, 0.2))
        wallNode.addSolid(CollisionTube(0, 8.5, 0, 0, 22, 0, 0.2))
        wallNode.addSolid(CollisionTube(0, 24.2, 0, 0, 31.4, 0, 0.2))
        wall = render.attachNewNode(wallNode)                                 # type: ignore
        wall.setX(-3.4)
        # wall.show()
        
        # Doors 4
        wallGap = CollisionNode("D4")
        wallGap.addSolid(CollisionTube(0, 6.3, 0, 0, 8.5, 0, 0.2))
        door = render.attachNewNode(wallGap)                                  # type: ignore
        door.setX(11.4)
        door.stash()
        # door.show()
        
        # Wall
        wallNode = CollisionNode("wall")
        wallNode.addSolid(CollisionTube(0, -0.1, 0, 0, 6.3, 0, 0.2))
        wallNode.addSolid(CollisionTube(0, 8.5, 0, 0, 14.8, 0, 0.2))
        wall = render.attachNewNode(wallNode)                                 # type: ignore
        wall.setX(11.4)
        # wall.show()
        
        # Doors 8
        wallGap = CollisionNode("D8")
        wallGap.addSolid(CollisionTube(0, 6.3, 0, 0, 8.5, 0, 0.2))
        door = render.attachNewNode(wallGap)                                  # type: ignore
        door.setX(29.85)
        door.stash()
        # door.show()
        
        # Wall
        wallNode = CollisionNode("wall")
        wallNode.addSolid(CollisionTube(0, -0.1, 0, 0, 6.3, 0, 0.2))
        wallNode.addSolid(CollisionTube(0, 8.5, 0, 0, 14.8, 0, 0.2))
        wall = render.attachNewNode(wallNode)                                 # type: ignore
        wall.setX(29.85)
        # wall.show()
        
        # Doors 14
        wallGap = CollisionNode("D14")
        wallGap.addSolid(CollisionTube(0, 22, 0, 0, 24.2, 0, 0.2))
        door = render.attachNewNode(wallGap)                                  # type: ignore
        door.setX(20.6)
        door.stash()
        # door.show()
        
        # Wall
        wallNode = CollisionNode("wall")
        wallNode.addSolid(CollisionTube(0, 14.8, 0, 0, 22, 0, 0.2))
        wallNode.addSolid(CollisionTube(0, 24.2, 0, 0, 31.3, 0, 0.2))
        wall = render.attachNewNode(wallNode)                                 # type: ignore
        wall.setX(20.6)
        # wall.show()
        
        # Doors 10 - 12
        wallGap = CollisionNode("D10")
        wallGap.addSolid(CollisionTube(0, 6.3, 0, 0, 8.5, 0, 0.2))
        door = render.attachNewNode(wallGap)                                  # type: ignore
        door.setX(44.7)
        door.stash()
        # door.show()
        
        wallGap = CollisionNode("D12")
        wallGap.addSolid(CollisionTube(0, 22, 0, 0, 24.2, 0, 0.2))
        door = render.attachNewNode(wallGap)                                  # type: ignore
        door.setX(44.7)
        door.stash()
        # door.show()
        
        # Wall
        wallNode = CollisionNode("wall")
        wallNode.addSolid(CollisionTube(0, -0.1, 0, 0, 6.3, 0, 0.2))
        wallNode.addSolid(CollisionTube(0, 8.5, 0, 0, 22, 0, 0.2))
        wallNode.addSolid(CollisionTube(0, 24.2, 0, 0, 31.4, 0, 0.2))
        wall = render.attachNewNode(wallNode)                                 # type: ignore
        wall.setX(44.7)
        # wall.show()
    
    def update(self):
        pX = base.pX                                                          # type: ignore
        pY = base.pY                                                          # type: ignore
        for door , cords in doors.items(): 
                if pX >= cords["x"][0] and pX <= cords["x"][1] and \
                    pY >= cords["y"][0] and pY <= cords["y"][1]:
                        doors[door]["status"] = "onDoor"
                self.updateDoor(door,pX,pY)
        self.doorCheck()
        self.gameCleared()
        if ( (-7.5 < pX < -3) or (-4.5 < pY < 0) or (46 < pX < 49) or (31 < pY < 35) )and \
            (doors["D1"]["status"] == doors["D3"]["status"] \
            == doors["D16"]["status"] == doors["D15"]["status"] \
            == doors["D13"]["status"] == doors["D12"]["status"] \
            == doors["D10"]["status"] == doors["D9"]["status"] \
            == doors["D5"]["status"] == "Closed"):
            self.message["text"] = "Stuck Outside :<"
            if self.gameCleared() is False:
                self.gameOverMethod()
        if ( (-2 < pX < 10) and (2 < pY < 13) ) and \
            (doors["D1"]["status"] == doors["D2"]["status"] \
            == doors["D3"]["status"] == doors["D4"]["status"] == "Closed"):
            self.message["text"] = "Stuck in Room-1 :'("
            if self.gameCleared() is False:
                self.gameOverMethod()
        if ( (13 < pX < 27) and (2 < pY < 13) ) and \
            (doors["D4"]["status"] == doors["D5"]["status"] \
            == doors["D6"]["status"] == doors["D7"]["status"] \
            == doors["D8"]["status"] == "Closed"):
            self.message["text"] = "Stuck in Room-2 :'<"
            if self.gameCleared() is False:
                self.gameOverMethod()
        if ( (32 < pX < 42) and (2 < pY < 13) ) and \
            (doors["D8"]["status"] == doors["D9"]["status"] \
            == doors["D10"]["status"] == doors["D11"]["status"] == "Closed"):
            self.message["text"] = "Stuck in Room-3 :("
            if self.gameCleared() is False:
                self.gameOverMethod()
        if ( (-2 < pX < 19) and (16 < pY < 29 ) ) and \
            (doors["D2"]["status"] == doors["D6"]["status"] \
            == doors["D14"]["status"] == doors["D15"]["status"] \
            == doors["D16"]["status"] == "Closed"):
            self.message["text"] = "Stuck in Room-4 :'("
            if self.gameCleared() is False:
                self.gameOverMethod()
        if ( (22 < pX < 43) and (16 < pY < 29 ) ) and \
            (doors["D7"]["status"] == doors["D11"]["status"] \
            == doors["D12"]["status"] == doors["D13"]["status"] \
            == doors["D14"]["status"] == "Closed"):
            self.message["text"] = "Stuck in Room-5 :("
            if self.gameCleared() is False:
                self.gameOverMethod()
    
    def updateDoor(self,door,pX,pY):
        if doors[door]["status"] == "onDoor":
            if not (pX >= doors[door]["x"][0] and pX <= doors[door]["x"][1] and \
                pY >= doors[door]["y"][0] and pY <= doors[door]["y"][1]):
                    doors[door]["status"] = "Closed"

            if base.keyMap["down"] is True:                                   # type: ignore
                doors[door]["status"] = "Open"
    
    def doorCheck(self):
        for d,stat in doors.items():
            temp = render.find("@@"+d)                                        # type: ignore
            curD = self.environment.find("**/"+d)
            if stat["status"] == "Closed" and temp.isStashed():
                self.doorSound.play()
                LerpPosInterval(curD, 1.5, (0,1200,0)).start()
                temp.unstash() 
                self.score += 1
    
    def gameOverMethod(self):
        self.gameOverBackdrop.show()
        self.gameOverScreen.show()    
        self.finalScoreLabel["text"] = "Doors Closed:"+str(self.score)+"/16"
        self.gameOver = True

        base.keyMap["pause"] = True                                           # type: ignore
    
    def gameCleared(self):
        clear = True
        if self.skipLevel is None:
            for c in doors.values():
                if c["status"] == "Open":  
                    return False
        if clear is True or self.skipLevel is True:
            for d,v in doors.items():
                if v["status"] == "Closed":
                    temp = render.find(d)                                        # type: ignore
                    temp.stash()
                try:
                    curD = self.environment.find("**/"+d)
                    curD.setPos(0,0,0)
                except Exception as e:
                    print(e)
                v["status"] = "Open"
                self.environment.removeNode()
                temp = render.findAllMatches("wall")                             # type: ignore
                temp.detach()
                temp = render.findAllMatches("@@*")                              # type: ignore
                temp.detach()
            self.cleared = True
            return True
    
    def cleanup(self):
        self.gameOverBackdrop.hide()
        self.gameOverScreen.hide()
        
        for d,v in doors.items():
            if v["status"] == "Closed":
                temp = render.find(d)                                        # type: ignore
                temp.stash()
            curD = self.environment.find("**/"+d)
            curD.setPos(0,0,0)
            v["status"] = "Open"
        for i in render.getChildren():                                       # type: ignore
            i.removeNode()
        for j in render.getStashedChildren():                                # type: ignore
            j.removeNode()