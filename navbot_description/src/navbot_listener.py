#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

def start_moving(data):
    if data.data == "START":
        rospy.loginfo("Button Pressed: Robot starts moving")
        # Publish a command to start moving
        move_cmd = Twist()
        move_cmd.linear.x = 10.0  # Move forward with 10 m/s
        pub.publish(move_cmd)

def listener():
    global pub
    rospy.init_node('arduino_listener', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('button_topic', String, start_moving)
    rospy.spin()

if __name__ == '__main__':
    listener()
