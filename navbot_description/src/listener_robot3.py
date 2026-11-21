#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

def start_moving(data, pub):
    if data.data == "START":
        rospy.loginfo("Button Pressed: Robot 3 starts moving")
        # Publish a command to start moving
        move_cmd = Twist()
        move_cmd.linear.x = 0.900  # Adjust speed as necessary
        pub.publish(move_cmd)

def listener():
    rospy.init_node('arduino_listener_robot3', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)  # Robot 3's cmd_vel topic
    rospy.Subscriber('button_topic_robot3', String, start_moving, pub)
    rospy.spin()

if __name__ == '__main__':
    listener()
