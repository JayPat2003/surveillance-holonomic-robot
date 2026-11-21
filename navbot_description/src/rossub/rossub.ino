#include <ros.h>
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
  int x_velocity = msg.linear.x * 2000; // Scaling linear velocity for steps
  
  // Control stepper1 and stepper2 based on x_velocity
  stepper1.move(x_velocity);
  stepper2.move(x_velocity);
  stepper3.move(-x_velocity);
  stepper4.move(-x_velocity);

}

ros::Subscriber<geometry_msgs::Twist> sub("cmd_vel", cmd_velCallback);

void setup() {
  pinMode(dirPin1, OUTPUT);
  pinMode(stepPin1, OUTPUT);
  pinMode(dirPin2, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin3, OUTPUT);
  pinMode(stepPin3, OUTPUT);
  pinMode(dirPin4, OUTPUT);
  pinMode(stepPin4, OUTPUT);
  
  nh.initNode();
  nh.subscribe(sub);

  stepper1.setMaxSpeed(9000);
  stepper1.setAcceleration(9000);

  stepper2.setMaxSpeed(11000);
  stepper2.setAcceleration(11000);

  stepper3.setMaxSpeed(11000);
  stepper3.setAcceleration(11000);

  stepper4.setMaxSpeed(11000);
  stepper4.setAcceleration(11000);
}

void loop() {
  nh.spinOnce();
  stepper1.run();
  stepper2.run();
  stepper3.run();
  stepper4.run();
}
