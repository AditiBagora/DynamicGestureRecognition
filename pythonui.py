import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import imutils
import pyttsx3
from collections import deque
# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
import threading
import time
import wx
import gui_code2
#importing * : to enable writing sin(13) instead of math.sin(13)
from math import *
cb=[]
y=0
direction = ""
counter=0
mv=[]
pts = deque(maxlen=2000)
move= deque(maxlen=2000)
counter = 0
(dX, dY) = (0, 0)
centre=[]
words=['Swipe','Always','See you Later','Oh!I see','Hard of Hearing']
codes=[[1,1,0.5,1],[1,0.5,0.5,0,0],[1,1,0,0],[1,1,0,0,0],[1,0,0,0]]
movement=['RIGHT','Circular',['UP', 'LEFT', 'DOWN'],['LEFT', 'DOWN','LEFT', 'DOWN'],['RIGHT', 'DOWN']]
#inherit from the MyFrame1 created in wxFowmBuilder and create CalcFrame
class MyFrame1(gui_code2.MyFrame2):
    #constructor
    def __init__(self,parent):
        #initialize parent class
        gui_code2.MyFrame2.__init__(self,parent)
        
    def decode_msg( self, event ):
      image_file_path=self.m_filePicker3.GetPath()
      
      def gesture():
         #print(threading.current_thread().getName(), 'Starting')
         cap = cv2.VideoCapture(image_file_path)
         (grabbed, image)= cap.read()
         image = imutils.resize(image,width=600)
         image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
         data=[]
         r=image.shape[0]
         c=image.shape[1]
         # reshape the image to be a list of pixels
         image1 = image.reshape((r*c, 3))
         k=2
         l=0
         # cluster the pixel intensities
         clt = KMeans(n_clusters = k)
         clt.fit(image1)
         labels = clt.labels_
         for i in range(r):
            for j in range(c):
                if labels[l]==0:
                  image[i][j]=(0,0,0)
                else:  
                  image[i][j]=(255,255,255)
                l=l+1
         image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
         cnts,h = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
                         cv2.CHAIN_APPROX_SIMPLE)
         cX=0
         cY=0
         bm=0
         flag=0
         c=max(cnts, key=cv2.contourArea)
         x,y,w,h=cv2.boundingRect(c)
         if h>w:
               vertical=1
         else:
               vertical=0
         M = cv2.moments(c)
         if M["m00"]<60000:
          cX = int((M["m10"] / M["m00"]))
          cY = int((M["m01"] / M["m00"]))
          cv2.drawContours(image,[c], -1, (100, 100, 100), 3)
          plt.scatter([cX],[cY])
          centroid=(cX,cY)
          centre.append(centroid)
          bm=c
          flag=1
          global cb        
          d1=[]
          cbd=[]
          lt=30
          ut=70
          x=0
          if flag==1:
            if vertical==1:
              plt.imshow(image)
              plt.scatter([cX],[cY])
              c=0
              e=0
              f=0
              j=0
              for i in bm[:,0]:
                c=c+1
              for i in range(c-1):
                g=bm[i]-bm[i+1]
                if g[:,0]>0:
                  d=g[:,1]/g[:,0]
                  if d>0:
                    f=0
                  else:
                    if flag==0:
                      f=f+1
                    flag=0
                  if f==10:
                      d1.append(bm[i-10,0])
              for i in d1:
                 dist=cY-i[1]
                 if dist<0:
                     dist=-dist
                 
                 cbd.append(dist)
                 plt.scatter([i[0]],[i[1]])
                 x=x+1
              for i in cbd:
                 if ((i>lt)and(i<ut)):
                    cb.append(0.5)
                 elif(i>ut):
                    cb.append(1)
                 else:
                    if i<0:
                      cb.append(0)
              while x!=5:
                 cb.append(0)
                 x=x+1
            else:
              plt.imshow(image)
              plt.scatter([cX],[cY])
              c=0
              e=0
              f=0
              j=0
              for i in bm[:,0]:
                c=c+1
              for i in range(c-1):
                g=bm[i]-bm[i+1]
                
                if g[:,0]>0:
                   
                  d=g[:,1]/g[:,0]
                  
                  if d<0:
                    f=0
                  else:
                    if flag==0:
                      f=f+1
                    flag=0
                      
                  if f==15:
                      
                      d1.append(bm[i-15,0])
                  
              for i in d1:
                 dist=cX-i[0]
                 if dist<0:
                     dist=-dist
                 
                 cbd.append(dist)
                 plt.scatter([i[0]],[i[1]])
                 x=x+1
              for i in cbd:
                 if ((i>lt)and(i<ut)):
                    cb.append(0.5)
                 elif(i>=ut):
                    cb.append(1)
                 elif(i<lt):
                    cb.append(0)
                 else:
                    if i<0:
                      cb.append(0)
              while x!=5:
                 cb.append(0)
                 x=x+1
          plt.show()
         # print(threading.current_thread().getName(), 'Exiting')
      def centroid():
          global counter
          global direction
          global y
          global move
         # print(threading.current_thread().getName(), 'Starting')
          c=0
          g=0
          temp1=0
          temp=""
          n=0
          centroid=(0,0)
          cap = cv2.VideoCapture(image_file_path)
          cX=0
          cY=0
          tX=0
          tY=0
          while True:
           g=g+1
           if g==8:
            g=0
            
            (grabbed, image)= cap.read()
            if not grabbed:
               break;
            image = imutils.resize(image,width=600)
            image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            image = cv2.medianBlur(image,5)
            ret,thr = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
            cnts,h = cv2.findContours(thr.copy(), cv2.RETR_EXTERNAL,
                         cv2.CHAIN_APPROX_SIMPLE)
            
            bm=0
            flag=0
            c=max(cnts, key=cv2.contourArea)
            M = cv2.moments(c)
            cX=int(M["m10"] / M["m00"])
            cY=int(M["m01"] / M["m00"])
                   
            centroid=(cX,cY)
            pts.append(centroid)
            
            for i in np.arange(1, len(pts)):
               # if either of the tracked points are None, ignore
               # them
               if pts[i - 1] is None or pts[i] is None:
                  continue

               # check to see if enough points have been accumulated in
               # the buffer
               if counter >= 10 and i == 1 and pts[-10] is not None:
                  # compute the difference between the x and y
                  # coordinates and re-initialize the direction
                  # text variables
                  dX = pts[-10][0] - pts[i][0]
                  dY = pts[-10][1] - pts[i][1]
                  (dirX, dirY) = ("", "")

                  # ensure there is significant movement in the
                  # x-direction
                  if np.abs(dX) > 20:
                     dirX = 'RIGHT' if np.sign(dX) == 1 else "LEFT"

                  # ensure there is significant movement in the
                  # y-direction
                  if np.abs(dY) > 20:
                     dirY = "UP" if np.sign(dY) == 1 else "DOWN"

                  # handle when both directions are non-empty
                  if dirX != "" and dirY != "":
                     direction = "{}-{}".format(dirY, dirX)
                  if dirX==""and dirY=="":
                     continue
                  # otherwise, only one direction is non-empty
                  else:
                     direction = dirX if dirX != "" else dirY
            
            if temp!=direction:
              move.appendleft(direction)
              y+=1
            
            temp=direction
            key = cv2.waitKey(1) & 0xFF
            counter += 1
            key = cv2.waitKey(1) & 0xFF
              # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
              break
         # print(threading.current_thread().getName(), 'Exiting')
          cap.release()
      def direction():
             # print(threading.current_thread().getName(), 'Starting')
              global y
              global mv
              global move
              if y==1:
                 mv=move.popleft()
              else:
                for i in np.arange(1, len(pts)):
                  if y%2==0 and y!=0:
                   t1=move.popleft()
                   t2=move.popleft()
                   
                   y=y-2
                   
                   if t1=="RIGHT" and t2=="LEFT" or t1=="LEFT" and t2=="RIGHT":
                    mv="Circular"
                    
                    break
                   else:
                    if t1=="UP" and t2=="DOWN" or t1=="DOWN" and t2=="UP":
                     mv="Circular"
                     break
                    else:
                     mv.append(t1)
                     mv.append(t2)
                     
                  else:
                    if y!=0:  
                     t3=move.popleft()
                     
                     y=y-1
                     mv.append(t3)
              #print(threading.current_thread().getName(), 'Exiting')
      #Th=threading.Thread(name='gesturec',target=gesturec)
      t = threading.Thread(name='Gesture', target=gesture)
      t1 = threading.Thread(name='Centroid', target=centroid)
      t2 = threading.Thread(name='direction', target=direction)
      #th.start()
      #th.join()
      t.start()
      t.join()
      t1.start()
      t1.join()
      t2.start()
      t2.join()
      j=0
      k=0
      str1 = ''.join(str(e) for e in cb)
      self.m_textCtrl5.SetValue(str1)
      str2 = ''.join(mv)
      self.m_textCtrl6.SetValue(str2)       
      for i in codes:
         if cb==i:
            break
         j=j+1
      for i in movement:
         if i==mv:
            break
         k=k+1
      if j==k and j<5:
       self.m_textCtrl7.SetValue(words[j])
       engine=pyttsx3.init('dummy')
       engine.say(words[j])
       engine.runAndWait()
      else:
       engine=pyttsx3.init('dummy')
       self.m_textCtrl7.SetValue("No Record of the gesture exist")
       engine.say("No Record of the gesture exist")
       engine.runAndWait()
      cv2.destroyAllWindows()
      event.Skip()
#mandatory in wx, create an app, False stands for not deteriction stdin/stdout
#refer manual for details
app = wx.App(False)     
#create an object of CalcFrame
frame = MyFrame1(None)
#show the frame
frame.Show(True)
#start the applications
app.MainLoop()








