/*
 * Research prototype firmware — holonomic surveillance robot (Woxsen AI & Robotics Lab).
 * Subscribes to ROS /cmd_vel via rosserial and drives 4 steppers (AccelStepper).
 * Simplified differential-style mapping of linear.x / angular.z (not full Mecanum IK).
 * Not production / safety-certified control software.
 */
#include <ros.h>
#include <std_msgs/Int32.h>
#include <geometry_msgs/Twist.h>
#include <AccelStepper.h>

#define dirPin1 2
#define stepPin1 3
#define dirPin2 4
#define stepPin2 5
#define dirPin3 6
#define stepPin3 7
#define dirPin4 8
#define stepPin4 9

#define motorInterfaceType 1

AccelStepper stepper1 = AccelStepper(motorInterfaceType, stepPin1, dirPin1);
AccelStepper stepper2 = AccelStepper(motorInterfaceType, stepPin2, dirPin2);
AccelStepper stepper3 = AccelStepper(motorInterfaceType, stepPin3, dirPin3);
AccelStepper stepper4 = AccelStepper(motorInterfaceType, stepPin4, dirPin4);

ros::NodeHandle nh;

void cmd_velCallback(const geometry_msgs::Twist& msg) {
  float x_velocity = msg.linear.x * 1000; // Scaling linear velocity for steps
  float z_rotation = msg.angular.z * 1000; // Scaling angular velocity for steps
  
  // Calculate the velocities for each wheel
  float v1 = x_velocity + z_rotation;
  float v2 = x_velocity - z_rotation;
  
  // Control the motors
  stepper1.move(-v1);
  stepper2.move(-v2);
  stepper3.move(v1);
  stepper4.move(v2);
}

ros::Subscriber<geometry_msgs::Twist> sub("cmd_vel", cmd_velCallback);

void setup() {
  nh.initNode();
  nh.subscribe(sub);

  stepper1.setMaxSpeed(9000);
  stepper1.setAcceleration(9000);

  stepper2.setMaxSpeed(9000);
  stepper2.setAcceleration(9000);

  stepper3.setMaxSpeed(9000);
  stepper3.setAcceleration(9000);

  stepper4.setMaxSpeed(9000);
  stepper4.setAcceleration(9000);
}

void loop() {
  nh.spinOnce();
  stepper1.run();
  stepper2.run();
  stepper3.run();
  stepper4.run();
}
