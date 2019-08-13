urviiimport cv2
import os
cam = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

path="/home/urvi/FACE/Final/dataSet"


Id=raw_input('enter your id: ')

User=raw_input('enter your name: ')
cpath=path+"/"+User
os.mkdir(cpath)
#print(cpath)

sampleNum=0
while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        
        #incrementing sample number 
        sampleNum=sampleNum+1
        #saving the captured face in the dataset folder
        
        cv2.imwrite(cpath+ "/"+User+"."+str(sampleNum)+".jpg", img[y:y+h,x:x+w])

        cv2.imshow('frame',img)
    #wait for 100 miliseconds 
    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break
    # break if the sample number is morethan 20
    elif sampleNum>4:
        break
cam.release()
cv2.destroyAllWindows()