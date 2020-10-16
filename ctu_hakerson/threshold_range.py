from __future__ import print_function
import cv2 as cv
import argparse
import numpy as np
import random as rng
import requests
import time
import matplotlib.pyplot as plt

max_value = 255
max_value_H = 360//2

low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value

low_H_ = 0
low_S_ = 0
low_V_ = 0
high_H_ = max_value_H
high_S_ = max_value
high_V_ = max_value



window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
window_object_name = 'Find plate'
window_object_name2 = 'Find food'

low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)
    
def histogram(img):
    histr = np.ones((3, 256,1))
    color = ('b','g','r')
    
    a,b,c = img.shape[0],img.shape[1],img.shape[2]
    img = np.reshape(img,(c,a,b))
    for i, col in enumerate(color):

        histr[i] = cv.calcHist([img],[i],None,[256],[0, 256])
        
    print(histr[0].mean(),histr[1].mean(),histr[2].mean())


parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera divide number.', default=0, type=int)
args = parser.parse_args()

cv.namedWindow(window_capture_name)

"""
cv.namedWindow(window_detection_name)
cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)

"""
cv.namedWindow(window_object_name)
cv.namedWindow(window_object_name2)

frame = cv.imread('plate.jpg')
test_frame = cv.imread('test.jpg')

cap = cv.VideoCapture(args.camera)

loop_count = 0

init_portion = 0
init_time = 0
dish = 0
change_dish = False
empty = False
prev_empty = 0
total_remain_time = 0
total_portion = 0
remain_times = []
portions = []

