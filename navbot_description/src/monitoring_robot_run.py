#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time

class AutonomousRobot:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('move_robot', anonymous=True)
        
        # Create a publisher to the /cmd_vel topic
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        # Create a subscriber to the /scan topic
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        
        self.move_cmd = Twist()
        self.rate = rospy.Rate(10)  # 10 Hz
        
        # Robot state variables
        self.obstacle_detected = False
        self.turn_direction = None
        
        # Parameters for obstacle avoidance
        self.min_distance = 0.5  # Minimum distance to consider an obstacle (adjust as needed)
        self.safe_distance = 1.0  # Safe distance to maintain from obstacles
        self.avoidance_speed = 0.5  # Speed to use during obstacle avoidance
        self.turn_speed = 0.5  # Angular speed for turning during obstacle avoidance
        
        # Goal position
        self.goal_distance = 10.0  # Distance to travel towards the goal in meters
        self.goal_speed = 1.0  # Speed to move towards the goal in meters per second

    def scan_callback(self, scan_data):
        # Check the laser scan data for obstacles
        ranges = scan_data.ranges
        front_min = min(min(ranges[0:10]), min(ranges[-10:]))  # Front 10 degrees
        left_min = min(ranges[80:100])  # Left 20 degrees
        right_min = min(ranges[-100:-80])  # Right 20 degrees
        
        # Determine if an obstacle is detected
        if front_min < self.min_distance or left_min < self.min_distance or right_min < self.min_distance:
            self.obstacle_detected = True
            if left_min < right_min:
                self.turn_direction = 'right'
            else:
                self.turn_direction = 'left'
        else:
            self.obstacle_detected = False
            self.turn_direction = None

    def move_robot(self, distance, speed):
        travel_time = distance / speed
        start_time = rospy.Time.now().to_sec()
        
        while rospy.Time.now().to_sec() - start_time < travel_time and not rospy.is_shutdown():
            if self.obstacle_detected:
                # Avoid obstacle
                self.move_cmd.linear.x = 0
                if self.turn_direction == 'left':
                    self.move_cmd.angular.z = self.turn_speed
                elif self.turn_direction == 'right':
                    self.move_cmd.angular.z = -self.turn_speed
            else:
                # Move forward towards goal
                self.move_cmd.linear.x = speed
                self.move_cmd.angular.z = 0
            
            # Publish Twist message to /cmd_vel topic
            self.vel_pub.publish(self.move_cmd)
            self.rate.sleep()
        
        # Stop the robot when goal is reached
        self.move_cmd.linear.x = 0
        self.move_cmd.angular.z = 0
        self.vel_pub.publish(self.move_cmd)

    def rotate_robot(self, angle, speed):
        # Calculate the time required to rotate the specified angle
        angular_speed = speed
        angular_distance = angle * (3.14159 / 180.0)
        duration = angular_distance / angular_speed
        
        self.move_cmd.linear.x = 0
        self.move_cmd.angular.z = angular_speed if angle > 0 else -angular_speed
        
        start_time = rospy.Time.now().to_sec()
        while rospy.Time.now().to_sec() - start_time < duration and not rospy.is_shutdown():
            self.vel_pub.publish(self.move_cmd)
            self.rate.sleep()
        
        self.move_cmd.angular.z = 0
        self.vel_pub.publish(self.move_cmd)
        
    def run(self):
        try:
            while not rospy.is_shutdown():
                # Move forward towards the goal
                self.move_robot(self.goal_distance, self.goal_speed)
                
                # Check if goal is reached
                if not self.obstacle_detected:
                    rospy.loginfo("Goal reached!")
                
                # Rotate 300 degrees
                self.rotate_robot(300, 0.5)
                
                # Return to the starting position
                self.move_robot(self.goal_distance, self.goal_speed)
                
                rospy.loginfo("Returned to starting position!")
        
        except rospy.ROSInterruptException:
            pass

if __name__ == '__main__':
    robot = AutonomousRobot()
    robot.run()
