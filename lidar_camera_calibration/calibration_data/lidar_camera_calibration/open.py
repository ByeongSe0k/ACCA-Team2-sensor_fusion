#!/usr/bin/env python3

import numpy as np


euler = np.load(file = '/home/lee/catkin_ws/src/lidar_camera_calibration/calibration_data/lidar_camera_calibration/euler.npy')
rlc = np.load(file = '/home/lee/catkin_ws/src/lidar_camera_calibration/calibration_data/lidar_camera_calibration/R.npy')
tlc = np.load(file = '/home/lee/catkin_ws/src/lidar_camera_calibration/calibration_data/lidar_camera_calibration/T.npy')
print("euler_matrix : ")
print(euler)
print("-----------------")
print("degree_euler_matrix : ")
print(np.rad2deg(euler[0]),np.rad2deg(euler[1]),np.rad2deg(euler[2]))
print("-----------------")
print("rlc : ")
print(rlc)
print("-----------------")
print("tlc : ")
print(tlc)