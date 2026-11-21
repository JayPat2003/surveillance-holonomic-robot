#!/usr/bin/env python

import rospy
from std_msgs.msg import String

class TriggerListener:
    def __init__(self):
        rospy.init_node('trigger_listener', anonymous=True)
        rospy.Subscriber('trigger', String, self.callback)
        rospy.spin()

    def callback(self, data):
        if data.data == 'StartMovement1':
            rospy.loginfo("Received trigger to start movement")
            # Call your function to start movement here

if __name__ == '__main__':
    try:
        TriggerListener()
    except rospy.ROSInterruptException:
        pass
