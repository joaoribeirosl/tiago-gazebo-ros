#! /usr/bin/python3

import rospy
from geometry_msgs.msg import Twist

rospy.init_node('simple_publisher')

# Criação do publisher no topic /mobile_base_controller/cmd_vel de uma mensagem de tipo Twist
pub = rospy.Publisher('/mobile_base_controller/cmd_vel', Twist, queue_size =1)

cmd = Twist()

rate = rospy.Rate(1)
count = 0
while not rospy.is_shutdown():
	if count % 2 == 0:
		cmd.linear.x = 1
		cmd.angular.z = 0
	else:
		cmd.linear.x = 0
		cmd.angular.z = 1
	pub.publish(cmd)
	count += 1
	rate.sleep()

