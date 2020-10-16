import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('ff.xml')
img = cv2.imread('test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

fact = 1.2;
x,y,w,h = faces[0]
w2, h2 = (int(w * fact), int(h * fact))
x -= (w2 - w) // 2;
y -= (h2 - h) // 2;
roi_color = img[y:y + h2, x:x + w2]
#img = cv2.rectangle(img, (x, y), (x + w2, y + h2), (255, 0, 0), 2)
cv2.imwrite('ext.png', roi_color)
#cv2.imshow('img',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
