#! /usr/bin/python

import rospy
from nav_msgs.msg import Odometry

#Definição da classe
class Odometer():
    #Definindo o subscriber
    def __init__(self) -> None:
        self.sub = rospy.Subscriber('/mobile_base_controller/odom', Odometry, self.callback, queue_size=1)
    
    def callback(self, msg):
        print(msg.pose)

#main 
if __name__ == "__main__":
    #Definir o nó (node)
    rospy.init_node('TIAGo_odem_node')

    #criar um objeto da classe Odometer e rodar a função
    odometro = Odometer()

    #Enquanto ROS está rodando
    rospy.spin()
