#! /usr/bin/python

import rospy
from math import pi, sin, cos
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler

class myRobot():

    def __init__(self):    

        self.sub_odom = rospy.Subscriber('/mobile_base_controller/odom', Odometry, self.callback_odometria, queue_size=1)
        self.sub_laser = rospy.Subscriber('/scan_raw', LaserScan, self.callback_laser, queue_size=1)
        self.client_camera = None
        self.publ_base = rospy.Publisher('/mobile_base_controller/cmd_vel', Twist, queue_size =1)
        self.publ_head = None # rospy.Publisher()
        

        self.anglemax = 0
        self.anglemin = 0
        self.angleincrement = 0
        self.numraios = 0
        self.ranges = []

        self.cmd_base = Twist()
        self.cmd_head = Twist()
    
    def callback_odometria(self, msg):
        print('callback odometria')
        print(f'Yaw pose:')
        qtn = msg.pose.pose.orientation
        qtn_list = [qtn.x, qtn.y, qtn.z, qtn.w]
        (roll, pitch, yaw) = euler_from_quaternion(qtn_list)
        print(yaw)
        print()
        

    def callback_laser(self, msg):  #  Validado pelo prof em 07 ago 24
        print('callback laser')
        # Armazenar os dados do laser
        self.anglemin = msg.angle_min
        self.anglemax = msg.angle_max
        self.angleincrement = msg.angle_increment
        self.ranges = msg.ranges
        self.numraios = 1 + (self.anglemax - self.anglemin)/self.angleincrement


        indice_direita = 0.0
        distancia_direita = 0.0
        indice_esquerda = 0.0
        distancia_esquerda = 0.0
        indice_zero = 0.0
        distancia_zero = 0.0
        # calcular os índices correspondentes aos ângulos -90, 0 e +90 graus
        for ind, valor in enumerate(self.ranges):
            if ((self.anglemin + ind * self.angleincrement) + 1.5708) < self.angleincrement: # -pi/2 radianos
                indice_direita = ind
                distancia_direita = valor
            elif -self.angleincrement < (self.anglemin + ind * self.angleincrement) < self.angleincrement: # 0 radianos
                indice_zero = ind
                distancia_zero = valor
            elif (1.5708 - (self.anglemin + ind * self.angleincrement)) > self.angleincrement: # pi/2 radianos
                indice_esquerda = ind
                distancia_esquerda = valor

        self.direcao_esquerda = self.anglemin + (indice_esquerda) * self.angleincrement
        self.direcao_frente = self.anglemin + (indice_zero) * self.angleincrement
        self.direcao_direita = self.anglemin + (indice_direita) * self.angleincrement

        id_max = 0
        idx = 0
        v_min = 1000
        for r in self.ranges: 
            if r < v_min and r > 0.10: # r > 0.10 for prune distances from laser to robot body!!
                v_min = r
                id_max = idx
            idx += 1
        angle_max = self.anglemin + id_max * self.angleincrement # ângulo em relação ao robô do obstáculo mais próximo

        x = v_min * cos(angle_max)
        y = v_min * sin(angle_max)

        print(f'x coordinate: {x}')
        print(f'y coordinate: {y}')

    def move_straight(self, distance):
        rate = rospy.Rate(10)
        moving = True
        
        while not rospy.is_shutdown() and moving:
            print('se move aí')

            if self.ranges and min(self.ranges) < distance:
                self.cmd_base.linear.x = 0
                moving = False
            else:
                self.cmd_base.linear.x = 1                
                print(self.ranges)
            
            self.publ_base.publish(self.cmd_base)
            rate.sleep()
                

    def turn(self, sens):
        print('turn')
        # sens pode ser comando direita/esquerda?
        
        rate = rospy.Rate(1)  # 1 hz de frequência de publicar comandos
        count = 0
        while not rospy.is_shutdown(): # and cond to stop turn
            if sens == 'direita':
                self.cmd_base.angular.z = 1
                rate.sleep()

            elif sens == 'esquerda':
                self.cmd_base.angular.z = -1
                rate.sleep()
            count += 1
            rate.sleep()
            self.publ_base.publish(self.cmd_base)
        # error = ...
        # while(abs(error) < value):

    def decision(self):
        print('decision')
        dist_front = min(self.ranges)
        dist_right = 0 # get dist_right
        dist_left = 0 # get dist_left
        


        # decides what action (move straight, turn or process img)    
        if dist_right < 1.5 and dist_left < 1.5:
            self.move_straight(1.0)
        elif dist_front < 1.5:
            if dist_left > dist_right:
                self.turn(pi/2)
            else:
                self.turn(-pi/2)
        else:
            pass
            # self.cmd_head.angular.z = 0.1
            # self.publ_head.publish(self.cmd_head)
            # rospy.sleep(1)


if __name__ == '__main__':

    rospy.init_node('tiago_esta_preso')

    tiago = myRobot()

    while not rospy.is_shutdown(): # test
        tiago.move_straight(-10)
        
    state = 0

    while(True):
        if state == 0:
            tiago.decision()
        elif state == 1:
            pass # process img
        elif state == 2:
            tiago.move_straight(1.0)
        elif state == 3:
            tiago.turn()
