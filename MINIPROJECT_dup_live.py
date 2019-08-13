print("importing required libraries...")
import face_recognition as fr
import cv2
import os
import telepot
import datetime
from twilio.rest import Client
import numpy as np 
from livenessmodel import get_liveness_model
font=cv2.FONT_HERSHEY_SIMPLEX
print("completed importing libraries")
#print()

# print("Connecting to the bot...")
#bot=telepot.Bot("677920014:AAH14Bl2Z1QBUvvdudQEPp839d7MIag82I8")
cap=cv2.VideoCapture(0)
directory=os.listdir("/home/urvi/FACE/")
length=len(directory)	
i=length-1
#print("Connected to bot")
#print()


# Get the liveness network
model = get_liveness_model()

# load weights into new model
model.load_weights("model/model.h5")
print("Loaded model from disk")

#bot starts here

sid="ACf15566b1b3f3dd7d5399f9e958b3268d"
token="ed9cd971fe86deebafa77a747ebe0ab1"

now=datetime.datetime.now()
#cv2.namedWindow("win",cv2.WINDOW_NORMAL)

#client=Client(sid,token)
#print("Acquiring face encodings...")
#for k in range(1,9):
#    sant=fr.load_image_file("H:\\Projects\\face recognition\\santosh"+str(k)+".jpg")
    
check_encode1=[]
img_name=[]

#prepare encodings of all images in the dataset
for filename in os.listdir("/home/urvi/FACE/Final/dataSet/"):
    #print(filename)
    for imgname in os.listdir("/home/urvi/FACE/Final/dataSet/"+filename):
        #print("/home/urvi/FACE/Final/dataSet/"+filename+"/"+imgname)
        img_temp=fr.load_image_file("/home/urvi/FACE/Final/dataSet/"+filename+"/"+imgname)
        img_encode=fr.face_encodings(img_temp)[0]
        check_encode1.append(img_encode)
        img_name.append(filename)
#print(img_name)
print(str(len(check_encode1))+' encodings are created...')
 

def send(frame,j):
    print("Sending msg to bot")
    bot.sendMessage(264855240,"Someone Unknown is at Door")
    client.messages.create(
            to="whatsapp:+919422964800",
            from_="whatsapp:+14155238886",
            body="Someone at your door,please check telegram"
        )
    print("Message Sent")
    print("sending photo")
    bot.sendPhoto(264855240,photo=open("/home/urvi/FACE/"+str(j)+".jpg","rb"))
    print("Photo Sent")
    print()
    return

def send1(nm):
    print("Sending message to bot")
    bot.sendMessage(264855240,nm+" is in front of your house")
    return

process_this_frame = True
input_vid = []

while(True):
    if len(input_vid) < 24:
        ret, frame = cap.read()
        liveimg = cv2.resize(frame, (100,100))
        liveimg = cv2.cvtColor(liveimg, cv2.COLOR_BGR2GRAY)
        input_vid.append(liveimg)
    else:
        print("entered else")
        ret,frame=cap.read()

        #new liveness detection
        liveimg = cv2.resize(frame, (100,100))
        liveimg = cv2.cvtColor(liveimg, cv2.COLOR_BGR2GRAY)
        input_vid.append(liveimg)
        inp = np.array([input_vid[-24:]])
        inp = inp/255
        inp = inp.reshape(1,24,100,100,1)
        pred = model.predict(inp)
        input_vid = input_vid[-25:]
        print("detect live"+str(pred[0][0]))
        
        if pred[0][0]> .47:
            if process_this_frame:
                flag=False
                face_locations=fr.face_locations(frame)
                face_encodings=fr.face_encodings(frame,face_locations)
            
                for (top,right,bottom,left),face_encode in zip(face_locations,face_encodings):
                    match=[]    
                    match=fr.compare_faces(check_encode1,face_encode,tolerance=0.5)
                    name1="Unknown"

                    if True in match:
                        index=match.index(True)
                        name1=img_name[index]
                        cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),3)
                        font=cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(frame,name1,(left+3,bottom-3),font,1.0,(255,255,255),2)
                        #cv2.imshow('win',frame)
                
                    for k in match:
                        if(match[k]==True):          
                            #send1(name[k])
                            f=open("/home/urvi/FACE/Final/log.txt","a")
                            f.write(img_name[k]+" is at home at "+str(now)+"\n")
                            f.close()
                            
                    if match.count(False)==len(match):
                        f=open("/home/urvi/FACE/log.txt","a")
                        f.write("*** Someone Unknown is at Door    "+str(now)+"\n")
                        f.close()
                        j=i+1
                        if(i==-1):
                            cv2.imwrite("/home/urvi/FACE/"+str(j)+".jpg",frame)
                            i=i+1
                        """previous_img=fr.load_image_file("/home/urvi/FACE/"+str(i)+".jpg")
                    print("Hii in false match")
                        previous_face_locations=fr.face_locations(previous_img)
                        previous_encode=fr.face_encodings(previous_img,previous_face_locations)[0]
                        match1=fr.compare_faces(previous_encode,face_encodings)
                        
                    if not True in match1:
                            cv2.imwrite("/home/urvi/FACE/"+str(j)+".jpg",frame)
                            flag=True
                            i=i+1
                    """
                    #print(match)
                    
                
                #if(flag==True):
                #   send(frame,j)
            process_this_frame = not process_this_frame        
        else:
            cv2.putText(frame, 'WARNING!', (frame.shape[1]//2, frame.shape[0]//2), font, 1.0, (255, 255, 255), 1)   
        cv2.imshow('Video', frame)
    if cv2.waitKey(33) == ord('a'):
        print "You stopped..."
        break

        
     #ends here       
    
cap.release()
cv2.destroyAllWindows()
f.close()