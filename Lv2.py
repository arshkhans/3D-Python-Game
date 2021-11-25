from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionRay, CollisionNode, CollisionTube
from panda3d.core import BitMask32
from panda3d.core import *
from panda3d.core import CollisionHandlerQueue
from direct.interval.LerpInterval import *

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


class Lv2(ShowBase):
    def __init__(self):
        
        self.myTexture = loader.loadTexture("obj/KeyMap/Hover.jpg")           # type: ignore
        
        self.environment = loader.loadModel("obj/lv2.obj")                    # type: ignore
        self.environment.reparentTo(render)                                   # type: ignore
        
        self.environment.setPos(0, 0, 0)
        self.environment.setHpr(0,90,0)
        self.environment.setScale(0.04, 0.04, 0.04)
        
        render.setShaderAuto()                                                # type: ignore
        
        self.accept("mouse1", self.click)

        self.queue = CollisionHandlerQueue()
        
        solveCord = {}
        base.player.sensitivityY = 1                                           # type: ignore
        
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
        
        self.solve = solvable.copy()
        
        for Drow in defaultMatrix:
            for val in Drow:
                count = 0
                for Srow in self.solve:
                    if val in Srow:
                        solveCord[val] = (count,Srow.index(val))
                    count+=1
        
        count = 0
        for row in defaultMatrix:
            for val in row:
                obj = self.environment.find("**/Key"+str(val))
                if val == 0:
                    continue
                a = count
                b = row.index(val)
                i,j = solveCord[val][0],solveCord[val][1]  
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

        rayNode = CollisionNode("ray")
        self.raySolid = CollisionRay(0, 0, 0, 0, 1, 0)
        rayNode.addSolid(self.raySolid)
        self.ray = render.attachNewNode(rayNode)                              # type: ignore
        self.ray.show()

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
                except:
                    print("array bound")
    
    def movRight(self,object,i,j):
        print("Right")
        # object.setX(object.getX()+40)
        LerpPosInterval(object, 0.4, (object.getPos()+(40,0,0))).start()
        self.solve[i][j], self.solve[i][j+1] = self.solve[i][j+1], self.solve[i][j]
    
    def movLeft(self,object,i,j):
        print("Left")
        # object.setX(object.getX()-40)
        LerpPosInterval(object, 0.4, (object.getPos()+(-40,0,0))).start()
        self.solve[i][j], self.solve[i][j-1] = self.solve[i][j-1], self.solve[i][j]
    
    def movDown(self,object,i,j):
        print("Down")
        # object.setY(object.getY()-40)
        LerpPosInterval(object, 0.4, (object.getPos()+(0,-40,0))).start()
        self.solve[i][j], self.solve[i+1][j] = self.solve[i+1][j], self.solve[i][j]
    
    def movUp(self,object,i,j):
        print("Up")
        # object.setY(object.getY()+40)
        LerpPosInterval(object, 0.4, (object.getPos()+(0,40,0))).start()
        self.solve[i][j], self.solve[i-1][j] = self.solve[i-1][j], self.solve[i][j]
        
    def update(self):
        # Get the amount of time since the last update
        # if self.queue.getNumEntries() > 0:
        #     # This is so we get the closest object.
        #     self.queue.sortEntries()
        #     hover = self.queue.getEntry(0).getIntoNodePath()
        #     print(hover)
        #     hover.setTexture(self.myTexture)
            
        # if stage != hover:
            #     self.environment.clearTexture(stage)
            # stage = hover.findTextureStage(0)
            # print(stage)
            # hover = self.environment.find(hObj)
            # print(hover)
            
        # k = self.environment.find("**/Key15")
        # stage = k.findTextureStage("default")
        # print(stage)
        # if stage is not None: 
        #     k.clearTexture(stage)
        # print("update")
        
        # for entry in self.queue.entries:
        #     print(entry)

        self.ray.reparentTo(base.camera)                                        # type: ignore
        