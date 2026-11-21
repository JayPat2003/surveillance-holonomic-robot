#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math

class AutonomousRobot:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('autonomous_robot', anonymous=True)
        
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
        self.avoidance_speed = 0.3  # Speed to use during obstacle avoidance
        self.turn_speed = 0.5  # Angular speed for turning during obstacle avoidance
        
        # Goal position
        self.goal_distance = 10.0  # Distance to travel towards the goal in meters
        self.goal_speed = 0.3  # Speed to move towards the goal in meters per second
        self.goal_reached = False
        
        # Path recording
        self.path = []
        
        # Starting position
        self.starting_position = None

    def scan_callback(self, scan_data):
        # Check the laser scan data for obstacles
        ranges = scan_data.ranges
        front_min = min(min(ranges[0:20]), min(ranges[-20:]))  # Front 20 degrees
        back_min = min(min(ranges[160:180]), min(ranges[180:200]))  # Back 20 degrees
        left_min = min(ranges[80:100])  # Left 20 degrees
        right_min = min(ranges[-100:-80])  # Right 20 degrees
        
        # Determine if an obstacle is detected
        if front_min < self.min_distance or back_min < self.min_distance or left_min < self.min_distance or right_min < self.min_distance:
            self.obstacle_detected = True
            if front_min < back_min and front_min < left_min and front_min < right_min:
                self.turn_direction = 'back'
            elif back_min < front_min and back_min < left_min and back_min < right_min:
                self.turn_direction = 'front'
            elif left_min < right_min:
                self.turn_direction = 'right'
            else:
                self.turn_direction = 'left'
        else:
            self.obstacle_detected = False
            self.turn_direction = None

    def move_robot(self):
        # Reset path and goal state
        self.path = []
        self.goal_reached = False
        
        # Move towards the goal distance
        distance_covered = 0
        while distance_covered < self.goal_distance and not rospy.is_shutdown():
            if self.obstacle_detected:
                # Avoid obstacle
                self.move_cmd.linear.x = 0
                if self.turn_direction == 'left':
                    self.move_cmd.angular.z = self.turn_speed
                elif self.turn_direction == 'right':
                    self.move_cmd.angular.z = -self.turn_speed
                elif self.turn_direction == 'front':
                    self.move_cmd.linear.x = -self.avoidance_speed
                elif self.turn_direction == 'back':
                    self.move_cmd.linear.x = self.avoidance_speed
            else:
                # Move forward towards goal
                self.move_cmd.linear.x = self.goal_speed
                self.move_cmd.angular.z = 0
                distance_covered += self.goal_speed / 10.0  # Assuming rate is 10 Hz
            
            # Record the path
            self.path.append((self.move_cmd.linear.x, self.move_cmd.angular.z))
            
            # Publish Twist message to /cmd_vel topic
            self.vel_pub.publish(self.move_cmd)
            self.rate.sleep()
        
        self.goal_reached = True

        # Stop the robot when goal is reached
        self.move_cmd.linear.x = 0
        self.move_cmd.angular.z = 0
        self.vel_pub.publish(self.move_cmd)
        rospy.loginfo("Goal reached!")

    def turn_in_place(self, angle):
        # Convert angle to radians
        angle_rad = math.radians(angle)
        
        rospy.loginfo("Turning {} degrees...".format(angle))
        
        # Determine direction of turn
        if angle > 0:
            self.move_cmd.angular.z = self.turn_speed
        else:
            self.move_cmd.angular.z = -self.turn_speed
        
        # Calculate turn duration based on angular speed
        turn_duration = abs(angle_rad / self.turn_speed)
        
        # Perform the turn
        start_time = rospy.Time.now().to_sec()
        while (rospy.Time.now().to_sec() - start_time) < turn_duration and not rospy.is_shutdown():
            self.vel_pub.publish(self.move_cmd)
            self.rate.sleep()
        
        # Stop the robot after turn
        self.move_cmd.angular.z = 0
        self.vel_pub.publish(self.move_cmd)
        rospy.loginfo("Turned {} degrees!".format(angle))

    def record_starting_position(self):
        # Record the current position as the starting position
        rospy.loginfo("Recording starting position...")
        self.starting_position = (self.move_cmd.linear.x, self.move_cmd.angular.z)

    def return_to_start(self):
        if not self.starting_position:
            rospy.logwarn("Starting position not recorded. Skipping return to start.")
            return
        
        rospy.loginfo("Returning to start position...")
        
        # Turn 300 degrees in place (clockwise)
        self.turn_in_place(300)
        
        # Stop the robot after turning
        self.move_cmd.linear.x = 0
        self.move_cmd.angular.z = 0
        self.vel_pub.publish(self.move_cmd)
        rospy.sleep(1)  # Wait for a moment after turning

        # Return to the starting position by moving forward
        start_x, start_z = self.starting_position
        start_time = rospy.Time.now().to_sec()
        while not rospy.is_shutdown():
            self.move_cmd.linear.x = start_x
            self.move_cmd.angular.z = start_z
            self.vel_pub.publish(self.move_cmd)
            self.rate.sleep()
            # Check distance covered to determine when to stop
            if rospy.Time.now().to_sec() - start_time > self.goal_distance / self.goal_speed:
                break

        # Stop the robot when it reaches the start position
        self.move_cmd.linear.x = 0
        self.move_cmd.angular.z = 0
        self.vel_pub.publish(self.move_cmd)
        rospy.loginfo("Returned to start position!")
        
        # Reset starting position after returning
        self.starting_position = None

    def run(self):
        try:
            # Wait for the scan callback to get initial sensor data
            rospy.sleep(1)
            
            while not rospy.is_shutdown():
                # Move the robot towards the goal while avoiding obstacles
                self.move_robot()
                
                # Record the starting position once when goal is first reached
                if self.goal_reached and not self.starting_position:
                    self.record_starting_position()
                    
                # Return to the start position if goal is reached
                if self.goal_reached and self.starting_position:
                    self.return_to_start()
                    
                    # Reset goal_reached flag to repeat the task
                    self.goal_reached = False
        
        except rospy.ROSInterruptException:
            pass

if __name__ == '__main__':
    robot = AutonomousRobot()
    robot.run()