while True:
    #time.sleep(0.3)
    ret, frame = cap.read()
    #print(frame.shape)
    #frame = cv.bilateralFilter(frame,9,75,75)
    frame = cv.GaussianBlur(frame,(9,9),0)
    h_, w_, _ = frame.shape
    
    
    if frame is None:
        break
    frame_ = frame#.copy()
    #cv.imshow(window_capture_name, frame_)

    frame_HSV = cv.cvtColor(frame_, cv.COLOR_BGR2HSV)
    
    """
    low_V = 0
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    #cv.imshow(window_detection_name, frame_threshold)
    """
    
    low_V_ = 90
    high_S_ = 50
    frame_threshold = cv.inRange(frame_HSV, (low_H_, low_S_, low_V_), (high_H_, high_S_, high_V_))

    """
    if w * h / (h_ * w_) < 0.1:
        print("no plate")
        continue
    """

    contours, hierarchy = cv.findContours(frame_threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    """
    print(contours)
    print(hierarchy)
    break
    """

    frame_show = frame_.copy()
    if empty == True  and prev_empty < 10:
        prev_empty = prev_empty + 1
        
    elif empty == False:
        prev_empty = 0
        
    #cv.imshow(window_capture_name, frame_show)
    
    if len(contours)!=0:
        c = max(contours, key = cv.contourArea)
        area = cv.contourArea(c)
        area_max_plate = area/h_/w_
  #      print("area_max_plate", area_max_plate)
    
        if 0.2>area_max_plate>0.07:
            #print("if")
            #print("prev_empty", prev_empty) 
            #x,y,w,h = cv.boundingRect(c)
            (x_center,y_center), radius = cv.minEnclosingCircle(c)
            x = int(x_center - radius)
            y = int(y_center - radius)
            if x>0 and x<w_ and y>0 and y<h_:
            
                w, h = int(2*radius), int(2*radius)
                #print(x, y, w, h)
                
                cv.rectangle(frame_show, (x, y), (x+w, y+h), (0,0,255), 2)
                cv.imshow(window_capture_name, frame_show)
                empty = False
                
                        
                """
                frame_threshold = frame_threshold[y:y+h, x:x+w]
                frame_ = frame_[y:y+h, x:x+w, :]
                """
                
                #print("prev_empty=",prev_empty,",empty=",empty,"dish=",dish)
                if prev_empty == 10:
                    loop_count = 0
                    change_dish = False

                  
                    
                """
                drawing = np.zeros(frame_.shape, dtype=np.uint8)
                
                color = (255, 255, 255)

                cv.drawContours(drawing, [c], -1, color, cv.FILLED)
                
                mask = cv.cvtColor(drawing, cv.COLOR_BGR2GRAY)
                
                drawing = drawing[y:y+h, x:x+w]
                mask = mask[y:y+h, x:x+w]
                """
                
                frame_ = frame_[y:y+h, x:x+w, :]
                frame_threshold = frame_threshold[y:y+h, x:x+w]
                
                """
                mask_inv = cv.bitwise_not(drawing)


                target = cv.bitwise_and(frame_, frame_, mask = mask)
                target = cv.bitwise_or(target, mask_inv)
                
                cv.imshow(window_object_name, target)
                """
                cv.imshow(window_object_name, frame_)
            #    histogram(target)
                ##cv.imshow("shit", target)
                ##################################################
                #target_HSV = cv.cvtColor(target, cv.COLOR_BGR2HSV)
                """
                target_HSV = cv.cvtColor(frame_, cv.COLOR_BGR2HSV)
                
                low_V = 170
                high_S = 20
                target_threshold = cv.inRange(target_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
                
                cv.imshow(window_object_name2, target_threshold)
                
                
                """
                cv.imshow(window_object_name2, frame_threshold)
                #cv.imshow(window_detection_name, target_threshold)
                #print(target_threshold.shape)
                #print(target_threshold > 0)
                """histagram"""
            #     histr = np.ones((3, 256,1))
            #     sample = 16
            #     histr_sample = np.ones((3, sample,1))
            #     color = ('b','g','r')
            #     
            #     for i, col in enumerate(color):
            #         histr[i] = cv.calcHist([target_HSV],[i],None,[256],[0, 256])
            # 
            #         #print(histr[i])
            #     #print(histr.shape)
            #     
            #     for i, col in enumerate(color):
            #         for j in range(sample):
            #             histr_sample[i][j][0] = int(np.mean(histr[i][j*int(256/sample):(j+1)*int(256/sample)][0]))
            #         
            #         #print(histr_sample[i][j][0])


                """histagram"""



                #plate = np.sum(target_threshold > 0)
                plate = np.sum(frame_threshold > 0)
                
                food = radius*radius*3.14 - plate
                portion = food/(w*h)
                #print(food/(w*h))
                #print("init_portion = ",init_portion)
                if loop_count == 0:
                    init_portion = food/(w*h)
                    init_time = time.time()
                
                remain_time = (time.time() - init_time) / (init_portion - portion) * portion / 60
                remain_time = min(10, remain_time)
                if remain_time < 0:
                    remain_time = 10
                remain_time = int(remain_time)
                portion = int(round(portion*100))
                portions.append(portion)
                remain_times.append(remain_time)
                if loop_count % 20 == 0 and loop_count != 0:
                    #print("id=0&status=1&finished={}&dish=1&time_left={}&order=2".format(portion, remain_time))
                    #print("init_portion=",init_portion)
                    portions.sort()
                    remain_times.sort()
                    #print(portions)
                    #print(remain_times)
                    portions = portions[5:-5]
                    remain_times = remain_times[5:-5]
                    #print(portions)
                    #print(remain_times)
                    total_portion = int(sum(portions) / (init_portion+0.001) / (len(portions)+0.001))
                    total_remain_time = int(sum(remain_times) / (len(remain_times)+0.001))
                    
                    print("portion=",total_portion)
                    print("time_left=",total_remain_time)
                    init_portion_100 = init_portion * 100
                    print('init_portion_100', init_portion_100)
                    print('finished', int(100 -  portion / init_portion_100 * 100))
                    requests.get("http://140.113.68.171:35000/frompie?id=0&status=1&finished={}&dish={}&time_left={}&order=2".format(max(0, int(100 -  portion / init_portion)), dish, remain_time))
                    portions = []
                    remain_times = []
                    total_portion = 0
                    total_remain_time = 0
                
                loop_count += 1
                key = cv.waitKey(30)
                if key == ord('q') or key == 27:
                    break
                
            else:
                cv.imshow(window_capture_name, frame_show)
                cv.imshow(window_object_name, test_frame)
                cv.imshow(window_object_name2, test_frame)
                    
        else:
            #print("else1")
            
            cv.imshow(window_capture_name, frame_show)
            cv.imshow(window_object_name, test_frame)
            cv.imshow(window_object_name2, test_frame)
            #print("prev_empty", prev_empty)
            empty = True
            if prev_empty== 10 and change_dish==False:
                #print("dish=",dish)
                if dish == 1:
                    requests.get("http://140.113.68.171:35000/dequeue")
                dish = 1 if dish == 0 else 0
                #print("dish=",dish)
                change_dish = True
            
                
            
            #continue
            
      
    else:
        print("else2")
        print("prev_empty", prev_empty)
        cv.imshow(window_capture_name, frame_show)
        cv.imshow(window_object_name, test_frame)
        cv.imshow(window_object_name2, test_frame)

        empty = True
        if prev_empty == 10 and change_dish == False:
            print("dish=",dish)
            if dish == 1:
                requests.get("http://140.113.68.171:35000/dequeue")
            dish = 1 if dish == 0 else 0
            print("dish=",dish)
            change_dish = True
    
        
        #continue

    
    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break

cap.release()
cv.destroyAllWindows()

