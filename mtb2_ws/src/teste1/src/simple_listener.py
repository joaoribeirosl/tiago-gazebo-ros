#! usr/bin/python3

import rospy
import time

#importação da biblioteca de mensagens padrôes

from std_msgs.msg import Int32

# Criação do nó com o nome simple_publisher
rospy.init_node('simple_publisher_ v2')

# Criação do publisher no topic counter de um mensagem de tipo  Int32

pub = rosp.Publisher('counter_v2", Int32, queue size = 1

rate = rospy.Rate(2)

variableToPubliser = Int32

count = 0
