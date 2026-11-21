#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu, LaserScan

class NavigationController:
    def __init__(self):
        rospy.init_node('navigation_controller', anonymous=True)
        rospy.Subscriber('/mpu6050_topic', Imu, self.imu_callback)
        rospy.Subscriber('/rplidar_topic', LaserScan, self.laser_scan_callback)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.twist_msg = Twist()

    def imu_callback(self, data):
        # Here you can process IMU data if needed
        pass

    def laser_scan_callback(self, data):
        # Here you can process LaserScan data if needed
        pass

    def send_velocity_command(self, linear_velocity, angular_velocity):
        self.twist_msg.linear.x = linear_velocity
        self.twist_msg.angular.z = angular_velocity
        self.cmd_vel_pub.publish(self.twist_msg)

    def run(self):
        rate = rospy.Rate(30)  # Hz
        while not rospy.is_shutdown():
            # Example: Sending constant forward velocity and zero angular velocity
            self.send_velocity_command(linear_velocity=0.5, angular_velocity=0.0)
            rate.sleep()

if __name__ == '__main__':
    try:
        navigation_controller = NavigationController()
        navigation_controller.run()
    except rospy.ROSInterruptException:
        pass
