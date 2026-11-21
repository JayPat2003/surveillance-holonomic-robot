#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32MultiArray

class RobotControl:
    def __init__(self):
        rospy.init_node('robot_control_node', anonymous=True)
        self.motor_pub = rospy.Publisher('motor_commands', Int32MultiArray, queue_size=10)
        self.vel_sub = rospy.Subscriber('/cmd_vel', Twist, self.velocity_callback)
        self.vel_msg = Twist()

    def velocity_callback(self, data):
        # Convert linear and angular velocity to motor commands
        # Example: map linear x velocity to motor speed
        motor_speed = int(data.linear.x * 100)  # Adjust scaling as needed
        # Example: map angular z velocity to steering or differential drive
        steering_angle = int(data.angular.z * 100)  # Adjust scaling as needed

        # Create Int32MultiArray message to send to motors
        motor_command = Int32MultiArray(data=[motor_speed, steering_angle, 0, 0])  # Adjust for your setup
        self.motor_pub.publish(motor_command)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        robot_controller = RobotControl()
        robot_controller.run()
    except rospy.ROSInterruptException:
        pass
