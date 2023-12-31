#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ast import Pass
import rospy
from visualization_msgs.msg import Marker, MarkerArray
import time
import tf
import sys
import numpy as np
import math as m
from geometry_msgs.msg import Pose, PoseStamped
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from DB import *
# pathdbA = None
# pathdbB = None


class Delivery(object):
    def __init__(self):
        self.x = []
        self.y = []
        
        # check id_number 
        self.panel = [[4,7],[5,8],[6,9]]  #[[A1,B1],[A2,B2],[A3,B3]]
        self.panel_id = [0,0,0]
        self.dis = 5 # distance
        self.deli_A = False
        self.deli_B = False
        self.pause = False
        self.count = 0
        self.pathdb = None
        self.pathid = ""
    
    def pathcallback(self, msg):
        self.pathid = msg.path_id
        if self.pathid == "E1A1" : #deli A
            self.pathdb = np.array([msg.cx,msg.cy,msg.cyaw],float)
        elif self.pathid == "E1A1" : #deli B
            self.pathdb = np.array([msg.cx,msg.cy,msg.cyaw],float)
        else :
            pass


    def callback(self, msg):

        if self.deli_A == False and self.pause == False: # state machine
            for marker in msg.markers:
                m_to_p = PoseStamped()

                m_to_p.header.frame_id = "velodyne"
                m_to_p.header.stamp = rospy.Time(0)
                m_to_p.pose.position.x = marker.pose.position.x
                m_to_p.pose.position.y = marker.pose.position.y
                m_to_p.pose.position.z = 0
                m_to_p.pose.orientation.x = 0
                m_to_p.pose.orientation.y = 0
                m_to_p.pose.orientation.z = 0
                m_to_p.pose.orientation.w = 1

                m_to_p = tf_node.transformPose("map", m_to_p)

                d = m.sqrt(marker.pose.position.x**2 + marker.pose.position.y**2)

                for i in range(3):
                    if (marker.id)//10000 in self.panel[i] :  
                        self.x.append(m_to_p.pose.position.x)
                        self.y.append(m_to_p.pose.position.y)
                        
                        self.panel_id[i] += 1
                        if (d<=self.dis):
                            self.pointpublish()
                            # self.pathdb = pathdbB

        elif self.pause == True and self.deli_B == False:
            self.count += 1
            if self.count >= 300:
                self.pause = False

        elif self.deli_A == True and self.deli_B == False:

            for marker in msg.markers:
                
                m_to_p = PoseStamped()

                m_to_p.header.frame_id = "velodyne"
                m_to_p.header.stamp = rospy.Time(0)
                m_to_p.pose.position.x = marker.pose.position.x
                m_to_p.pose.position.y = marker.pose.position.y
                m_to_p.pose.position.z = 0
                m_to_p.pose.orientation.x = 0
                m_to_p.pose.orientation.y = 0
                m_to_p.pose.orientation.z = 0
                m_to_p.pose.orientation.w = 1

                m_to_p = tf_node.transformPose("map", m_to_p)

                if (marker.id)//10000 == self.panel[self.panel_id.index(max(self.panel_id))][1] :
                    self.x.append(m_to_p.pose.position.x)
                    self.y.append(m_to_p.pose.position.y)

                    d = m.sqrt(marker.pose.position.x**2 + marker.pose.position.y**2)
                    if d <= self.dis :
                        self.pointpublish()

                else:
                    pass
    
        else: 
            pass

    def pointpublish(self):

        panel_x = sum(self.x)/len(self.x)
        panel_y = sum(self.y)/len(self.y)

        #publish
        posestamp = PoseStamped()
        posestamp.header.frame_id = "map"
        posestamp.header.stamp = rospy.Time(0)
        posestamp.pose.position.x = panel_x
        posestamp.pose.position.y = panel_y
        posestamp.pose.position.z = 0


        posestamp.pose.orientation.x = 0
        posestamp.pose.orientation.y = 0
        posestamp.pose.orientation.z = 0
        posestamp.pose.orientation.w = 1
    
        pose_pub.publish(posestamp)
        
        print("publish end.")
        if self.deli_A == True:
            self.deli_B = True
        self.pause = True
        self.deli_A = True
        self.x = []
        self.y = []

    def testcallback(self):
        db = DB("/school_test.db")
        if self.pathid == "" :
            self.pathdb = db.bring_pathinfo("E1A1")
            self.pathid = "E1A1"
        elif self.pathid == "E1A1" and self.deli_A == True:
            self.pathdb = db.bring_pathinfo("E1A1")
            self.pathid = "E1A1"
        else: pass

if __name__ == '__main__':
   
    rospy.init_node('delivery_AB',anonymous=True)
    
    
    # db = DB("/school_test.db")
    # pathdbA = db.bring_pathinfo("E1A1")
    # pathdbB = db.bring_pathinfo("E1A1")
    
    
    deli = Delivery()
    tf_node = tf.TransformListener()
    
    rospy.Subscriber("/nearmarkers",MarkerArray,deli.callback)
    pose_pub = rospy.Publisher("delivery_AB",PoseStamped,queue_size = 5)
    
    # rospy.Subscriber("path_response",PathResponse,deli.pathcallback)

    
    r = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        '''for test'''
        # deli.testcallback()
        ''' for test end'''
        r.sleep()
        