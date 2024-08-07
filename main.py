#! /usr/bin/python

import rospy
# from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist

class myRobot():

    def __init__(self):    
        # Subscriber odometria
        # Subscriber laser
        # Client Service camera
        # Publisher base
        self.base_pub = rospy.Publisher('/mobile_base_controller/cmd_vel', Twist, queue_size = 1) 
        # Publisher cabeca
    
    def callback_odometria(self, msg):
        print('callback odometria')
        # qtn = msg.pose.pose.orientation
        # qtn_list = [qtn.x, qtn.y, qtn.z,qtn.w]
        # (roll, pitch, yaw) = euler_from_quaternion(qtn_list)
        # print (roll, pitch, yaw)

    def callback_laser(self, msg):
        print('callback laser')
        print(msg.ranges)

    def move_staright(self):
        print('move straight')
        cmd = Twist()
        cmd.linear.x = 1
        self.base_pub.publish(cmd)
            

    def turn(self, sens):
        print('turn')
        # error = ...
        # while(abs(error) < value):

    def decision(self):
        print('decision')
        #

if __name__ == '__main__':

    rospy.init_node('tiago_esta_preso')

    tiago = myRobot()

    while not rospy.is_shutdown(): # test
        tiago.move_staright()
    
    
    # state = 0

    
    # while(...):
     # if state == 0:
        # decision
        # compute next state
     # else if state == 1
        # image porcessing
        # compute next state
     # else if state == 3
        # move straight
        # compute next state
     # else if state == 4
        # turn
        # compute next state
