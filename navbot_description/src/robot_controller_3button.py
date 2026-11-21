#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2

class RobotController:
    def __init__(self):
        try:
            rospy.init_node('robot_controller', anonymous=True)
            self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
            self.pose_subscriber = rospy.Subscriber('/odom', Odometry, self.update_pose)
            self.trigger_subscriber = rospy.Subscriber('/trigger_event', String, self.trigger_callback)

            self.pose = None
            self.rate = rospy.Rate(10) # 10 Hz

            rospy.spin()
        except rospy.ROSInterruptException as e:
            rospy.logerr("ROS Interrupt Exception: %s", e)
        except Exception as ex:
            rospy.logerr("Exception occurred: %s", ex)

    def update_pose(self, data):
        self.pose = data.pose.pose

    def get_orientation(self):
        orientation = self.pose.orientation
        orientation_list = [orientation.x, orientation.y, orientation.z, orientation.w]
        _, _, yaw = euler_from_quaternion(orientation_list)
        return yaw

    def move_to_goal(self, goal_x, goal_y):
        try:
            while not rospy.is_shutdown():
                if self.pose is None:
                    continue
                
                current_x = self.pose.position.x
                current_y = self.pose.position.y
                goal_distance = ((goal_x - current_x)**2 + (goal_y - current_y)**2)**0.5

                if goal_distance < 0.1:
                    rospy.loginfo("Goal reached!")
                    self.stop_robot()
                    break

                desired_angle = atan2(goal_y - current_y, goal_x - current_x)
                current_angle = self.get_orientation()

                twist = Twist()
                if abs(desired_angle - current_angle) > 0.1:
                    twist.angular.z = 0.5 if desired_angle > current_angle else -0.5
                else:
                    twist.linear.x = 0.5

                self.velocity_publisher.publish(twist)
                self.rate.sleep()
        except rospy.ROSInterruptException as e:
            rospy.logerr("ROS Interrupt Exception: %s", e)
        except Exception as ex:
            rospy.logerr("Exception occurred: %s", ex)

    def stop_robot(self):
        twist = Twist()
        self.velocity_publisher.publish(twist)

    def trigger_callback(self, data):
        if data.data == 'StartMovement1':
            self.move_to_goal(2.0, 2.0)  # Goal for Location 1
        elif data.data == 'StartMovement2':
            self.move_to_goal(4.0, 4.0)  # Goal for Location 2
        elif data.data == 'StartMovement3':
            self.move_to_goal(6.0, 6.0)  # Goal for Location 3

if __name__ == '__main__':
    RobotController()
