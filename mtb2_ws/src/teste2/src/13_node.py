#! /usr/bin/python

import rospy
from sensor_msgs.msg import LaserScan


class LaserRangeSubscriber():
    def __init__(self) -> None:
        self.sub = rospy.Subscriber('/scan_raw', LaserScan, self.callback, queue_size=1)
        self.anglemax = 0
        self.anglemin = 0
        self.angleincrement = 0
        self.numraios = 0
        self.ranges = []
        self.angle = []

        self.x = []
        self.y = []

    
    def callback(self, msg):
        self.anglemin = msg.angle_min
        self.anglemax = msg.angle_max
        self.angleincrement = msg.angle_increment
        self.ranges = msg.ranges
        self.numraios = 1 + (self.anglemax - self.anglemin) / self.angleincrement
        print(msg.ranges)

    def minrangefind(self):
        #Desmontar a mensagem em angle_min, _max, _increment, e a lista ranges[]
        tabela_distancias = self.ranges
        #  minimum = min(tabela_distancias)
        # indices = [i for i, v in enumerate(tabela_distancias) if v == minimum and v > 0.15]

        v_min = 1000
        for r in tabela_distancias: # prune distances from laser to robot body!!
            if r < v_min and r > 0.15:
                v_min = r

        return  v_min

#main
if __name__ == "__main__":
    # Define node
    rospy.init_node('TIAGo_Laserange_node')
    # Cria um objeto da classe QuatEuler e roda a função
    lasersensor = LaserRangeSubscriber()
    # Enquanto ROS está rodando
    #rospy.spin()
    while not rospy.is_shutdown():
        dist1 = lasersensor.minrangefind()
        print(dist1)
