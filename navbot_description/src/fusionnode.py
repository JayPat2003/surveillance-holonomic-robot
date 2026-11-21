#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan, Imu
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import sin, cos
import numpy as np

class EKFNode:
    def __init__(self):
        rospy.init_node('ekf_node', anonymous=True)

        self.odom_pub = rospy.Publisher('odom', Odometry, queue_size=10)

        self.rplidar_sub = rospy.Subscriber('rplidar_scan', LaserScan, self.rplidar_callback)
        self.mpu6050_sub = rospy.Subscriber('mpu6050_data', Imu, self.mpu6050_callback)

        self.last_time = rospy.Time.now()

        # Initialize variables for EKF
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.v = 0.0
        self.w = 0.0

        # EKF parameters
        self.Q = np.eye(3) * 0.01  # Process noise covariance matrix
        self.R = np.eye(3) * 0.01  # Measurement noise covariance matrix
        self.P = np.eye(3) * 0.1  # Initial estimate covariance matrix

    def rplidar_callback(self, data):
        # Process RPLIDAR data
        ranges = data.ranges
        angle_min = data.angle_min
        angle_increment = data.angle_increment

        # Calculate average distance and angle
        valid_ranges = [r for r in ranges if r != 0.0 and not np.isinf(r)]
        if valid_ranges:
            avg_distance = np.mean(valid_ranges)
            avg_angle = angle_min + angle_increment * (len(ranges) // 2)  # Middle angle
        else:
            return

        # Predict step of the EKF
        self.x += self.v * cos(self.theta) * dt
        self.y += self.v * sin(self.theta) * dt
        self.theta += self.w * dt

        # Update covariance matrix
        self.P = self.P + self.Q

        # Measurement update step of the EKF using RPLIDAR data
        z_lidar = np.array([self.x, self.y, self.theta])  # Measurement vector from RPLIDAR
        H_lidar = np.eye(3)  # Measurement matrix for RPLIDAR
        K_lidar = np.dot(self.P, np.dot(H_lidar.T, np.linalg.inv(np.dot(H_lidar, np.dot(self.P, H_lidar.T)) + self.R)))  # Kalman gain for RPLIDAR
        innovation_lidar = z_lidar - np.array([avg_distance, avg_angle, 0])  # Innovation vector for RPLIDAR
        self.x = self.x + K_lidar[0][0] * innovation_lidar[0]
        self.y = self.y + K_lidar[1][0] * innovation_lidar[1]
        self.theta = self.theta + K_lidar[2][0] * innovation_lidar[2]

        # Update covariance matrix
        self.P = np.dot((np.eye(3) - np.dot(K_lidar, H_lidar)), self.P)

        # Publish odometry
        self.publish_odometry(current_time)

    def mpu6050_callback(self, data):
        # Process MPU6050 data
        quaternion = (
            data.orientation.x,
            data.orientation.y,
            data.orientation.z,
            data.orientation.w
        )
        (roll, pitch, yaw) = euler_from_quaternion(quaternion)

        # Calculate time difference
        current_time = rospy.Time.now()
        dt = (current_time - self.last_time).to_sec()
        self.last_time = current_time

        # Predict step of the EKF
        self.x += self.v * cos(self.theta) * dt
        self.y += self.v * sin(self.theta) * dt
        self.theta += self.w * dt

        # Update covariance matrix
        self.P = self.P + self.Q

        # Measurement update step of the EKF using MPU6050 data
        z_mpu = np.array([self.x, self.y, self.theta])  # Measurement vector from MPU6050
        H_mpu = np.eye(3)  # Measurement matrix for MPU6050
        K_mpu = np.dot(self.P, np.dot(H_mpu.T, np.linalg.inv(np.dot(H_mpu, np.dot(self.P, H_mpu.T)) + self.R)))  # Kalman gain for MPU6050
        innovation_mpu = z_mpu - np.array([self.x, self.y, self.theta])  # Innovation vector for MPU6050
        self.x = self.x + K_mpu[0][0] * innovation_mpu[0]
        self.y = self.y + K_mpu[1][0] * innovation_mpu[1]
        self.theta = self.theta + K_mpu[2][0] * innovation_mpu[2]

        # Update covariance matrix
        self.P = np.dot((np.eye(3) - np.dot(K_mpu, H_mpu)), self.P)

        # Publish odometry
        self.publish_odometry(current_time)

    def publish_odometry(self, current_time):
        odom = Odometry()
        odom.header.stamp = current_time
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"

        # Set position
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0

        # Set orientation
        odom_quaternion = tf.transformations.quaternion_from_euler(0, 0, self.theta)
        odom.pose.pose.orientation.x = odom_quaternion[0]
        odom.pose.pose.orientation.y = odom_quaternion[1]
        odom.pose.pose.orientation.z = odom_quaternion[2]
        odom.pose.pose.orientation.w = odom_quaternion[3]

        # Set velocity
        odom.twist.twist.linear.x = self.v
        odom.twist.twist.angular.z = self.w

        self.odom_pub.publish(odom)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        ekf_node = EKFNode()
        ekf_node.run()
    except rospy.ROSInterruptException:
        pass
