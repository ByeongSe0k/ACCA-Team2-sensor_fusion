#!/usr/bin/env python3

import rospy
from tf.transformations import *
import math as m
import numpy as np

rospy.init_node("matrix",anonymous=True)
roll = -0.681
pitch = 3.47
yaw = -1.496
#yaw = -1.5
#yaw = -3.299
matrix = euler_matrix(m.radians(roll),m.radians(pitch),m.radians(yaw),'sxyz')

matrix_list = []

for i in range(0,3,1):
    for j in range(0,3,1):
        matrix_list.append(matrix[i][j])

print("rlc:",matrix_list)