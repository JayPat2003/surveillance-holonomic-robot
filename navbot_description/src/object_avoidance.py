#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObjectAvoidance:
    def __init__(self):
        rospy.init_node('object_avoidance', anonymous=True)

        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        self.twist = Twist()

    def scan_callback(self, data):
        range_ahead = min(min(data.ranges[0:30]), min(data.ranges[330:359])) # Checking front ranges

        if range_ahead < 1.0:  # if distance to obstacle is less than 1 meter
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.5  # turn left
        else:
            self.twist.linear.x = 0.5
            self.twist.angular.z = 0.0  # go forward

        self.cmd_pub.publish(self.twist)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        node = ObjectAvoidance()
        node.run()
    except rospy.ROSInterruptException:
        pass
