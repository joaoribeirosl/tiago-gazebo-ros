#! /usr/bin/python
from math import sin, cos
import rospy
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker


class MarkerSubscriber():
    def __init__(self) -> None:
        self.sub = rospy.Subscriber('/scan_raw', LaserScan, self.callback, queue_size=1)
        self.pub = rospy.Publisher('myPoint', Marker , queue_size =1)
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
        #print(msg.ranges)
        self.minrangefind()

    def minrangefind(self):
        #Desmontar a mensagem em angle_min, _max, _increment, e a lista ranges[]
        tabela_distancias = self.ranges
        #  minimum = min(tabela_distancias)
        # indices = [i for i, v in enumerate(tabela_distancias) if v == minimum and v > 0.15]
        rangemax = 1000
        id_max = 0
        idx = 0
        v_min = 1000
        for r in tabela_distancias: # prune distances from laser to robot body!!
            if r < v_min and r > 0.15:
                v_min = r
                id_max = idx
            idx += 1
        angle_max = self.anglemin + id_max * self.angleincrement
        x = v_min * cos(angle_max)
        y = v_min * sin(angle_max)
        

        marker = Marker()
        marker.header.frame_id = "base_laser_link"
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = 0.05
        marker.scale.y = 0.05
        marker.scale.z = 0.05
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 1.0
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = x
        marker.pose.position.y = y
        marker.pose.position.z = 0

        self.pub.publish(marker)
        # return marker

#main
if __name__ == "__main__":
    # Define node
    rospy.init_node('Marker_node')
    # Cria um objeto da classe QuatEuler e roda a função
    lasersensor = MarkerSubscriber()
    # Enquanto ROS está rodando
    rospy.spin()
    #while not rospy.is_shutdown():
    #    dist1 = lasersensor.minrangefind()
    #    print(dist1)
