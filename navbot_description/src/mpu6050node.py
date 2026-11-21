#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
from smbus import SMBus
import tf2_ros
from geometry_msgs.msg import TransformStamped

# MPU6050 I2C address
MPU6050_ADDR = 0x68

# Initialize I2C bus
bus = SMBus(1)

# TF broadcaster
tf_broadcaster = tf2_ros.TransformBroadcaster()

# Function to read raw accelerometer and gyroscope data
def read_raw_data(addr, reg):
    high = bus.read_byte_data(addr, reg)
    low = bus.read_byte_data(addr, reg + 1)
    value = (high << 8) | low
    if value > 32767:
        value -= 65536
    return value

def imu_publisher():
    # Initialize ROS node
    rospy.init_node('imu_publisher', anonymous=True)
    imu_pub = rospy.Publisher('imu/data', Imu, queue_size=10)
    rate = rospy.Rate(10)  # 10Hz

    while not rospy.is_shutdown():
        imu_msg = Imu()

        # Read accelerometer data
        accel_x = read_raw_data(MPU6050_ADDR, 0x3B)
        accel_y = read_raw_data(MPU6050_ADDR, 0x3D)
        accel_z = read_raw_data(MPU6050_ADDR, 0x3F)

        # Read gyroscope data
        gyro_x = read_raw_data(MPU6050_ADDR, 0x43)
        gyro_y = read_raw_data(MPU6050_ADDR, 0x45)
        gyro_z = read_raw_data(MPU6050_ADDR, 0x47)

        # Populate IMU message
        imu_msg.linear_acceleration.x = accel_x / 16384.0  # Sensitivity scale factor for accelerometer
        imu_msg.linear_acceleration.y = accel_y / 16384.0
        imu_msg.linear_acceleration.z = accel_z / 16384.0
        imu_msg.angular_velocity.x = gyro_x / 131.0  # Sensitivity scale factor for gyroscope
        imu_msg.angular_velocity.y = gyro_y / 131.0
        imu_msg.angular_velocity.z = gyro_z / 131.0

        # Publish the IMU message
        imu_pub.publish(imu_msg)

        # Broadcast TF transform
        transformStamped = TransformStamped()
        transformStamped.header.stamp = rospy.Time.now()
        transformStamped.header.frame_id = "base_link"
        transformStamped.child_frame_id = "imu_link"
        transformStamped.transform.translation.x = 0.0
        transformStamped.transform.translation.y = 0.0
        transformStamped.transform.translation.z = 0.0
        transformStamped.transform.rotation.x = 0.0
        transformStamped.transform.rotation.y = 0.0
        transformStamped.transform.rotation.z = 0.0
        transformStamped.transform.rotation.w = 1.0
        tf_broadcaster.sendTransform(transformStamped)

        rate.sleep()

if __name__ == '__main__':
    try:
        imu_publisher()
    except rospy.ROSInterruptException:
        pass
