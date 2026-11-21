#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import math

# Define the goal coordinates
goal_x = 1.0
goal_y = 2.0
goal_tolerance = 0.1  # Tolerance for reaching the goal
linear_speed = 0.2  # Linear speed (m/s)
angular_speed = 0.5  # Angular speed (rad/s)

current_x = 0.0
current_y = 0.0
current_yaw = 0.0

def odom_callback(data):
    global current_x, current_y, current_yaw
    current_x = data.pose.pose.position.x
    current_y = data.pose.pose.position.y
    orientation_q = data.pose.pose.orientation
    (roll, pitch, current_yaw) = euler_from_quaternion([orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w])

def euler_from_quaternion(quat):
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    """
    x, y, z, w = quat
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(t3, t4)

    return roll, pitch, yaw

def button_callback(msg):
    if msg.data == "pressed":
        send_velocity_commands()

def send_velocity_commands():
    rospy.loginfo("Sending velocity commands to move to goal")
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/odom', Odometry, odom_callback)
    rate = rospy.Rate(10)  # 10 Hz

    while not rospy.is_shutdown():
        # Calculate distance and angle to the goal
        distance = math.sqrt((goal_x - current_x)**2 + (goal_y - current_y)**2)
        angle_to_goal = math.atan2(goal_y - current_y, goal_x - current_x)

        # Check if the goal is reached
        if distance < goal_tolerance:
            rospy.loginfo("Goal reached")
            break

        # Calculate velocity commands
        twist = Twist()
        if abs(angle_to_goal - current_yaw) > 0.1:
            twist.angular.z = angular_speed if angle_to_goal > current_yaw else -angular_speed
        else:
            twist.linear.x = linear_speed

        # Publish velocity commands
        pub.publish(twist)
        rate.sleep()

    # Stop the robot
    twist = Twist()
    pub.publish(twist)

def listener():
    rospy.init_node('cmd_vel_goal_node', anonymous=True)
    rospy.Subscriber('/arduino_signal', String, button_callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
