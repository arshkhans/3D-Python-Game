from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionRay, CollisionHandlerQueue, CollisionNode
from panda3d.core import BitMask32
from panda3d.core import WindowProperties
from direct.gui.DirectGui import *
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import Vec4
import threading
import time
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib

# loadPrcFileData("", "load-file-type p3assimp")                          # type: ignore

class Lv4(ShowBase):
    def __init__(self):
        self.board = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]

        self.queen = 8
        self.clicks = 0
        self.name = "Lv4"
        self.lv = 4

        self.gameOver = None
        self.skipLevel = None
        self.cleared = None
        self.wait = None

        self.nextLevel = "None"

        self.queenImage = OnscreenImage(image='env/icons/queenImage.png', pos=(1.7, 0, -0.9),scale = 0.09)
        self.queenImage.setTransparency(TransparencyAttrib.MAlpha)

        base.cursor.setCursorHidden(False)                                             # type: ignore
        base.win.requestProperties(base.cursor)                                        # type: ignore

        self.environment = loader.loadModel("env/lv4/env.obj")                         # type: ignore
        self.environment.reparentTo(render)                                            # type: ignore

        # base.disableMouse()                                                            # type: ignore

        base.camera.reparentTo(render)                                                 # type: ignore
        base.camera.lookAt(render)                                                     # type: ignore

        base.camera.setPos(0.306829, -6.92946, 11.3305)                                # type: ignore
        base.camera.setHpr(2.09389, -52.0479, 2.04174)                                 # type: ignore

        self.environment.setPos(0, 0, 0)
        self.environment.setHpr(0,90,0)
        self.environment.setDepthOffset(1)
        self.environment.setScale(10, 10, 10)
        
        mainLight = DirectionalLight("main light")
        self.mainLightNodePath = render.attachNewNode(mainLight)                       # type: ignore
        self.mainLightNodePath.setHpr(0,-60,0)
        render.setLight(self.mainLightNodePath)                                        # type: ignore

        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))                                  # type: ignore
        self.ambientLightNodePath = render.attachNewNode(ambientLight)                 # type: ignore
        render.setLight(self.ambientLightNodePath)                                     # type: ignore

        render.setShaderAuto()                                                         # type: ignore
        
        self.queue = CollisionHandlerQueue()

        base.accept("mouse1", self.click)                                              # type: ignore

        for i in range(8):
            for j in range(8):
                k = self.environment.find("**/Chessboard_"+str(i)+str(j))
                k.node().setIntoCollideMask(BitMask32.bit(0))

        rayNode = CollisionNode("ray")
        self.raySolid = CollisionRay(0, 0, 0, 0, 1, 0)
        rayNode.addSolid(self.raySolid)
        self.ray = render.attachNewNode(rayNode)                                       # type: ignore
        self.ray.show()

        base.cTrav.addCollider(self.ray, self.queue)                          # type: ignore

        self.ray.reparentTo(base.camera)                                               # type: ignore

        # Font
        self.font = loader.loadFont("Fonts/Wbxkomik.ttf")                              # type: ignore

        self.error = OnscreenText(text="Can't place here!",
                            pos=(0, -0.95),
                            scale = 0.1)
        self.error.hide()

        self.clickInfo = OnscreenText(text="",
                            pos=(1.85, 0.9),
                            font = self.font,
                            scale = 0.1)

        self.queenCount = OnscreenText(text="",
                            pos=(1.85, -0.95),
                            font = self.font,
                            scale = 0.11)

        print(render.ls())# type: ignore
        base.hint["text"] = 'Hint: Place eight queens on the chessboard\nsuch that none of them attack one another.' # type: ignore
    
    def click(self):
        if self.queue.getNumEntries() > 0 and base.keyMap["pause"] is False:          # type: ignore
            print("inside")
            self.queue.sortEntries()
            click = self.queue.getEntry(0).getIntoNodePath()
            print(click)
            self.setQueen(int(click.getName()[-2:-1]),int(click.getName()[-1:]))
    
    def setQueen(self, a, b):
        self.clicks += 1
        self.clickInfo.setText(str(self.clicks))
        if self.board[a][b] != 1:
            self.queen -= 1
            self.queenCount.setText("x"+str(self.queen))
            k = self.environment.find("**/Queen_"+str(a)+str(b))
            k.setY(0.48)

            incA = decA = a
            incB = decB = b
            while not (incA < 0 or incA > 7 or incB < 0 or incB > 7):
                self.board[incA][incB] = 1
                incA += 1
                incB += 1
            while not (decA < 0 or decA > 7 or decB < 0 or decB > 7):
                self.board[decA][decB] = 1
                decA -= 1
                decB -= 1

            tempA = a
            tempB = b
            while not (tempA < 0 or tempA > 7 or tempB < 0 or tempB > 7):
                self.board[tempA][tempB] = 1
                tempA = tempA + 1
                tempB = tempB - 1

            tempA = a
            tempB = b
            while not (tempA < 0 or tempA > 7 or tempB < 0 or tempB > 7):
                self.board[tempA][tempB] = 1
                tempA = tempA - 1
                tempB = tempB + 1
            for i in range(8):
                for j in range(8):
                    if i == a or j == b:
                        self.board[i][j] = 1

        else:
            txt = "Can't Place Here!"
            botMessage = threading.Thread(target = self.showMessageBottom, args=(txt,))
            botMessage.start()
    
    def showMessageBottom(self,text):
        self.error["text"] = text
        self.error.show()
        time.sleep(1)
        self.error.hide()

    def update(self):
        if base.mouseWatcherNode.hasMouse():                                           # type: ignore
            mpos = base.mouseWatcherNode.getMouse()                                    # type: ignore
            self.raySolid.setFromLens(base.camNode, mpos.getX(), mpos.getY())          # type: ignore 
        if self.queen == 0:
            self.cleared = True
            base.gameClearedScreen.show()                                              # type: ignore
            base.gameBackdrop.show()                                                   # type: ignore
            self.queenImage.hide()
        if self.clicks == 10 and self.cleared is None:
            base.gameOverScreen.show()                                                 # type: ignore
            base.gameBackdrop.show()                                                   # type: ignore
            self.queenImage.hide()
    
    def cleanup(self):
        base.gameClearedScreen.hide()                                                  # type: ignore
        base.gameBackdrop.hide()                                                       # type: ignore
        base.gameOverScreen.hide()                                                     # type: ignore
        self.queenImage.show()

        self.board = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]
        self.queen = 8
        self.clicks = 0

        self.clickInfo.destroy()
        self.queenCount.destroy()
        for i in range(8):
            for j in range(8):
                k = self.environment.find("**/Queen_"+str(i)+str(j))
                k.setPos(0,0,0)