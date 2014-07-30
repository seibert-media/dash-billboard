import cv2
import json
import numpy as np
import os.path
import signal
import threading
import time

import Log
import Device

class RectangleUtils:
    @staticmethod
    def rect_center(rect):
        if rect == None:
            center = None
        else:
            x1, y1, x2, y2 = rect
            center = 0.5 * (np.array([x2, y2]) + np.array([x1, y1]))
            center = center.astype(int)
        return center
    
    @staticmethod
    def biggest_rect(rects):
        if len(rects) == 0:
            max_rect = None
        else:
            max_rect = (0, 0, 0, 0)
            for x1, y1, x2, y2 in rects:
                if x2-x1 > max_rect[2]-max_rect[0] and y2-y1 > max_rect[3]-max_rect[1]:
                    max_rect = (x1, y1, x2, y2)
        return max_rect


class LauncherControleThread(threading.Thread):
    def __init__(self, rocket_device, frame_rect):
        threading.Thread.__init__(self)
        self.allowed_center_offset_error = 30
        self.rocket_device = rocket_device
        self.frame_center = RectangleUtils.rect_center(frame_rect)
    
    def stop(self):
        self.rocket_device.send_cmd(Device.STOP)
        
    def move_to(self, target):
        command = 0x00
        if target != None:
            offset = target - self.frame_center
            cmd_str = ""
            if abs(offset[0]) > abs(offset[1]):
                if offset[0] < -self.allowed_center_offset_error:
                    command = Device.RIGHT
                    cmd_str += " right"
                elif offset[0] > self.allowed_center_offset_error:
                    command = Device.LEFT
                    cmd_str += " left"
            else:
                if offset[1] < -self.allowed_center_offset_error:
                    command = Device.UP
                    cmd_str += " up"
                elif offset[1] > self.allowed_center_offset_error:
                    command = Device.DOWN
                    cmd_str += " down"
            Log.log("Targeting: " + str(State.target) + ", Framecenter: " + str(self.frame_center) + ", Offset: " + str(offset) + ", CMD:" + cmd_str + "(" + str(command) + ")")
        if command > 0:
            self.rocket_device.send_cmd(command)
        else:
            self.stop()
        
    def run(self):
        while not State.stop:
            self.move_to(State.target)
        self.stop()


class TargetFaceDetectionThread(threading.Thread):
    def __init__(self, capture_device, frame_rect):
        threading.Thread.__init__(self)
        self.cascade_fn = "haarcascades/haarcascade_frontalface_alt2.xml"
        if not os.path.isfile(self.cascade_fn):
            raise Exception("Cascade '"+self.cascade_fn+" not found.")
        self.cascade = cv2.CascadeClassifier(self.cascade_fn)
        self.frame_center = RectangleUtils.rect_center(frame_rect)
    
    def detect_faces(self, img):
        cv2.imshow('gray', img)
        rects = self.cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=2, minSize=(40, 40), flags = cv2.CASCADE_SCALE_IMAGE)
        if len(rects) == 0:
            return []
        rects[:,2:] += rects[:,:2]
        return rects
    
    def detect_target(self, img):
        roi = None
        target = None
        if img != None:
            gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            rects = self.detect_faces(gray)
            biggest_rect = RectangleUtils.biggest_rect(rects)
            roi = biggest_rect
            target = RectangleUtils.rect_center(biggest_rect)
        return (roi, target)
        
    def run(self):
        while not State.stop:
            (State.roi, State.target) = self.detect_target(State.frame)
        State.roi = State.target = None


class CameraThread(threading.Thread):
    def __init__(self, capture_device, frame_rect):
        threading.Thread.__init__(self)
        self.showWindow = True
        self.crossSize = 5
        self.thickness = 2
        self.capture_device = capture_device
        self.frame_rect = frame_rect
        self.frame_center = RectangleUtils.rect_center(frame_rect)
        
    def draw_cross(self, img, pt, color):
        if pt != None:
            cv2.line(img, tuple(np.array(pt) + np.array([-self.crossSize, -self.crossSize])), tuple(np.array(pt) + np.array([ self.crossSize, self.crossSize])), color, self.thickness)
            cv2.line(img, tuple(np.array(pt) + np.array([ self.crossSize, -self.crossSize])), tuple(np.array(pt) + np.array([-self.crossSize, self.crossSize])), color, self.thickness)
            
    def draw_rect(self, img, rect, color):
        if rect != None:
            x1, y1, x2, y2 = rect
            cv2.rectangle(img, (x1, y1), (x2, y2), color, self.thickness)
            
    def run(self):
        while True:
            ret, img = self.capture_device.read()
            cv2.resize(img, self.frame_rect)
            img = cv2.flip(img, 0)
            State.frame = img.copy()
            if self.showWindow:
                self.draw_rect(img, State.roi, (0, 255, 0))
                self.draw_cross(img, State.target, (0, 255, 0))
                self.draw_cross(img, self.frame_center, (0, 0, 255))
                cv2.imshow('facedetect', img)
                
            if 0xFF & cv2.waitKey(5) == 27:
                State.stop = True
                break
        
        State.frame = None
        if self.showWindow:
            cv2.destroyAllWindows()


class State:
    stop = False
    frame = None
    target = None
    roi = None
    
    @staticmethod
    def init():
        State.stop = False
        State.frame = None
        State.target = None
        State.roi = None


class Guard:
    def __init__(self, rocket_device, video_src=0):
        try: self.video_src = int(video_src)
        except ValueError: pass
        
        self.rocket_device = rocket_device
        self.frame_size = (320, 240)
        #self.frame_size = ("auto", "auto")
    
    def create_capture(self, source = 0):
        cap = cv2.VideoCapture(source)
        if cap is None or not cap.isOpened():
            raise Exception('Unable to open video source: ' + source)
        return cap
    
    def frame_rect(self, cap):
        width = self.frame_size[0]
        if (width == "auto"):
            width = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
        else:
            cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
        height = self.frame_size[1]
        if (height == "auto"):
            height = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
        else:
            cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)
        return (0, 0, width, height)
        
    def start(self):
        cv2.namedWindow('facedetect');
        cv2.namedWindow('gray');
        
        State.init()
        capture_device = self.create_capture(self.video_src)
        frame_rect = self.frame_rect(capture_device)
        
        camera_thread = CameraThread(capture_device, frame_rect)
        target_face_detection_thread = TargetFaceDetectionThread(capture_device, frame_rect)
        launcher_controle_thread = LauncherControleThread(self.rocket_device, frame_rect)
        
        camera_thread.start()
        target_face_detection_thread.start()
        launcher_controle_thread.start()
        
        launcher_controle_thread.stop()
        target_face_detection_thread.join()
        camera_thread.join()
        capture_device.release()
