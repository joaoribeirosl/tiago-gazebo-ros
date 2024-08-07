#! /usr/bin/python

import rospy
from sensor_msgs.msg import LaserScan


class LaserRangeSubscriber():
    def __init__(self) -> None:
        self.sub = rospy.Subscriber('/scan_raw', LaserScan, self.callback, queue_size=1)
    
    def callback(self, msg):
        print(msg.ranges)

#main
if __name__ == "__main__":
    # Define node
    rospy.init_node('TIAGo_Laserange_node')
    # Cria um objeto da classe QuatEuler e roda a função
    lasersensor = LaserRangeSubscriber()
    # Enquanto ROS está rodando
    rospy.spin()
