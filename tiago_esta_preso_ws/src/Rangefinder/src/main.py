#! /usr/bin/python

import rospy
from math import sin, cos
from sensor_msgs.msg import LaserScan

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

from tf.transformations import euler_from_quaternion, quaternion_from_euler


class myRobot():

    def __init__(self):
        # Subscriber odometria
        self.sub_odom = rospy.Subscriber('/mobile_base_controller/odom', 
                                         Odometry, self.callback_odometria, queue_size=1)
        # Subscriber laser
        self.sub_laser = rospy.Subscriber('/scan_raw', LaserScan, self.callback_laser, queue_size=1)
        # Client Service camera
        self.client_camera = None
        # Publisher base
        self.publ_base = rospy.Publisher('/mobile_base_controller/cmd_vel', Twist, queue_size =1)
        # Publisher cabeca
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
        # Armazenar os dados de odometria
        # a mensagem varia de -pi a +pi radianos
        # se o robô precisar girar de -pi/2 para +pi/2 passando por pi,
        # vai gerar o salto no valor yaw da odometria.
        # tornar a faixa um valor contínuo, entre 0 e 2*pi, ao
        # permitir posicionamentos como 270 graus ou +3*pi/2 radianos
        self.

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

        ## Debug - print information from laserscan channel        
        #print(self.angleincrement)
        #print(self.anglemin)
        #print(self.anglemax)
        #print('------------------')
        #print('ind esquerda +pi/2')
        #print({indice_esquerda})
        #print(self.anglemin + (indice_esquerda) * self.angleincrement)
        #print(f'Distância a 90°: {distancia_esquerda}')
        #print('------------------')
        #print('ind direita -pi/2')
        #print({indice_direita})
        #print(self.anglemin + (indice_direita) * self.angleincrement)
        #print(f'Distância a -90°: {distancia_direita}')
        #print('------------------')
        #print(f'ind zero rad: {indice_zero}')
        #print(f'{self.anglemin + (indice_zero) * self.angleincrement}')
        #print(f'Distância a 0°: {distancia_zero}')
        ## medir menor distância     
        #  minimum = min(tabela_distancias)
        # indices = [i for i, v in enumerate(tabela_distancias) if v == minimum and v > 0.15]
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


    def moveStraight(self): # João implementa
        print('move straight')
        # error = ...
        # while(abs(error) < value):

    def turn(self, sens):
        print('turn')
        # sens pode ser comando direita/esquerda?
        if sens == 'direita':
            self.cmd_base.linear.x = 1
            self.cmd_base.angular.z = -

        elif sens == 'esquerda':

            cmd = Twist()

        rate = rospy.Rate(1)  # 1 hz de frequência de publicar comandos
        count = 0
        while not rospy.is_shutdown():
            if count % 2 == 0:
                
            else:
                self.cmd_base.linear.x = 0
                self.cmd_base.angular.z = 1
            self.publ_base.publish(cmd)
            count += 1
            rate.sleep()
        # error = ...
        # while(abs(error) < value):

    def decision(self):
        print('decision')
        #

if __name__ == '__main__':

    rospy.init_node('TiagoEstaPreso')

    tiago = myRobot()

    rospy.spin()

    state = 0
    # while(...):
     # if state == 0:
        # decision
        # compute next state
     # else if state == 1
        # image processing
        # compute next state
     # else if state == 3
        # move straight
        # compute next state
     # else if state == 4
        # turn
        # compute next state