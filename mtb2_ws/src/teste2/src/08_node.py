#! /usr/bin/python

import rospy
import time
from std_msgs.msg import Int32

# Define a funçao chamada pelo subscriber
# Essa função é padrão no ROS
# Sempre será esse nome e sempre terá um argumento
def callback(msg):
	print(msg.data)
	time.sleep(1) # simular algum processamento

rospy.init_node('simple_subscriber')

# define o novo subscriber
rospy.Subscriber('counter', Int32, callback, queue_size=1)

# Equivalente a um while infinito para não fechar o programa
rospy.spin()
