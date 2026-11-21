#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PointStamped
from interactive_markers.interactive_marker_server import InteractiveMarkerServer

class ClickCoordinates():
    def __init__(self):
        rospy.init_node('click_coordinates_node')
        self.server = InteractiveMarkerServer("map")
        rospy.Subscriber("/clicked_point", PointStamped, self.clicked_point_callback)

    def clicked_point_callback(self, msg):
        x = msg.point.x
        y = msg.point.y
        z = msg.point.z
        rospy.loginfo("Clicked point coordinates - x: {}, y: {}, z: {}".format(x, y, z))

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    click_coordinates = ClickCoordinates()
    click_coordinates.run()
