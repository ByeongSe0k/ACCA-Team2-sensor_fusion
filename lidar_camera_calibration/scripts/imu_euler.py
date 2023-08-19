#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
from tf.transformations import *
import math as m

class Euler:
    def __init__(self):
        rospy.Subscriber("imu/data",Imu,self.callback)

    def callback(self,msg):
        roll,pitch,yaw = euler_from_quaternion([msg.orientation.x,msg.orientation.y,msg.orientation.z,msg.orientation.w])
        print("Roll : %.3f Pitch : %.3f Yaw : %.3f" %(m.degrees(roll),m.degrees(pitch),m.degrees(yaw)))

def main():
    rospy.init_node("imu_euler",anonymous=True)
    e = Euler()
    rospy.spin()

if __name__=="__main__":
    main()