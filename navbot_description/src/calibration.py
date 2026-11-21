#!/usr/bin/env python3

import smbus
import time
import numpy as np

# MPU6050 Registers and their Address
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

# Initialize the MPU6050
def MPU_Init():
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 0x01)
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    bus.write_byte_data(Device_Address, CONFIG, 0)
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_Address, ACCEL_CONFIG, 0)
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    value = ((high << 8) | low)
    if value > 32768:
        value = value - 65536
    return value

# Calibration function
def calibrate(num_samples=1000):
    acc_x_bias, acc_y_bias, acc_z_bias = 0, 0, 0
    gyro_x_bias, gyro_y_bias, gyro_z_bias = 0, 0, 0
    
    for i in range(num_samples):
        acc_x_bias += read_raw_data(ACCEL_XOUT_H)
        acc_y_bias += read_raw_data(ACCEL_YOUT_H)
        acc_z_bias += read_raw_data(ACCEL_ZOUT_H)
        gyro_x_bias += read_raw_data(GYRO_XOUT_H)
        gyro_y_bias += read_raw_data(GYRO_YOUT_H)
        gyro_z_bias += read_raw_data(GYRO_ZOUT_H)
        time.sleep(0.01)
    
    acc_x_bias /= num_samples
    acc_y_bias /= num_samples
    acc_z_bias /= num_samples
    gyro_x_bias /= num_samples
    gyro_y_bias /= num_samples
    gyro_z_bias /= num_samples

    acc_z_bias -= 16384  # Adjust for gravity
    
    return acc_x_bias, acc_y_bias, acc_z_bias, gyro_x_bias, gyro_y_bias, gyro_z_bias

bus = smbus.SMBus(1)  # or smbus.SMBus(0) depending on your setup
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

print("Calibrating MPU6050... Please keep the sensor stationary.")
acc_x_bias, acc_y_bias, acc_z_bias, gyro_x_bias, gyro_y_bias, gyro_z_bias = calibrate()
print(f"Calibration Complete.\nAccelerometer Bias: X={acc_x_bias} Y={acc_y_bias} Z={acc_z_bias}\nGyroscope Bias: X={gyro_x_bias} Y={gyro_y_bias} Z={gyro_z_bias}")

print("Reading Data of Gyroscope and Accelerometer")

while True:
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)
    
    Ax = (acc_x - acc_x_bias) / 16384.0
    Ay = (acc_y - acc_y_bias) / 16384.0
    Az = (acc_z - acc_z_bias) / 16384.0
    
    Gx = (gyro_x - gyro_x_bias) / 131
