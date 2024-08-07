#! /usr/bin/python

import rospy

rospy.init_node('hello_world')

# Definição da frequência do la ̧co while
rate = rospy.Rate(2)

count = 0
# Em loop até a detecção de Ctrl +c
while not rospy.is_shutdown() :
	print (" Hello world number {}".format ( count ) )
	count += 1

	# Esperar pelo fim do tempo do la̧co
	rate.sleep()
