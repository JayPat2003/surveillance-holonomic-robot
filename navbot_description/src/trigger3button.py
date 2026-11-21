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
            rospy.loginfo("Received trigger to start movement from Location 1")
            # Call function or perform action for Location 1
        elif data.data == 'StartMovement2':
            rospy.loginfo("Received trigger to start movement from Location 2")
            # Call function or perform action for Location 2
        elif data.data == 'StartMovement3':
            rospy.loginfo("Received trigger to start movement from Location 3")
            # Call function or perform action for Location 3

if __name__ == '__main__':
    try:
        TriggerListener()
    except rospy.ROSInterruptException:
        pass
