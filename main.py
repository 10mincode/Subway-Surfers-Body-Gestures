import cv2
import mediapipe as mp
import time
import threading
import pyautogui

mpDraw=mp.solutions.drawing_utils
mpPose=mp.solutions.pose
pose=mpPose.Pose()
cap=cv2.VideoCapture(0)
v=0
def getaverage(a,b,intornot=True):
    if intornot: return int((a+b)/2)
    else: return (a+b)/2
def get_y():
    time.sleep(10)
    global v,y,y2
    v=getaverage(y,y2)
    time.sleep(10)
    global canplay
    canplay=True
x=threading.Thread(target=get_y)
x.start()
x_direc=0
canplay=False
while True:
    _,image=cap.read()
    image=cv2.flip(image,1)
    imgRGB=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    
    result=pose.process(imgRGB)
    
    if result.pose_landmarks:
        # mpDraw.draw_landmarks(
        #     image,
        #     result.pose_landmarks,
        #     mpPose.POSE_CONNECTIONS
        # )
        landmarks = result.pose_landmarks.landmark
        h,w,_=image.shape
        x,y=int(landmarks[11].x*w),int(landmarks[11].y*h)
        x2,y2=int(landmarks[12].x*w),int(landmarks[12].y*h)
        ax, ay = getaverage(x, x2), getaverage(y, y2)
        if canplay:
            if ay<v-40:
                pyautogui.press("up")
            if ay>v+40:
                pyautogui.press("down")
            
            if ax<x_mid-40:
                if x_direc!=1:
                    pyautogui.press("left")
                    x_direc=1      
            elif ax>x_mid+40:
                
                if x_direc!=2:
                    pyautogui.press("right")
                    x_direc=2
            else: x_direc=0
        cv2.circle(image,(ax,ay),15,(0,255,0),-1)
        
        
    x_mid=int(image.shape[1]/2)
    if v!=0:  
        cv2.line(image,(x_mid-40,v-40),(x_mid-40,v+40),(0,0,255),3)
        cv2.line(image,(x_mid+40,v-40),(x_mid+40,v+40),(0,0,255),3)
        cv2.line(image,(x_mid-40,v-40),(x_mid+40,v-40),(0,0,255),3)
        cv2.line(image,(x_mid-40,v+40),(x_mid+40,v+40),(0,0,255),3)
    cv2.imshow("Image",image)
    if cv2.waitKey(1)==27:
        break
cap.release()
cv2.destroyAllWindows()
