from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from GameObject import *
from Lv1 import *
from Lv2 import *
from Lv3 import *
from Lv4 import *

# loadPrcFileData("", "load-file-type p3assimp")                              # type: ignore
# w, h = 1366, 768
# loadPrcFileData('', 'win-size %i %i' % (w, h))                              # type: ignore
# loadPrcFileData("", "fullscreen true")                                      # type: ignore 

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

        self.pX = None
        self.pY = None
        
        self.disableAllAudio()                                                # type: ignore
        
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
        
        self.sound = None
        
        self.loadingSound = loader.loadSfx("Sounds/loading.ogg")         # type: ignore
        self.loadingSound.setLoop(True)
        self.loadingSound.setVolume(0.05) # 0.05
        self.loadingSound.play()

        # Font
        self.font = loader.loadFont("Fonts/Wbxkomik.ttf")                     # type: ignore

        self.buttonImages = (
            loader.loadTexture("Models/Misc/UI/UIButton.jpg"),                # type: ignore
            loader.loadTexture("Models/Misc/UI/UIButtonPressed.jpg"),         # type: ignore
            loader.loadTexture("Models/Misc/UI/UIButtonHighlighted.jpg"),     # type: ignore
            loader.loadTexture("Models/Misc/UI/UIButtonDisabled.png")         # type: ignore
        )
        
        # Title Screen
        self.titleMenuBackdrop = DirectFrame(frameColor = (0, 0, 0, 1),
                                             frameSize = (-1, 1, -1, 1),
                                             parent = render2d)               # type: ignore
        
        self.titleMenu = DirectFrame(frameColor = (1, 1, 1, 0))
        
        self.gameBackdrop = DirectFrame(frameColor = (0, 0, 0, 1),
                                             frameSize = (-1, 1, -1, 1),
                                             parent = render2d)               # type: ignore
        self.gameBackdrop.hide()
        
        self.gameClearedScreen = DirectFrame(frameColor = (1, 1, 1, 0))
        self.gameClearedScreen.hide()

        level1 = DirectLabel(text = "Cleared",
                            scale = 0.1,
                            pos = (0, 0, 0.4),
                            parent = self.gameClearedScreen,
                            relief = None,
                            text_font = self.font,                            # type: ignore
                            text_fg = (1, 1, 1, 1))
        
        # Game Over Screen
        self.gameOverScreen = DirectFrame(frameColor = (1, 1, 1, 0))
        self.gameOverScreen.hide()

        level1 = DirectLabel(text = "Game Over",
                            scale = 0.1,
                            pos = (0, 0, 0.4),
                            parent = self.gameOverScreen,
                            relief = None,
                            text_font = self.font,                            # type: ignore
                            text_fg = (1, 1, 1, 1))
        
        btn = DirectButton(text = "Quit",
                           command = self.quit,
                           pos = (-0.3, 0, 0.1),
                           parent = self.gameOverScreen,
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
                           parent = self.gameOverScreen,
                           scale = 0.07,
                           text_font = self.font,
                           clickSound = loader.loadSfx("Sounds/UIClick.ogg"), # type: ignore
                           frameTexture = self.buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)
        
        title = DirectLabel(text = "The",
                            scale = 0.08,
                            pos = (0, 0, 0.9),
                            parent = self.titleMenu,
                            relief = None,
                            text_font = self.font,
                            text_fg = (1, 1, 1, 1),)
        title3 = DirectLabel(text = "Game",
                             scale = 0.13,
                             pos = (0, 0, 0.75),
                             parent = self.titleMenu,
                            #  relief = None,
                             text_font = self.font,
                             text_fg = (27/ 255.0, 27/ 255.0, 27/ 255.0, 1),
                             frameColor = (255/ 255.0, 163/ 255.0, 26/ 255.0, 1))
        
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

        btn = DirectCheckButton(command = self.mute,
                                pos = (1.93, 0, -0.91),
                                parent = self.titleMenu,
                                scale = 0.07,
                                text_font = self.font,
                                clickSound = loader.loadSfx("Sounds/UIClick.ogg"), # type: ignore
                                boxImage = ("Models/icons/unmuteT.png", "Models/icons/muteT.png", None),
                                relief = DGG.FLAT,)
        btn.setTransparency(True)
        
        # Pause Menu
        self.pauseGame = DirectDialog(frameSize = (-0.7, 0.7, -0.7, 0.7),
                                           fadeScreen = 0.4,
                                           relief = DGG.FLAT,
                                           frameTexture = "Models/Misc/UI/stoneFrame.jpg")
        self.pauseGame.hide()

        self.hint = OnscreenText(text="", 
                            pos=(0, -0.85),
                            parent = self.pauseGame,
                            scale = 0.1)
        
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
      
        btn = DirectButton(text = "Skip",
                           command = self.skipLevel,
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
        
        btn = DirectCheckButton(command = self.mute,
                                pos = (-0.5, 0, -0.6),
                                parent = self.pauseGame,
                                scale = 0.07,
                                text_font = self.font,
                                clickSound = loader.loadSfx("Sounds/UIClick.ogg"), # type: ignore
                                boxImage = ("Models/icons/unmuteT.png", "Models/icons/muteT.png", None),
                                relief = DGG.FLAT,)
        btn.setTransparency(True)

        self.currentLevel = None
    
        self.updateTask = taskMgr.add(self.update, "update")                  # type: ignore
    
    def mute(self,status):
        if status:
            self.sound = "Muted"
            base.disableAllAudio()                                            # type: ignore
        else:
            self.sound = None
            base.enableAllAudio()                                             # type: ignore
    
    def skipLevel(self):
        if self.currentLevel:
            self.resumeGame()
            self.currentLevel.skipLevel = True
       
    def startGame(self):
        self.titleMenu.hide()
        self.titleMenuBackdrop.hide()
        self.pauseGame.hide()

        self.loadingSound.stop()
        
        self.keyMap["pause"] = False
        
        self.cursor.setCursorHidden(True)
        self.win.requestProperties(self.cursor)

        self.cleanup()
        if self.player is None:
            self.player = Player() 
        if self.currentLevel is None or self.currentLevel.name == "Lv1":
            self.currentLevel = Lv1()
        elif self.currentLevel.name == "Lv2":
            self.currentLevel = None
            self.currentLevel = Lv2()
        elif self.currentLevel.name == "Lv3":
            self.currentLevel = None
            self.currentLevel = Lv3()
        elif self.currentLevel.name == "Lv4":
            self.currentLevel = Lv4()


    def resumeGame(self):
        self.keyMap["pause"] = False
        if self.currentLevel.name != "Lv4":
            self.cursor.setCursorHidden(True)
            self.win.requestProperties(self.cursor)
        self.pauseGame.hide()
                       
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def update(self, task):
        dt = globalClock.getDt()                                              # type: ignore
        if self.player is None and self.currentLevel:
            if self.currentLevel.name == "Lv4":
                self.currentLevel.update()
        if self.player is not None and self.keyMap["pause"] is False:
            self.pX = float("{:.2f}".format(self.player.getX()))
            self.pY = float("{:.2f}".format(self.player.getY()))
            if self.currentLevel.name != "Lv4":
                self.player.update(self.keyMap, dt)
            if self.currentLevel is not None:
                self.currentLevel.update()
                # Check and run once
                if self.currentLevel.cleared is True:
                    print("cHANING levels")
                    if self.currentLevel.nextLevel == "Lv2":
                        self.currentLevel = Lv2()
                    elif self.currentLevel.nextLevel == "Lv3":
                        self.currentLevel = Lv3()
                        self.startGame()
                    elif self.currentLevel.nextLevel == "Lv4":
                        self.currentLevel = Lv4()
                        self.startGame()
        if self.keyMap["pause"] is True:
            if self.currentLevel is not None and self.currentLevel.gameOver is None:
                self.pauseGame.show()
            self.cursor.setCursorHidden(False)
            self.win.requestProperties(self.cursor)
        
        return task.cont
    
    def cleanup(self):
        if self.player is not None:
            self.currentLevel.cleanup()
            self.player.cleanup()
            self.player = None
            
    def quit(self):
        base.userExit()                                                      # type: ignore

game = Game()
game.run()