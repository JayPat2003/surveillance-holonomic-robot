#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2

class RobotController:
    def __init__(self):
        rospy.init_node('robot_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/odom', Odometry, self.update_pose)
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        
        rospy.loginfo("Waiting for move_base action server...")
        self.client.wait_for_server()
        rospy.loginfo("Connected to move_base action server")

        self.pose = None
        self.rate = rospy.Rate(10) # 10 Hz

    def update_pose(self, data):
        self.pose = data.pose.pose

    def get_orientation(self):
        orientation = self.pose.orientation
        orientation_list = [orientation.x, orientation.y, orientation.z, orientation.w]
        _, _, yaw = euler_from_quaternion(orientation_list)
        return yaw

    def move_to_goal(self, goal_x, goal_y):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = goal_x
        goal.target_pose.pose.position.y = goal_y
        goal.target_pose.pose.orientation.w = 1.0

        rospy.loginfo("Sending goal location ...")
        self.client.send_goal(goal)

        self.client.wait_for_result()

        if self.client.get_state() == actionlib.GoalStatus.SUCCEEDED:
            rospy.loginfo("You have reached the destination")
        else:
            rospy.loginfo("The robot failed to reach the destination")

    def stop_robot(self):
        twist = Twist()
        self.velocity_publisher.publish(twist)

if __name__ == '__main__':
    try:
        robot = RobotController()
        goal_x = -2.19637513161 # Specify your goal x coordinate here
        goal_y = -0.410311222076 # Specify your goal y coordinate here
        robot.move_to_goal(goal_x, goal_y)
    except rospy.ROSInterruptException:
        pass
