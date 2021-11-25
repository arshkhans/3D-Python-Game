from panda3d.core import Vec3
from direct.actor.Actor import Actor
from panda3d.core import CollisionNode, CollisionTube
from panda3d.core import BitMask32
from direct.interval.IntervalGlobal import *

FRICTION = 150.0

class GameObject():
    def __init__(self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName):
        self.actor = Actor(modelName, modelAnims)
        self.actor.reparentTo(render)                                         # type: ignore
        self.actor.setPos(pos)

        self.maxHealth = maxHealth
        self.health = maxHealth
        
        self.defaultView = "firstPerson"

        self.maxSpeed = maxSpeed

        self.velocity = Vec3(0, 0, 0)
        self.acceleration = 300.0

        self.walking = False

        colliderNode = CollisionNode(colliderName)
        colliderNode.addSolid(CollisionTube(0, -1, 0, 0, 1, 0, 0.2))
        self.collider = self.actor.attachNewNode(colliderNode)
        self.collider.show()
        self.collider.setPythonTag("owner", self)
        

    def update(self, dt):
        # If we're going faster than our maximum speed,
        # set the velocity-vector's length to that maximum
        speed = self.velocity.length()
        if speed > self.maxSpeed:
            self.velocity.normalize()
            self.velocity *= self.maxSpeed
            speed = self.maxSpeed

        # If we're walking, don't worry about friction.
        # Otherwise, use friction to slow us down.
        if not self.walking:
            frictionVal = FRICTION*dt
            if frictionVal > speed:
                self.velocity.set(0, 0, 0)
            else:
                frictionVec = -self.velocity
                frictionVec.normalize()
                frictionVec *= frictionVal

                self.velocity += frictionVec

        self.actor.setPos(self.actor, self.velocity*dt)

    def alterHealth(self, dHealth):
        self.health += dHealth

        if self.health > self.maxHealth:
            self.health = self.maxHealth

    def cleanup(self):
        if self.collider is not None and not self.collider.isEmpty():
            self.collider.clearPythonTag("owner")
            base.cTrav.removeCollider(self.collider)                          # type: ignore
            base.pusher.removeCollider(self.collider)                         # type: ignore

        if self.actor is not None:
            self.actor.cleanup()
            self.actor.removeNode()
            self.actor = None

        self.collider = None

class Player(GameObject):
    def __init__(self):
        GameObject.__init__(self,
                            Vec3(0, 0, 0),
                            "Models/PandaChan/act_p3d_chan",
                              {
                                  "stand" : "Models/PandaChan/a_p3d_chan_idle",
                                  "walk" : "Models/PandaChan/a_p3d_chan_run"
                              },
                            5,
                            10,
                            "player")
        self.actor.getChild(0).setH(180)
        
        mask = BitMask32()
        mask.setBit(1)

        self.collider.node().setFromCollideMask(mask)
        
        base.pusher.addCollider(self.collider, self.actor)                    # type: ignore
        base.cTrav.addCollider(self.collider, base.pusher)                    # type: ignore

        self.actor.loop("stand")
        
        self.sensitivityY = 2
        self.sensitivityX = 0.01
        
        self.dummyNode = render.attachNewNode("center")                       # type: ignore
        self.pp = self.actor.getPos()
        self.dummyNode.setPos(self.pp[0],self.pp[1]+1,self.pp[2]+1)
        self.dummyNode.reparentTo(self.actor)
        
        
        base.camera.reparentTo(self.actor)                                    # type: ignore
        camera.setPos(self.pp[0],self.pp[1],self.pp[2]+1)                     # type: ignore       
        camera.lookAt(self.dummyNode)                                         # type: ignore
        
    
    def getPos(self):
        return self.actor.getPos()  
    
    def getX(self):
        return self.actor.getX() 
    
    def getY(self):
        return self.actor.getY() 
    
        
    def update(self, keys, dt):
        GameObject.update(self, dt)
        if base.mouseWatcherNode.hasMouse() and self.defaultView=="firstPerson":                                  # type: ignore
            CX = int(base.win.getXSize() / 2)                                 # type: ignore
            CY = int(base.win.getYSize() / 2)                                 # type: ignore
            base.win.movePointer(0, CX, CY)                                   # type: ignore
            
            x=base.mouseWatcherNode.getMouseX()                               # type: ignore
            y=base.mouseWatcherNode.getMouseY()                               # type: ignore
            
            if x > 0:
                self.actor.setH(self.actor.getH()-self.sensitivityY)
            if x < 0:
                self.actor.setH(self.actor.getH()+self.sensitivityY)
            
            if y > 0.002 and self.dummyNode.getZ() < 2:
                self.dummyNode.detachNode()
                self.dummyNode.setZ(self.dummyNode.getZ() + self.sensitivityX)
            if y < 0 and self.dummyNode.getZ() > 0.69:                        # nice!
                self.dummyNode.detachNode()
                self.dummyNode.setZ(self.dummyNode.getZ() - self.sensitivityX)
            
            self.dummyNode.reparentTo(self.actor)
             
        self.walking = False
        if keys["up"]:
            self.walking = True
            self.velocity.addY(self.acceleration*dt)
            
        if keys["down"]:
            self.walking = True
            self.velocity.addY(-self.acceleration*dt)
            
        if keys["left"]:
            self.walking = True
            self.velocity.addX(-self.acceleration*dt)
            
        if keys["right"]:
            self.walking = True
            self.velocity.addX(self.acceleration*dt)
        
        if keys["pause"]:
            keys["pause"] = True

        if self.walking:
            standControl = self.actor.getAnimControl("stand")
            if standControl.isPlaying():
                standControl.stop()

            walkControl = self.actor.getAnimControl("walk")
            if not walkControl.isPlaying():
                self.actor.loop("walk")
        else:
            standControl = self.actor.getAnimControl("stand")
            if not standControl.isPlaying():
                self.actor.stop("walk")
                self.actor.loop("stand")
        
        camera.lookAt(self.dummyNode)                                     # type: ignore
    
    def cleanup(self):
        GameObject.cleanup(self)