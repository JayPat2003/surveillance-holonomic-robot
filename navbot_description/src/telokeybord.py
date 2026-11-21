#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

class ArduinoControl:
    def __init__(self):
        rospy.init_node('arduino_control')

        rospy.Subscriber('cmd_vel', Twist, self.cmd_vel_callback)

        self.rate = rospy.Rate(10)  # 10 Hz

    def cmd_vel_callback(self, msg):
        x_linear = msg.linear.x
        z_angular = msg.angular.z

        # Publish scaled velocities to Arduino
        # You might need to adjust the scaling factor according to your system
        # Publish scaled velocities to Arduino
        # You might need to adjust the scaling factor according to your system
        self.publish_to_arduino(x_linear, z_angular)

    def publish_to_arduino(self, x_linear, z_angular):
        # Process linear and angular velocities to send to Arduino
        # Scaling linear and angular velocities for your system
        x_steps = int(x_linear * 1000)  # Scaling linear velocity for steps
        z_steps = int(z_angular * 1000)  # Scaling angular velocity for steps

        # Code to publish to Arduino, you might need to use rospy.Publisher to do this

    def run(self):
        while not rospy.is_shutdown():
            self.rate.sleep()

if __name__ == '__main__':
    try:
        controller = ArduinoControl()
        controller.run()
    except rospy.ROSInterruptException:
        pass
