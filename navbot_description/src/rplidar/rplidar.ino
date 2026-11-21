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
  int x_velocity = msg.linear.x * 10000; // Scaling linear velocity for steps
  //int z_rotation = msg.angular.z * 1000; // Scaling angular velocity for steps
  
  // Here you can map linear and angular velocities to the movements of your motors
  // You can control each motor based on the values of x_velocity and z_rotation
  
  // For example, you can control stepper1 and stepper2 based on x_velocity
  stepper1.move(x_velocity);
  stepper2.move(x_velocity);
  
  // For example, you can control stepper3 and stepper4 based on z_rotation
  stepper3.move(x_velocity);
  stepper4.move(x_velocity);
}

ros::Subscriber<geometry_msgs::Twist> sub("cmd_vel", cmd_velCallback);

void setup() {
  nh.initNode();
  nh.subscribe(sub);

  stepper1.setMaxSpeed(90000);
  stepper1.setAcceleration(90000);

  stepper2.setMaxSpeed(90000);
  stepper2.setAcceleration(90000);

  stepper3.setMaxSpeed(90000);
  stepper3.setAcceleration(90000);

  stepper4.setMaxSpeed(90000);
  stepper4.setAcceleration(90000);
}

void loop() {
  nh.spinOnce();
  stepper1.run();
  stepper2.run();
  stepper3.run();
  stepper4.run();
}
