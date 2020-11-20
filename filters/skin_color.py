import cv2
import numpy

#Fonction qui détermine la couleur de peau d'un acteur à partir de son visage (on analyse tout particulièrement la proportion de bleu dans la composition)

def ethnic(file):
    img = cv2.imread(file)
    face_cascade = cv2.CascadeClassifier('./face_detect/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 1)
    try :
        (x,y,w,h)=faces[0]
    except:
        print("No face detected")
    e1, e2= int(w*0.1), int(h*0.1)
    res=img[y+e2:y+h-e2,x+e1:x+w-e1]
    #cv2.imshow('img', res)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    avg_color_per_row = numpy.average(res, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)
    print(avg_color)
    return avg_color[0]<=95
    
if __name__=='main':
    for i in range(1,21):
        res = './dataset/ethnic_testing/00'+str(i)+'.jpg'
        print(i, ethnic(res))
    pass