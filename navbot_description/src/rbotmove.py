import paho.mqtt.client as mqtt
import rospy
from std_msgs.msg import String

# MQTT settings
mqtt_broker = "your-MQTT"
mqtt_port = 1883
mqtt_topic = "robot/start"

# ROS settings
ros_topic = "/robot/command"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print(f"Message received: {msg.payload.decode()}")
    if msg.payload.decode() == "start":
        pub.publish("start")

if __name__ == "__main__":
    rospy.init_node("mqtt_ros_bridge")
    pub = rospy.Publisher(ros_topic, String, queue_size=10)
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_start()

    rospy.spin()
    client.loop_stop()
    client.disconnect()
