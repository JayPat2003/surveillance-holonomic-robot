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
  double linear_x = msg.linear.x;
  double angular_z = msg.angular.z;

  double forward_velocity = linear_x;
  double backward_velocity = -linear_x;
  double rotation_velocity = angular_z;

  int forward_steps = forward_velocity * 1000; // Scaling forward velocity for steps
  int backward_steps = backward_velocity * 1000; // Scaling backward velocity for steps
  int rotation_steps = rotation_velocity * 1000; // Scaling angular velocity for steps

  // Control forward and backward movement of the robot
  stepper1.move(forward_steps);
  stepper2.move(forward_steps);
  stepper3.move(backward_steps);
  stepper4.move(backward_steps);
  
  // Control rotation
  stepper3.move(rotation_steps);
  stepper4.move(rotation_steps);
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
