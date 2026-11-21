#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

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
        self.goal_distance = 3.0  # Distance to travel towards the goal in meters
        self.goal_speed = 0.3  # Speed to move towards the goal in meters per second
        self.goal_reached = False
        self.start_time = rospy.Time.now()  # Time when the robot starts
        
        # Wait for the scan callback to get initial sensor data
        rospy.sleep(1)

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

    def move_robot(self):
        # Move towards the goal distance
        while not self.goal_reached and not rospy.is_shutdown():
            # Calculate elapsed time
            current_time = rospy.Time.now()
            elapsed_time = (current_time - self.start_time).to_sec()
            
            if self.obstacle_detected:
                # Avoid obstacle
                self.move_cmd.linear.x = 0
                if self.turn_direction == 'left':
                    self.move_cmd.angular.z = self.turn_speed
                elif self.turn_direction == 'right':
                    self.move_cmd.angular.z = -self.turn_speed
            else:
                # Move forward towards goal
                self.move_cmd.linear.x = self.goal_speed
                self.move_cmd.angular.z = 0
            
            # Publish Twist message to /cmd_vel topic
            self.vel_pub.publish(self.move_cmd)
            self.rate.sleep()
            
            # Check if goal distance reached
            if elapsed_time >= self.goal_distance / self.goal_speed:
                self.goal_reached = True
        
        # Stop the robot when goal is reached
        self.move_cmd.linear.x = 0
        self.move_cmd.angular.z = 0
        self.vel_pub.publish(self.move_cmd)
        rospy.loginfo("Goal reached!")

    def run(self):
        try:
            # Move the robot towards the goal while avoiding obstacles
            self.move_robot()
        
        except rospy.ROSInterruptException:
            pass

if __name__ == '__main__':
    robot = AutonomousRobot()
    robot.run()
