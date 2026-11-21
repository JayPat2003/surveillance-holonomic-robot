#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from robot_controller import RobotController  # Assuming RobotController is in a file named robot_controller.py

class TriggerListener:
    def __init__(self):
        rospy.init_node('trigger_listener', anonymous=True)
        rospy.Subscriber('trigger', String, self.callback)
        self.robot_controller = RobotController()
        rospy.spin()

    def callback(self, data):
        if data.data == 'StartMovement2':
            rospy.loginfo("Received trigger to start movement")
            goal_x = -1.99793934822  # Specify your goal x coordinate here
            goal_y = -0.357921123505 # Specify your goal y coordinate here
            self.robot_controller.move_to_goal(goal_x, goal_y)

if __name__ == '__main__':
    try:
        TriggerListener()
    except rospy.ROSInterruptException:
        pass
