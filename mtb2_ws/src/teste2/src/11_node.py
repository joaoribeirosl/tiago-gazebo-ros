#! /usr/bin/python

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler

class QuatEuler():
    def __init__(self) -> None:
        self.sub = rospy.Subscriber('/mobile_base_controller/odom',
                                    Odometry, self.callback, queue_size=1)
    
    def callback(self, msg):
        qtn = msg.pose.pose.orientation
        qtn_list = [qtn.x, qtn.y, qtn.z, qtn.w]
        (roll, pitch, yaw) = euler_from_quaternion(qtn_list)
        print(roll, pitch, yaw)

#main
if __name__ == "__main__":
    # Define node
    rospy.init_node('TIAGo_odem_node')
    # Cria um objeto da classe QuatEuler e roda a função
    quaternion_para_euler = QuatEuler()
    # Enquanto ROS está rodando
    rospy.spin()
