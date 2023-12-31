#!/usr/bin/env python

import rospy
import sys
import rospkg
import numpy as np
from sensor_msgs.msg import LaserScan
from lidar_camera_calibration.msg import obTF


"""
Subscribe 'scan_filtered' and
Publish 'ob_TF'
"""


class Lidar(object):
    def __init__(self):
        super(Lidar, self).__init__()
        self.ranges = []
        self.part_fin = []
        self.part_index = []
        self.fin = []
        self.threshold_range = rospy.get_param("threshold_range", 5.0)

        rospy.Subscriber("/scan_filtered", LaserScan, self.laserCallback)

        self.part_pub = rospy.Publisher("ob_TF",obTF,queue_size=1)

    def laserCallback(self, msg):
        self.ranges = msg.ranges
        
    def partYN(self):
        self.part_fin = []
        partitionA = 0
        partitionB = 0
        partitionC = 0
        partitionD = 0

        DEG = 10

        for i in range(len(self.ranges)):
            TF = self.ranges[i]
            if TF != 0 and TF <= self.threshold_range:
                if i >= 0 and i < 180 - (DEG * 2):
                    partitionA = 1
                if i >= 180 - (DEG * 2) and i < 180:
                    partitionB = 1
                if i >= 180 and i < 180 + (DEG * 2):
                    partitionC = 1
                if i >= 180 + (DEG * 2) and i < 361:
                    partitionD = 1
        self.part_fin = [partitionA, partitionB, partitionC, partitionD]

    def xylistMake(self):
        if len(self.part_index) < 5:
            self.part_index.append(self.part_fin)

        else:
            print("error")

    def thresholding(self):
        self.fin = []
        A = 0
        B = 0
        C = 0
        D = 0
        a = 0
        b = 0
        c = 0
        d = 0
        for i in range(len(self.part_index)):
            A = A + self.part_index[i][0]
            B = B + self.part_index[i][1]
            C = C + self.part_index[i][2]
            D = D + self.part_index[i][3]
        if A > 2:
            a = 1
        if B > 2:
            b = 1
        if C > 2:
            c = 1
        if D > 2:
            d = 1

        self.fin = [a, b, c, d]

    def pubResults(self, publisher):
        partTF = obTF()

        try:
            partTF.side_right = self.fin[0]
            partTF.front_right = self.fin[1]
            partTF.front_left = self.fin[2]
            partTF.side_left = self.fin[3]

            publisher.publish(partTF)

        except Exception as ex:
            print(ex)

    def main(self):
        self.partYN()
        self.xylistMake()
        if len(self.part_index) == 5:
            self.thresholding()
            self.pubResults(publisher=self.part_pub)
            # print(self.fin)
            del self.part_index[0]


if __name__ == "__main__":
    rospy.init_node("check_obstacles")

    pub = rospy.Publisher("ob_TF", obTF, queue_size=1)

    lidar = Lidar()

    r = rospy.Rate(100.0)
    while not rospy.is_shutdown():
        lidar.main()
        r.sleep()