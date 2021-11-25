from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import LineSegs
from direct.gui.DirectGui import *
from panda3d.core import *
from GameObject import *
from Lv1 import *


loadPrcFileData("", "load-file-type p3assimp")                          # type: ignore

# w, h = 1366, 768
# loadPrcFileData('', 'win-size %i %i' % (w, h))                        # type: ignore
# loadPrcFileData("", "fullscreen true")                                # type: ignore 

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()
        render.setShaderAuto()                                                # type: ignore
        
        properties = WindowProperties()
        properties.setSize(1000, 650)
        self.win.requestProperties(properties)
        
        self.cursor = WindowProperties()
        self.cursor.setCursorHidden(False)
        self.win.requestProperties(self.cursor)
        
        
        self.keyMap = {
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False,
            "pause" : False
        }
        
        # Using Keys
        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.accept("escape", self.updateKeyMap,["pause", True] )
        
        self.pusher = CollisionHandlerPusher()
        self.cTrav = CollisionTraverser()
        
        self.pusher.setHorizontal(True)
        
        self.player = None
        self.lv1 = None
        
        self.sound = None
        
        self.loadingSound = base.loader.loadSfx("Sounds/loading.ogg")         # type: ignore
        self.loadingSound.setLoop(True)
        self.loadingSound.setVolume(0.05) # 0.05
        self.loadingSound.play()
        
        # Title Screen
        self.titleMenuBackdrop = DirectFrame(frameColor = (0, 0, 0, 1),
                                             frameSize = (-1, 1, -1, 1),
                                             parent = render2d)               # type: ignore
        
        self.titleMenu = DirectFrame(frameColor = (1, 1, 1, 0))
        
        # Font
        self.font = loader.loadFont("Fonts/Wbxkomik.ttf")                     # type: ignore
        
        self.buttonImages = (
            loader.loadTexture("Models/Misc/UI/UIButton.jpg"),                # type: ignore
            loader.loadTexture("Models/Misc/UI/UIButtonPressed.jpg"),         # type: ignore
            loader.loadTexture("Models/Misc/UI/UIButtonHighlighted.jpg"),     # type: ignore
            loader.loadTexture("Models/Misc/UI/UIButtonDisabled.png")         # type: ignore
        )
        
        title = DirectLabel(text = "Aastha",
                            scale = 0.1,
                            pos = (0, 0, 0.9),
                            parent = self.titleMenu,
                            relief = None,
                            text_font = self.font,
                            text_fg = (1, 1, 1, 1))
        title2 = DirectLabel(text = "and her",
                             scale = 0.07,
                             pos = (0, 0, 0.79),
                             parent = self.titleMenu,
                             text_font = self.font,
                             frameColor = (0.5, 0.5, 0.5, 1))
        title3 = DirectLabel(text = "Insatiable Hunger",
                             scale = 0.125,
                             pos = (0, 0, 0.65),
                             parent = self.titleMenu,
                             relief = None,
                             text_font = self.font,
                             text_fg = (1, 1, 1, 1))
        
        btn = DirectButton(text = "Start Game",
                           command = self.startGame,
                           pos = (0, 0, 0.2),
                           parent = self.titleMenu,
                           scale = 0.1,
                           text_font = self.font,
                           clickSound = loader.loadSfx("Sounds/UIClick.ogg"), # type: ignore
                           frameTexture = self.buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text = "Quit",
                           command = self.quit,
                           pos = (0, 0, -0.2),
                           parent = self.titleMenu,
                           scale = 0.1,
                           text_font = self.font,
                           clickSound = loader.loadSfx("Sounds/UIClick.ogg"), # type: ignore
                           frameTexture = self.buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)
        
        # Pause Menu
        self.pauseGame = DirectDialog(frameSize = (-0.7, 0.7, -0.7, 0.7),
                                           fadeScreen = 0.4,
                                           relief = DGG.FLAT,
                                           frameTexture = "Models/Misc/UI/stoneFrame.jpg")
        self.pauseGame.hide()
        
        label = DirectLabel(text = "Pause!",
                            parent = self.pauseGame,
                            scale = 0.1,
                            pos = (0, 0, 0.4),
                            text_font = self.font,
                            relief = None)
        
        btn = DirectButton(text = "Resume",
                           command = self.resumeGame,
                           pos = (-0.3, 0, 0.1),
                           parent = self.pauseGame,
                           scale = 0.07,
                           text_font = self.font,
                           clickSound = loader.loadSfx("Sounds/UIClick.ogg"), # type: ignore
                           frameTexture = self.buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)
        
        btn = DirectButton(text = "Restart",
                           command = self.startGame,
                           pos = (0.3, 0, 0.1),
                           parent = self.pauseGame,
                           scale = 0.07,
                           text_font = self.font,
                           clickSound = loader.loadSfx("Sounds/UIClick.ogg"), # type: ignore
                           frameTexture = self.buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text = "Quit",
                           command = self.quit,
                           pos = (0.3, 0, -0.1),
                           parent = self.pauseGame,
                           scale = 0.07,
                           text_font = self.font,
                           clickSound = loader.loadSfx("Sounds/UIClick.ogg"), # type: ignore
                           frameTexture = self.buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)
      
        btn = DirectButton(text = "View",
                           command = self.changeView,
                           pos = (-0.3, 0, -0.1),
                           parent = self.pauseGame,
                           scale = 0.07,
                           text_font = self.font,
                           clickSound = loader.loadSfx("Sounds/UIClick.ogg"), # type: ignore
                           frameTexture = self.buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)
        
        btn = DirectCheckButton(command = self.mute,
                                pos = (-0.5, 0, -0.6),
                                parent = self.pauseGame,
                                scale = 0.07,
                                text_font = self.font,
                                clickSound = loader.loadSfx("Sounds/UIClick.ogg"), # type: ignore
                                boxImage = ("Models/icons/unmuteT.png", "Models/icons/muteT.png", None),
                                relief = DGG.FLAT,)
        btn.setTransparency(True)
    
        self.updateTask = taskMgr.add(self.update, "update")                  # type: ignore
    
    def mute(self,status):
        if status:
            self.sound = "Muted"
            base.disableAllAudio()                                            # type: ignore
        else:
            self.sound = None
    
    def changeView(self):
        if self.player.defaultView == "firstPerson":
            self.enableMouse()                                                # type: ignore
            self.player.defaultView = "moding"
        else:
            self.player.defaultView = "firstPerson"
            self.pp = self.player.getPos()
            self.player.dummyNode.setPos(self.pp[0],self.pp[1]+1,self.pp[2]+1)
            self.player.dummyNode.reparentTo(self.player.actor)
            
            camera.reparentTo(self.player.actor)                         # type: ignore
            camera.setPos(self.pp[0],self.pp[1],self.pp[2]+1)                 # type: ignore
            camera.lookAt(self.player.dummyNode)                              # type: ignore
            self.disableMouse()
       
    def startGame(self):
        self.titleMenu.hide()
        self.titleMenuBackdrop.hide()
        self.pauseGame.hide()
        
        self.loadingSound.stop()
        
        self.keyMap["pause"] = False
        
        self.cursor.setCursorHidden(True)
        self.win.requestProperties(self.cursor)

        self.cleanup()

        self.player = Player() 
        self.lv1 = Lv1()
        self.lv1.gg = None

        self.player.actor.setPos(0,-3,0)

    def resumeGame(self):
        self.keyMap["pause"] = False
        self.cursor.setCursorHidden(True)
        self.win.requestProperties(self.cursor)
        self.pauseGame.hide()
                       
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def update(self, task):
        dt = globalClock.getDt()                                              # type: ignore
        if self.player is not None and self.keyMap["pause"] is False:
            pX = float("{:.2f}".format(self.player.getX()))
            pY = float("{:.2f}".format(self.player.getY()))
            self.player.update(self.keyMap, dt)
            if self.lv1 is not None:
                self.lv1.update(pX,pY)
        if self.keyMap["pause"] is True:
            if self.lv1 is not None and self.lv1.gg is None:
                self.pauseGame.show()
            self.cursor.setCursorHidden(False)
            self.win.requestProperties(self.cursor)
        return task.cont
    
    def cleanup(self):
        if self.player is not None:
            self.lv1.cleanup()
            self.player.cleanup()
            self.player = None    
            
    def quit(self):
        base.userExit()                                                      # type: ignore

game = Game()
game.run()