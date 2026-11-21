#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import time

class MoveRobot:
    def __init__(self):
        rospy.init_node('move_robot_node', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.vel_msg = Twist()
        rospy.Subscriber('button_press', String, self.button_callback)

    def button_callback(self, msg):
        if msg.data == "button_pressed":
            rospy.loginfo("Button pressed. Starting the robot movement.")
            self.move_robot()

    def move_robot(self):
        # Set linear speed
        self.vel_msg.linear.x = 0.99  # Adjust speed as needed
        self.vel_msg.linear.y = 0
        self.vel_msg.linear.z = 0

        # Set angular speed
        self.vel_msg.angular.x = 0
        self.vel_msg.angular.y = 0
        self.vel_msg.angular.z = 0  # No angular velocity for straight motion

        # Time to run the robot
        start_time = time.time()
        while time.time() - start_time <= 5.0:  # Move for 5 seconds
            self.velocity_publisher.publish(self.vel_msg)
            rospy.sleep(0.1)

        # Stop the robot after 5 seconds
        self.vel_msg.linear.x = 0
        self.velocity_publisher.publish(self.vel_msg)

if __name__ == '__main__':
    try:
        move_robot_object = MoveRobot()
        rospy.spin()  # Keep the node running and waiting for button press
    except rospy.ROSInterruptException:
        pass
