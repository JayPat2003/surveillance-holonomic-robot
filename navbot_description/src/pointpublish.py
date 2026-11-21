#!/usr/bin/env python

import rospy
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from geometry_msgs.msg import Point

def create_marker(marker_id, x, y, z, r, g, b):
    marker = Marker()
    marker.header.frame_id = "map"
    marker.header.stamp = rospy.Time.now()
    marker.ns = "basic_shapes"
    marker.id = marker_id
    marker.type = Marker.CUBE  # You can change the shape here (e.g., SPHERE, ARROW, CYLINDER)
    marker.action = Marker.ADD

    # Set the pose of the marker
    marker.pose.position.x = x
    marker.pose.position.y = y
    marker.pose.position.z = z
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0

    # Set the scale of the marker
    marker.scale.x = 1.0
    marker.scale.y = 1.0
    marker.scale.z = 1.0

    # Set the color
    marker.color.r = r
    marker.color.g = g
    marker.color.b = b
    marker.color.a = 1.0

    return marker

def main():
    rospy.init_node('markers_node', anonymous=True)
    marker_pub = rospy.Publisher('visualization_marker_array', MarkerArray, queue_size=10)

    marker_array = MarkerArray()

    # Create three markers at different locations with different colors
    marker1 = create_marker(0, 1.0, 2.0, 0.0, 1.0, 0.0, 0.0)  # Red cube at (1, 2, 0)
    marker2 = create_marker(1, 3.0, 4.0, 0.0, 0.0, 1.0, 0.0)  # Green cube at (3, 4, 0)
    marker3 = create_marker(2, 5.0, 6.0, 0.0, 0.0, 0.0, 1.0)  # Blue cube at (5, 6, 0)

    marker_array.markers.append(marker1)
    marker_array.markers.append(marker2)
    marker_array.markers.append(marker3)

    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        marker_pub.publish(marker_array)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
