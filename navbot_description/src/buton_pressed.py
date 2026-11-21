#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

def button_callback(data):
    if data.data == "button_pressed":
        rospy.loginfo("Button pressed! Moving robot...")

        # Create Twist message
        twist = Twist()
        twist.linear.x = 0.1  # linear velocity (m/s)
        twist.angular.z = 0.1  # angular velocity (rad/s)

        # Publish Twist message to '/cmd_vel' topic
        cmd_vel_pub.publish(twist)

def listener():
    rospy.init_node('button_listener', anonymous=True)

    rospy.Subscriber("button_topic", String, button_callback)
    rospy.spin()

if __name__ == '__main__':
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    listener()
