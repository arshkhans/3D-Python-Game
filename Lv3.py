from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import TransparencyAttrib
from panda3d.core import Vec4
from panda3d.core import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
import random

loadPrcFileData("", "load-file-type p3assimp")                          # type: ignore

import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

class Lv3():
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.environment = loader.loadModel("env/lv3/lv3.obj")                             # type: ignore
        self.environment.reparentTo(render)                                                # type: ignore
        self.environment.setPos(0, 0, 0)
        self.environment.setHpr(0,90,0)

        base.camera.reparentTo(render)                                                     # type: ignore
        base.camera.lookAt(render)                                                         # type: ignore
        base.camera.setPos(198.317, 15.7636, 63.2784)                                      # type: ignore
        base.camera.setHpr(93.3851, -14.9913, -1.03374)                                    # type: ignore

        base.player.actor.setPos(150,0,27.5)                                               # type: ignore
        base.player.actor.setScale(2)                                                      # type: ignore

        base.disableMouse()                                                                # type: ignore

        self.name = "Lv3"
        self.lv = 3

        base.cursor.setCursorHidden(False)                                                 # type: ignore
        base.win.requestProperties(base.cursor)                                            # type: ignore

        self.gameOver = None
        self.skipLevel = None
        self.cleared = None
        self.wait = None
        self.nextLevel = "Lv4"

        self.score = 0
        self.maxScore = 3

        self.gameStaus = None

        self.options = ['rock','paper','scissor']

        self.playerChoice = ""
        self.cpuChoice = ""

        render.setShaderAuto()                                                         # type: ignore

        # Hint 
        base.hint["text"] = "Hint: Win three rounds to clear"                          # type: ignore

        self.startBtn = DirectButton(text = "",
                    command = self.start,
                    pos = (0, 0, 0),
                    image = "env/lv3/UI/start.png",
                    image_scale = (0.7,0,0.6),
                    relief = None
                    )
        self.startBtn.setTransparency(TransparencyAttrib.MAlpha)
        # self.startBtn.hide()

        self.restartBtn = DirectButton(text = "",
                    command = self.start,
                    pos = (0, 0, 0),
                    image = "env/lv3/UI/restart.png",
                    image_scale = (0.7,0,0.6),
                    relief = None
                    )
        
        self.restartBtn.setTransparency(TransparencyAttrib.MAlpha)
        self.restartBtn.hide()

        self.three = loader.loadModel('env/lv3/UI/3.obj')   #type: ignore
        self.three.reparentTo(aspect2d)    #type: ignore
        self.three.setHpr(0,90,0)
        self.three.setTransparency(TransparencyAttrib.MAlpha)
        self.three.hide()
        self.fadeInThree = self.three.colorScaleInterval( 0.5,Vec4(1,1,1,1),Vec4(1,1,1,0) )
        self.fadeOutThree = self.three.colorScaleInterval( 0.5,Vec4(1,1,1,0) )

        self.two = loader.loadModel('env/lv3/UI/2.obj')   #type: ignore
        self.two.reparentTo(aspect2d)    #type: ignore
        self.two.setHpr(0,90,0)
        self.two.setTransparency(TransparencyAttrib.MAlpha)
        self.two.hide()
        self.fadeInTwo = self.two.colorScaleInterval( 0.5,Vec4(1,1,1,1),Vec4(1,1,1,0) )
        self.fadeOutTwo = self.two.colorScaleInterval( 0.5,Vec4(1,1,1,0) )

        self.one = loader.loadModel('env/lv3/UI/1.obj')   #type: ignore
        self.one.reparentTo(aspect2d)    #type: ignore
        self.one.setHpr(0,90,0)
        self.one.setTransparency(TransparencyAttrib.MAlpha)
        self.one.hide()
        self.fadeInOne = self.one.colorScaleInterval( 0.5,Vec4(1,1,1,1),Vec4(1,1,1,0) )
        self.fadeOutOne = self.one.colorScaleInterval( 0.5,Vec4(1,1,1,0) )

        self.menuBorder = OnscreenImage(image='env/lv3/UI/menu.png', 
                                            parent = render2d) # type: ignore  # 2d-pos(x,z,y) (1.7, 0, -0.9)
        self.menuBorder.setTransparency(TransparencyAttrib.MAlpha)
        self.menuBorder.hide()

        self.cpuOption = OnscreenImage(image='env/lv3/UI/rock.png', 
                                            pos=(-0.7, 0, 0),
                                            scale = (0.12,0,0.2),
                                            parent = render2d) # type: ignore  # 2d-pos(x,z,y) (1.7, 0, -0.9)
        self.cpuOption.setTransparency(TransparencyAttrib.MAlpha)
        self.cpuOption.hide()

        self.playerOption = OnscreenImage(image='env/lv3/UI/rock.png', 
                                            pos=(0.7, 0, 0),
                                            scale = (0.12,0,0.2),
                                            parent = render2d) # type: ignore  # 2d-pos(x,z,y) (1.7, 0, -0.9)
        self.playerOption.setTransparency(TransparencyAttrib.MAlpha)
        self.playerOption.hide()

        # Top Score
        self.scoreShow = OnscreenText(text="",
                            pos=(0, 0.92),
                            scale = 0.06,
                            parent = render2d) # type: ignore
        self.scoreShow.show()

        self.hands = mp_hands.Hands(
                    max_num_hands=1,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) 
        
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
    
    def start(self):
        self.startBtn.hide()
        self.cpuOption.hide()
        self.playerOption.hide()
        self.restartBtn.hide()
        
        self.countdown = Sequence(
            # 3
            Func(self.three.show), 
            self.fadeInThree,
            # Func(sound.play), 
            # Wait(sound.length()), # wait until sound finishes
            Wait(0.1),
            self.fadeOutThree,
            # 2
            Func(self.two.show), 
            self.fadeInTwo,
            # Func(sound.play), 
            # Wait(sound.length()), # wait until sound finishes
            Wait(0.1),
            self.fadeOutTwo,
            # 1
            Func(self.one.show), 
            self.fadeInOne,
            # Func(sound.play), 
            # Wait(sound.length()), # wait until sound finishes
            Wait(0.1),
            self.fadeOutOne,
        )
        self.gameStaus = "Playing"
        self.countdown.start()
        self.menuBorder.show()
    
    def reset(self):
        self.gameStaus = None
        self.restartBtn.show()
    
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
    
    def update(self):
        if self.gameStaus is not None:
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
            else:
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = self.hands.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        if (hand_landmarks.landmark[8].y > hand_landmarks.landmark[5].y)\
                        and (hand_landmarks.landmark[12].y > hand_landmarks.landmark[9].y)\
                        and (hand_landmarks.landmark[16].y > hand_landmarks.landmark[13].y)\
                        and (hand_landmarks.landmark[20].y > hand_landmarks.landmark[17].y):
                            self.playerChoice = "rock"
                        elif (hand_landmarks.landmark[8].y < hand_landmarks.landmark[5].y)\
                        and (hand_landmarks.landmark[12].y < hand_landmarks.landmark[9].y)\
                        and (hand_landmarks.landmark[16].y > hand_landmarks.landmark[13].y)\
                        and (hand_landmarks.landmark[20].y > hand_landmarks.landmark[17].y):
                            self.playerChoice = "scissor"
                        elif (hand_landmarks.landmark[8].y < hand_landmarks.landmark[5].y)\
                        and (hand_landmarks.landmark[12].y < hand_landmarks.landmark[9].y)\
                        and (hand_landmarks.landmark[16].y < hand_landmarks.landmark[13].y)\
                        and (hand_landmarks.landmark[20].y < hand_landmarks.landmark[17].y):
                            self.playerChoice = "paper"
                        else:
                            self.playerChoice = "Error"
                else:
                    self.playerChoice = "Error"
            if not self.countdown.isPlaying():
                self.cpuChoice = random.choice(self.options)
                self.cpuOption['image'] = f'env/lv3/UI/{self.cpuChoice}.png'
                self.cpuOption.setTransparency(TransparencyAttrib.MAlpha)
                self.cpuOption.show()
                if self.playerChoice != "Error":
                    self.playerOption['image'] = f'env/lv3/UI/{self.playerChoice}.png'
                    self.playerOption.setTransparency(TransparencyAttrib.MAlpha)
                    self.playerOption.show()
                    if self.playerChoice == "paper" and self.cpuChoice == "rock":
                        self.score = self.score + 1
                        self.scoreShow["text"] = str(self.score) +"/"+ str(self.maxScore)
                    elif self.playerChoice == "rock" and self.cpuChoice == "scissor":
                        self.score = self.score + 1
                        self.scoreShow["text"] = str(self.score) +"/"+ str(self.maxScore)
                    elif self.playerChoice == "scissor" and self.cpuChoice == "paper":
                        self.score = self.score + 1
                        self.scoreShow["text"] = str(self.score) +"/"+ str(self.maxScore)
                if self.score != self.maxScore:
                    self.reset()
                else:
                    self.cleared = True
                    self.cleanup()
            
        if self.skipLevel is True:
            self.cleared = True
            self.cleanup()
    
    def cleanup(self):
        self.scoreShow.hide()
        self.startBtn.hide()
        self.cpuOption.hide()
        self.playerOption.hide()
        self.restartBtn.hide()
        self.environment.removeNode()
        img = render2d.find_all_matches("**/OnscreenImage")                    # type: ignore
        for i in img:
            i.removeNode()
        for i in render.getChildren():                                       # type: ignore
            i.removeNode()
        self.cap.release()