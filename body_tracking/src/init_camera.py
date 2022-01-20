#!/usr/bin/env python3
# Author:  
# Date:    2021-19-01
# Version: 0.0.1
# Email: vitor.mendes@ieee.org
# chmod +x setup.bash
# ./setup.bash

from distutils.log import warn
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def main():
    cap_right = cv2.VideoCapture(0)
    cap_left = cv2.VideoCapture(2)
    rospy.init_node('init_camera',anonymous=False)
    print("camera_init runing...")
    print("Crtl+C for quit")
    right_pub = rospy.Publisher('/image_right',Image,queue_size=1)
    left_pub = rospy.Publisher('/image_left',Image,queue_size=1)
    rate = rospy.Rate(30)
    bridge = CvBridge()
    cont = 0

    while not rospy.is_shutdown():
        try:
            ret_r, frame_r = cap_right.read()
            ret_l, frame_l = cap_left.read()
            if ret_r == True:
                if cont == 0:
                    print("img_right published")
                img_right = bridge.cv2_to_imgmsg(frame_r, 'bgr8')
                right_pub.publish(img_right)
            if ret_l == True:
                if cont == 0:
                    print("img_left published")
                img_left = bridge.cv2_to_imgmsg(frame_l, 'bgr8')
                left_pub.publish(img_left)
            if cont == 0 :
                cont += 1

        except KeyboardInterrupt:
            break
        rate.sleep()

if __name__ == '__main__':
    main()