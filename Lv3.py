from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionTube, CollisionNode
from panda3d.core import Vec4, Vec3
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import *
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

from GameObject import *

class test(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.cap = cv2.VideoCapture(0)
        
        # self.disableMouse()
        # Load the environment model.
        self.environment = self.loader.loadModel("obj/lv2.obj")
        # Reparent the model to render.
        self.environment.reparentTo(self.render)
        
        self.environment.setPos(0, 0, 0)
        self.environment.setHpr(0,90,0)
        self.environment.setScale(0.003, 0.002, 0.003)
        
        self.render.setShaderAuto()
        
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        
        
        self.keyMap = {
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False,
            "pause" : False
        }

        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        
        self.updateTask = self.taskMgr.add(self.update, "update")
    
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
    
    def update(self, task):                                        # type: ignore
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
        return task.cont 

app = test()
app.run() 