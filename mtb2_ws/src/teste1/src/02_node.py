#! /usr/bin/python

import rospy

rospy.init_node('hello world')

# Definição da frequência do laço while
rate = rospy.Rate(2)

count = 0

# Em loop até a detecção de Ctrl+C
while not rospy.is_shutdown():
	print("Hello World number {}".format(count))
	count += 1

	# Esperar pelo fim do tempo do laço
	rate.sleep()
