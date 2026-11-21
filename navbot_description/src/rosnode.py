#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def control_motors():
    rospy.init_node('motor_controller', anonymous=True)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        twist = Twist()
        # Here you can set the linear and angular velocities
        twist.linear.x = 0.1  # Example linear velocity
        twist.angular.z = 0.1  # Example angular velocity
        pub.publish(twist)
        rate.sleep()

if __name__ == '__main__':
    try:
        control_motors()
    except rospy.ROSInterruptException:
        pass
