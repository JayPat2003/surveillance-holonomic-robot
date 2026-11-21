#!/usr/bin/env python3


import rospy
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
import paho.mqtt.client as mqtt

# Define marker positions
marker_positions = {
    "button1": (1.0, 2.0, 0.0),
    "button2": (3.0, 4.0, 0.0),
    "button3": (5.0, 6.0, 0.0)
}

def move_to_goal(x, y):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    wait = client.wait_for_result()

    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

def on_message(client, userdata, msg):
    button = msg.topic
    rospy.loginfo("{} pressed".format(button))
    if button in marker_positions:
        x, y, _ = marker_positions[button]
        rospy.loginfo("Moving to {} position: ({}, {})".format(button, x, y))
        move_to_goal(x, y)

def main():
    rospy.init_node('button_listener')

    client = mqtt.Client()
    client.on_message = on_message
    client.connect("mqtt_broker_ip", 1883) # Connect to MQTT broker
    client.subscribe("button1")
    client.subscribe("button2")
    client.subscribe("button3")

    client.loop_forever()

if __name__ == '__main__':
    main()
