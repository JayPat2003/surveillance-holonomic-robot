#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import socket

def handle_client(client_socket, pub1, pub2, pub3):
    try:
        request = client_socket.recv(1024)
        rospy.loginfo("Received: %s" % request)
        if request.strip() == b"START1":
            pub1.publish("START")
        elif request.strip() == b"START2":
            pub2.publish("START")
        elif request.strip() == b"START3":
            pub3.publish("START")
    except socket.error as e:
        rospy.logerr("Socket error: %s" % str(e))
    finally:
        client_socket.close()

def main():
    rospy.init_node('arduino_server')
    pub1 = rospy.Publisher('button_topic_robot1', String, queue_size=10)
    pub2 = rospy.Publisher('button_topic_robot2', String, queue_size=10)
    pub3 = rospy.Publisher('button_topic_robot3', String, queue_size=10)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8080))  # Change to port 8080
    server.listen(50)
    server.settimeout(1.0)  # Set timeout to 1 second
    
    rospy.loginfo("Server started, waiting for connections on port 8080...")
    
    while not rospy.is_shutdown():
        try:
            client_socket, addr = server.accept()
            rospy.loginfo("Accepted connection from: %s" % str(addr))
            handle_client(client_socket, pub1, pub2, pub3)
        except socket.timeout:
            # Handle the timeout - this is expected during idle periods
            continue
        except socket.error as e:
            rospy.logerr("Socket error: %s" % str(e))

if __name__ == "__main__":
    main()
