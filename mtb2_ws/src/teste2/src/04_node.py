#! /usr/bin/python

import rospy
# Importaço da biblioteca de mensagens de geometria
from geometry_msgs.msg import Twist

rospy.init_node('simple_publisher')

# Criação do publisher no topic /turtle/cmd_vel de uma mensagem de tipo Twist
pub = rospy.Publisher('/turtle1/cmd_vel', Twist , queue_size =1)

cmd = Twist()
rate = rospy.Rate(1)

count = 0
while not rospy.is_shutdown():
# Move straight
	if count % 2 == 0:
		cmd.linear.x = 1.0
		cmd.linear.y = 0.0
		cmd.linear.z = 0.0
		cmd.angular.x = 0.0
		cmd.angular.y = 0.0
		cmd.angular.z = 0.0
	# rotate
	else :
		cmd.linear.x = 0.0
		cmd.linear.y = 0.0
		cmd.linear.z = 0.0
		cmd.angular.x = 0.0
		cmd.angular.y = 0.0
		cmd.angular.z = 1.0
	pub.publish(cmd)
	count += 1
	rate.sleep()
