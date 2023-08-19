#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from mission.msg import BoundingBox, BoundingBoxes

def talker():
    pub1 = rospy.Publisher('bounding_boxes', BoundingBoxes, queue_size=10)
    # pub2 = rospy.Publisher('/bounding_boxes', BoundingBoxes, queue_size=10)
    rospy.init_node('yolo_falsedata', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        boxes = BoundingBoxes()
        boxes.header.stamp = rospy.Time.now()
        boxes.header.frame_id = 'camera'
        boxes.image_header.stamp = rospy.Time.now()
        boxes.image_header.frame_id = 'camera'
        box = BoundingBox()
        box.probability = 0.8
        box.xmin = 300
        box.xmax = 500
        box.ymin = 500
        box.ymax = 600
        box.id = 1
        box.Class = "B1"
        boxes.bounding_boxes.append(box)
        pub1.publish(boxes)
        # pub2.publish(boxes)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass