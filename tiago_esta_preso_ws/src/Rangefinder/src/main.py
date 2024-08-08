#! /usr/bin/python

import rospy
from math import sin, cos, pi
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

        self.anglemax = 0.0
        self.anglemin = 0.0
        self.angleincrement = 0.0
        #self.numraios = 0.0
        self.distances = []
        self.yaw = 0.0

        self.cmd_base = Twist()
        self.cmd_head = Twist()

    def callback_odometria(self, msg):
        print('callback odometria')
        print(f'Yaw pose:')
        qtn = msg.pose.pose.orientation
        qtn_list = [qtn.x, qtn.y, qtn.z, qtn.w]
        self.yaw = euler_from_quaternion(qtn_list)[2]
        print(self.yaw)
        print()
        # Armazenar os dados de odometria
        # a mensagem varia de -pi a +pi radianos em relação ao referencial da cena!
        # se o robô precisar girar de -pi/2 para +pi/2 passando por pi,
        # vai gerar o salto no valor yaw da odometria.
        # tornar a faixa um valor contínuo, entre 0 e 2*pi, ao
        # permitir posicionamentos como 270 graus ou +3*pi/2 radianos

    def callback_laser(self, msg):  #  Validado pelo prof em 07 ago 24
        print('callback laser')
        # Armazenar os dados do laser
        self.anglemin = msg.angle_min
        self.anglemax = msg.angle_max
        self.angleincrement = msg.angle_increment
        ranges = msg.ranges
        #self.numraios = 1 + (self.anglemax - self.anglemin)/self.angleincrement


        indice_direita = 0.0
        distancia_direita = 0.0
        indice_esquerda = 0.0
        distancia_esquerda = 0.0
        indice_zero = 0.0
        distancia_zero = 0.0
        # calcular os índices correspondentes aos ângulos -90, 0 e +90 graus
        for ind, valor in enumerate(ranges):
            if ((self.anglemin + ind * self.angleincrement) + 1.5708) <= self.angleincrement: # -pi/2 radianos
                indice_direita = ind
                distancia_direita = valor
            elif -self.angleincrement < (self.anglemin + ind * self.angleincrement) <= self.angleincrement: # 0 radianos
                indice_zero = ind
                distancia_zero = valor
            elif (1.5708 - (self.anglemin + ind * self.angleincrement)) >= self.angleincrement: # pi/2 radianos
                indice_esquerda = ind
                distancia_esquerda = valor

        esquerda = self.anglemin + (indice_esquerda) * self.angleincrement
        frente = self.anglemin + (indice_zero) * self.angleincrement
        direita = self.anglemin + (indice_direita) * self.angleincrement

        self.distances = [esquerda, distancia_esquerda, frente, distancia_zero, direita, distancia_direita]

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
        for r in ranges: 
            if r < v_min and r > 0.10: # r > 0.10 for prune distances from laser to robot body!!
                v_min = r
                id_max = idx
            idx += 1
        angle_max = self.anglemin + id_max * self.angleincrement # ângulo em relação ao robô do obstáculo mais próximo

        x = v_min * cos(angle_max)
        y = v_min * sin(angle_max)

        print(f'x coordinate: {x} meters')
        print(f'y coordinate: {y} meters')
        print(self.distances)


    def moveStraight(self): # João implementa
        print('move straight')
        # error = ...
        # while(abs(error) < value):

    def turn(self, sens):
        print('turn')

        # A dica do comentário deve ser a de medir a diferença entre o angulo
        # atual e o ângulo que deve ser alcançado
        # Á medida que o robô chega perto do alvo, diminuir a velocidade de giro

        # supondo que a decisão chama o método turn, informando o ângulo final,
        # então o argumento sens deve ser essa informação

        # error = ...
        # while(abs(error) < value):

        # error = angulo final - angulo atual
        # angulo final == angulo inicial + sens
        # angulo inicial == self.yaw
        
        # O sens informa giro em +pi/2 ou -pi/2 em relação ao ângulo atual em relação
        # o referencial da cena.

        # O problema potencial é o robô precisar girar para ou a partir de +pi/-pi
        initial_yaw = self.yaw
        final_yaw = initial_yaw + sens
        # se posição inicial for -/+pi radianos, converter o final_yaw
        if final_yaw > pi:  # 3*pi/2
            final_yaw -= 2 * pi # -pi/2
        elif final_yaw < -pi: # -3*pi/2
            final_yaw += 2 * pi # +pi/2

        error = final_yaw - self.yaw
        limit_error = self.angleincrement

        while abs(error) > limit_error:
            self.cmd_base.linear.x = 0.0
            self.cmd_base.angular.z = error/(final_yaw - initial_yaw) * pi/4 # radians/s
            self.publ_base.publish(self.cmd_base)
            error = final_yaw - self.yaw
        self.cmd_base.angular.z = 0.0
        self.publ_base.publish(self.cmd_base)
    def decision(self):
        print('decision')
        #

if __name__ == '__main__':

    rospy.init_node('TiagoEstaPreso')

    tiago = myRobot()

    #rospy.spin()

    state = 0
    while not rospy.is_shutdown():
        tiago.turn(pi/2)
        tiago.turn(-pi/2)
        break

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