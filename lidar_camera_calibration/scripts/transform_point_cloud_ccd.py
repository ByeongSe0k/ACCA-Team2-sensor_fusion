#!/usr/bin/env python

from threading import Lock
import rospy
import tf2_ros
import tf2_py as tf2
from sensor_msgs.msg import PointCloud2
from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud

class TransformPointCloud:
    def __init__(self):
        self.a = None
        self.tf_buffer = tf2_ros.Buffer()
        self.tl = tf2_ros.TransformListener(self.tf_buffer)
        self.pub = rospy.Publisher("pcdtf1", PointCloud2, queue_size=1)
        # self.pub2 = rospy.Publisher("pcdtf2",PointCloud2,queue_size=2)
        self.sub = rospy.Subscriber("before_adaptive1", PointCloud2,
                                    self.point_cloud_callback, queue_size=1)
        # self.sub2 = rospy.Subscriber("before_adaptive2", PointCloud2,
        #                             self.point_cloud_callback2,queue_size=2)

    def point_cloud_callback(self, msg):
        try:
            trans = self.tf_buffer.lookup_transform("velodyne","camera",rospy.Time(0))
            self.a = do_transform_cloud(msg, trans)
        except tf2_ros.LookupException:
            pass

        if self.a :
            self.pub.publish(self.a)
        
    # def point_cloud_callback2(self, msg):
    #     try:
    #         trans = self.tf_buffer.lookup_transform("velodyne","camera",rospy.Time(0))
    #         a = do_transform_cloud(msg, trans)
    #     except tf2_ros.LookupException:
    #         pass
    #     print(a)
    #     self.pub2.publish(a)

if __name__ == '__main__':
    rospy.init_node('transform_point_cloud_ccd')
    transform_point_cloud = TransformPointCloud()
    rospy.spin()
