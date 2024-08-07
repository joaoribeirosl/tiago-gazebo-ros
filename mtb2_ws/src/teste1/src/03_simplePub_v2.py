!# /usr/bin/python3

import rospy
import time

#importação da biblioteca de mensagens padronizadas
from geometry_msgs.msg import Twist

# Criação do nó com o nome simple_publisher alterado para publisher_turtle,
# Posteriormente alterado para publisher_tiago
rospy.init_node('publisher_turtle')

# Criação do publisher no topic counter de uma mensagem de tipo FLoat32MultiArray
# para /turtle/cmd_vel

pub = rospy.


while not rospy.is_shutdown():
# Move straight
	if count % 2 == 0:
		variableToPublish.linear.x = 0.5
y = 0.0
z = 0.0
angular.x = 0.0
y = 0.0
z = 0.0
# rotate
	else:
		variableToPublish.linear.x = 0
.y = 0.0
.z =0.0
angular.x = 0.0
.y = 0.0
z = 0.5

# Publicação da mensagem no tópico
	pub.publish(variableToPublish)
	count += 1
