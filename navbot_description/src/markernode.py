#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import subprocess

mqtt_broker = "192.168.46.26"  # IP address of your MQTT broker
mqtt_topics = {
    "button1_pressed": (1.0, 2.0, 0.0),
    "button2_pressed": (3.0, 4.0, 0.0),
    "button3_pressed": (5.0, 6.0, 0.0)
}

current_marker_position = None

def on_mqtt_message(topic, payload):
    global current_marker_position
    if topic in mqtt_topics:
        current_marker_position = mqtt_topics[topic]
        rospy.loginfo("Moving to marker position: %s", str(current_marker_position))
        move_robot(current_marker_position)

def move_robot(position):
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10Hz

    while not rospy.is_shutdown():
        # Example: move straight towards the position (you may need to adjust this logic)
        twist_msg = Twist()
        twist_msg.linear.x = 0.1  # adjust linear velocity as needed
        twist_msg.angular.z = 0.0
        pub.publish(twist_msg)
        rate.sleep()

def main():
    rospy.init_node('move_to_marker_node', anonymous=True)
    
    rospy.loginfo("ROS node initialized, waiting for button presses...")

    # Start MQTT subscriber in a separate process
    sub_process = subprocess.Popen(['mosquitto_sub', '-h', mqtt_broker, '-t', 'button1_pressed', 'button2_pressed', 'button3_pressed', '-u', 'your_username', '-P', 'your_password', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while not rospy.is_shutdown():
        # Read MQTT messages from subprocess stdout
        output = sub_process.stdout.readline()
        if output == b'':  # Process has terminated
            break
        rospy.loginfo("Received MQTT message: %s", output)
        
        # Parse the topic and payload from the MQTT message
        parts = output.strip().split()
        if len(parts) >= 2:
            topic = parts[0].decode('utf-8')
            payload = parts[1].decode('utf-8')
            on_mqtt_message(topic, payload)

    sub_process.kill()  # Kill the subprocess when ROS node shuts down

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
