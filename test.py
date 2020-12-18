import cv2
import os

lib_path = 'images'

"""
Create two list:
    One to store the images,
    the other for the names (note we want to save the name to display to user)
"""

images = []
classNames = []

os.chdir('database/magic_cards')
myList = os.listdir(lib_path)

print('Total classes detected: ',len(myList))

"""
NOW TO IMPORT IN THE IMAGES
"""
for x in myList:
    cur = cv2.imread("images/"+x)
    images.append(cur)
    classNames.append(x)
print(classNames)
# usr_img = cv2.imread('database/magic_cards/test/Volrath-the-Shapestealer.jpg',0)
# lib_img = cv2.imread('database/magic_cards/images/Ripjaw-Raptor.jpg',0)
#
# orb = cv2.ORB_create(nfeatures=1000)
#
# kp1,des1 = orb.detectAndCompute(usr_img,None)
# kp2,des2 = orb.detectAndCompute(lib_img,None)
#
# usrKp1 = cv2.drawKeypoints(usr_img,kp1,None)
# libKp2 = cv2.drawKeypoints(lib_img,kp2,None)
#
# bf = cv2.BFMatcher()
# matches = bf.knnMatch(des1,des2,k=2)
#
# good = []
#
# for m,n in matches:
#     if m.distance < 0.75*n.distance:
#         good.append([m])
# print(len(good))
# m_img = cv2.drawMatchesKnn(usr_img,kp1,lib_img,kp2,good,None,flags=2)
#
# cv2.namedWindow('lib',cv2.WINDOW_NORMAL)
# cv2.resizeWindow('lib',(640,540))
# cv2.namedWindow('m_img ',cv2.WINDOW_NORMAL)
# cv2.resizeWindow('m_img ',(640,540))
#
# cv2.imshow('usr',usr_img)
# cv2.imshow('lib',lib_img)
# cv2.imshow('m_img ',m_img )
# cv2.waitKey(0)
#
# if cv2.waitKey(1) & 0xFF == 27:
#     cv2.destroyAllWindows()
