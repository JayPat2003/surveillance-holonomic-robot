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
  
  // Control each motor based on the sign of x_velocity and z_rotation
  stepper1.move(-x_velocity + z_rotation);
  stepper2.move(-x_velocity + z_rotation);
  stepper3.move(x_velocity - z_rotation);
  stepper4.move(x_velocity - z_rotation);
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
