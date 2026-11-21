#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import time

def move_straight(distance, speed):
    # Initialize the ROS node
    rospy.init_node('move_robot', anonymous=True)
    
    # Create a publisher to the /cmd_vel topic
    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    # Create a Twist message and set the speed
    move_cmd = Twist()
    move_cmd.linear.x = speed
    move_cmd.angular.z = 0
    
    # Calculate the time needed to travel the specified distance
    travel_time = distance / speed
    
    # Get the current time
    start_time = time.time()
    
    # Move forward for the calculated time
    while time.time() - start_time < travel_time:
        vel_pub.publish(move_cmd)
        rospy.sleep(0.1)
    
    # Stop the robot
    move_cmd.linear.x = 0
    vel_pub.publish(move_cmd)
    
    # Pause for a moment
    rospy.sleep(1)
    
    # Move backward for the same time
    move_cmd.linear.x = -speed
    start_time = time.time()
    
    while time.time() - start_time < travel_time:
        vel_pub.publish(move_cmd)
        rospy.sleep(0.1)
    
    # Stop the robot
    move_cmd.linear.x = 0
    vel_pub.publish(move_cmd)

if __name__ == '__main__':
    try:
        # Move forward 3 meters (3.0 meters) at a speed of 1 meter per second
        move_straight(300.0, 10.0)
    except rospy.ROSInterruptException:
        pass
