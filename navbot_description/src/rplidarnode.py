#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry

class RPLIDAR_Odometry:
    def __init__(self):
        rospy.init_node('rplidar_odometry_node', anonymous=True)
        
        # Subscriber to RPLIDAR data
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        
        # Publisher for odometry data
        self.odom_pub = rospy.Publisher('/odometry', Odometry, queue_size=10)
        
    def scan_callback(self, scan_data):
        # Here you would process the LaserScan data to calculate odometry
        # For simplicity, let's assume we're just using the ranges to calculate the odometry
        
        # For demonstration purposes, let's say we're extracting the range at a specific angle
        # You should replace this with your actual odometry calculation
        angle_index = len(scan_data.ranges) // 2  # Assuming the Lidar is mounted straight ahead
        range_value = scan_data.ranges[angle_index]
        
        # Create an Odometry message
        odom_msg = Odometry()
        # Fill in odometry data
        # For simplicity, let's say we're using range as odometry value
        odom_msg.pose.pose.position.x = range_value
        odom_msg.pose.pose.position.y = 0.0  # Assuming no lateral movement
        odom_msg.pose.pose.position.z = 0.0  # Assuming no vertical movement
        odom_msg.twist.twist.linear.x = range_value  # Assuming linear velocity is proportional to range
        odom_msg.twist.twist.linear.y = 0.0  # Assuming no lateral velocity
        odom_msg.twist.twist.angular.z = 0.0  # Assuming no angular velocity
        
        # Publish the odometry message
        self.odom_pub.publish(odom_msg)
        
    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        rplidar_odometry = RPLIDAR_Odometry()
        rplidar_odometry.run()
    except rospy.ROSInterruptException:
        pass
