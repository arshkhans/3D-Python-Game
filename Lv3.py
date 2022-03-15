from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionTube, CollisionNode
from panda3d.core import Vec4, Vec3
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import *

loadPrcFileData("", "load-file-type p3assimp")                          # type: ignore

import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

class Lv3():
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.environment = loader.loadModel("env/lv3/lv3.obj")                                 # type: ignore
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

        self.gameOver = None
        self.skipLevel = None
        self.cleared = None
        self.wait = None
        self.nextLevel = "Lv4"

        render.setShaderAuto()                                                             # type: ignore
        
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
    
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
    
    def update(self):
        if self.skipLevel is None:
            with mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
                success, image = self.cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                else:
                    # If loading a video, use 'break' instead of 'continue'.
                    # To improve performance, optionally mark the image as not writeable to
                    # pass by reference.
                    image.flags.writeable = False
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    results = hands.process(image)

                    # Draw the hand annotations on the image.
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            if (hand_landmarks.landmark[8].y > hand_landmarks.landmark[5].y)\
                            and (hand_landmarks.landmark[12].y > hand_landmarks.landmark[9].y)\
                            and (hand_landmarks.landmark[16].y > hand_landmarks.landmark[13].y)\
                            and (hand_landmarks.landmark[20].y > hand_landmarks.landmark[17].y):
                                print("Rock")
                            elif (hand_landmarks.landmark[8].y < hand_landmarks.landmark[5].y)\
                            and (hand_landmarks.landmark[12].y < hand_landmarks.landmark[9].y)\
                            and (hand_landmarks.landmark[16].y > hand_landmarks.landmark[13].y)\
                            and (hand_landmarks.landmark[20].y > hand_landmarks.landmark[17].y):
                                print("Scissors")
                            elif (hand_landmarks.landmark[8].y < hand_landmarks.landmark[5].y)\
                            and (hand_landmarks.landmark[12].y < hand_landmarks.landmark[9].y)\
                            and (hand_landmarks.landmark[16].y < hand_landmarks.landmark[13].y)\
                            and (hand_landmarks.landmark[20].y < hand_landmarks.landmark[17].y):
                                print("Paper")
        if self.skipLevel is True:
            self.cleared = True
            self.cleanup()
    
    def cleanup(self):
        self.environment.removeNode()
        for i in render.getChildren():                                       # type: ignore
            i.removeNode()
        self.cap.release()