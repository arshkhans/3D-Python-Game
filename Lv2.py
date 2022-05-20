from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionRay, CollisionNode, CollisionTube
from panda3d.core import BitMask32
from panda3d.core import *
from panda3d.core import CollisionHandlerQueue
from direct.interval.LerpInterval import *
from direct.gui.DirectGui import *
import copy
from panda3d.core import TransparencyAttrib

loadPrcFileData("", "load-file-type p3assimp")                                 # type: ignore

defaultMatrix = [
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12],
    [13,14,15,0]
]

solvable = [
    [1,4,8,0],
    [3,7,9,2],
    [10,6,11,12],
    [14,5,13,15]
]

unSolvable = [
    [
        [3,9,1,15],
        [14,11,4,6],
        [13,0,10,12],
        [2,7,8,5]
    ],
    [
        [1,2,3,4],
        [5,6,7,8],
        [9,10,11,12],
        [13,15,14,0]
    ]
    
]

testing = [
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12],
    [13,14,0,15]
]


class Lv2(ShowBase):
    def __init__(self):
        
        self.myTexture = loader.loadTexture("env/lv2/KeyMap/Hover.jpg")           # type: ignore
        
        self.environment = loader.loadModel("env/lv2/lv2.obj")                    # type: ignore
        self.environment.reparentTo(render)                                       # type: ignore

        self.environment.setTransparency(TransparencyAttrib.MAlpha)
        
        self.environment.setPos(0, 0, 0)
        self.environment.setHpr(0,90,0)
        self.environment.setScale(0.04, 0.04, 0.04)
        
        render.setShaderAuto()                                               # type: ignore
        base.crossHair.show()                                                 # type: ignore

        self.name = "Lv2"
        self.lv = 2

        self.gameOver = None
        self.skipLevel = None
        self.cleared = None
        self.wait = None

        self.nextLevel = "Lv3"

        self.accept("mouse1", self.click)

        self.queue = CollisionHandlerQueue()

        self.slideSound = loader.loadSfx("audios/stoneSlide.ogg")         # type: ignore
        self.slideSound.setLoop(False)
        self.slideSound.setVolume(1) # 0.05 (0-1)

        # Hint
        base.hint["text"] = "Arraange the numbers in Ascending order."    # type: ignore
        
        # self.solve = copy.deepcopy(unSolvable[0])
        # self.solve = copy.deepcopy(solvable)
        self.solve = copy.deepcopy(testing)
        self.solveCord = {}

        for Drow in defaultMatrix:
            for val in Drow:
                count = 0
                for Srow in self.solve:
                    if val in Srow:
                        self.solveCord[val] = (count,Srow.index(val))
                    count+=1
        
        count = 0
        for row in defaultMatrix:
            for val in row:
                obj = self.environment.find("**/Key"+str(val))
                if val == 0:
                    continue
                a = count
                b = row.index(val)
                i,j = self.solveCord[val][0],self.solveCord[val][1]  
                if i > a:
                    diff = i-a
                    obj.setY(obj.getY()-(40*diff))
                if i < a:
                    diff = a-i
                    obj.setY(obj.getY()+(40*diff))
                if j > b:
                    diff = j-b
                    obj.setX(obj.getX()+(40*diff))
                if j < b:
                    diff = b-j
                    obj.setX(obj.getX()-(40*diff))
            count += 1

        # base.player.sensitivityY = 1                                          # type: ignore
        
        wallSolid = CollisionTube(-9.0, 0, 0, 50.3, 0, 0, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)                                 # type: ignore
        wall.setY(-20)
        wall.show()
        
        for i in range(1,16):
            k = self.environment.find("**/Key"+str(i)) 
            k.node().setIntoCollideMask(BitMask32.bit(0))
            k.setTag('Key',str(i).encode())

        rayNode = CollisionNode("ray")
        self.raySolid = CollisionRay(0, 0, 0, 0, 1, 0)
        rayNode.addSolid(self.raySolid)
        self.ray = render.attachNewNode(rayNode)                              # type: ignore
        self.ray.show()
    
        self.numbers = render.findAllMatches("**/Key*")                       # type: ignore

        base.cTrav.addCollider(self.ray, self.queue)                          # type: ignore
    
    def click(self):
        if self.queue.getNumEntries() > 0:
            # This is so we get the closest object.
            self.queue.sortEntries()
            click = self.queue.getEntry(0).getIntoNodePath()
            if click.hasTag("Key"):
                val = click.getTag("Key")
                val = int(val)
                count = 0
                for row in self.solve:
                    if val in row:   
                        i,j = count,row.index(val)
                    count += 1
                try:
                    if (j+1) <= 3 and self.solve[i][j+1] == 0:
                        self.movRight(click,i,j)
                    elif (j-1) >= 0 and self.solve[i][j-1] == 0:
                        self.movLeft(click,i,j)
                    elif (i+1) <= 3 and self.solve[i+1][j] == 0:
                        self.movDown(click,i,j)
                    elif (i-1) >= 0 and self.solve[i-1][j] == 0:
                        self.movUp(click,i,j)
                except Exception as e:
                    print(e)
    
    def movRight(self,object,i,j):
        LerpPosInterval(object, 0.4, (object.getPos()+(40,0,0))).start()
        self.solve[i][j], self.solve[i][j+1] = self.solve[i][j+1], self.solve[i][j]
        self.slideSound.play()
    
    def movLeft(self,object,i,j):
        LerpPosInterval(object, 0.4, (object.getPos()+(-40,0,0))).start()
        self.solve[i][j], self.solve[i][j-1] = self.solve[i][j-1], self.solve[i][j]
        self.slideSound.play()
    
    def movDown(self,object,i,j):
        LerpPosInterval(object, 0.4, (object.getPos()+(0,-40,0))).start()
        self.solve[i][j], self.solve[i+1][j] = self.solve[i+1][j], self.solve[i][j]
        self.slideSound.play()
    
    def movUp(self,object,i,j):
        LerpPosInterval(object, 0.4, (object.getPos()+(0,40,0))).start()
        self.solve[i][j], self.solve[i-1][j] = self.solve[i-1][j], self.solve[i][j]
        self.slideSound.play()
        
    def update(self):
        if self.queue.getNumEntries() > 0:
            self.queue.sortEntries()
            hover = self.queue.getEntry(0).getIntoNodePath()
            for i in self.numbers:
                if hover == i:
                    continue
                i.clearTexture()
            hover.setTexture(self.myTexture)
        
        if self.solve == defaultMatrix:
            base.saveData.changeLevelStatus(self.lv,"Cleared")              # type: ignore
            self.cleared = True
        self.ray.reparentTo(base.camera)                                    # type: ignore

    def cleanup(self):
        self.environment.removeNode()
        for i in render.getChildren():                                      # type: ignore
            i.removeNode()
