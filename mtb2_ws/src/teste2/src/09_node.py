#! /usr/bin/python

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

# Definição de uma classe
class RobotControlLoop():
	def __init__ (self):
		# Definir o Subscriber (tópico, Tipo de mensagem, callback, tamanho do queue)
		self.sub = rospy.Subscriber('/turtle1/pose', Pose, self.callback, queue_size=1)
		self.x = 0.0
		self.y = 0.0
		self.theta = 0.0
		self.targetX = 1.0
		self.targetY = 1.0
		self.targetTheta = 3.14
		self.pub = rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size = 1)


	def callback(self, msg):
		self.x = msg.x
		self.y = msg.y
		self.theta = msg.theta

	def printMsg(self):
		print(f'Posição \n{self.x}, \n{self.y}, \n{self.theta}')

	def publish_cmd(self):
		cmd = Twist()
		if self.targetX > self.x:
			cmd.linear.x = self.targetX - self.x
		else:
			cmd.linear.x = self.x - self.targetX
		if self.targetY > self.y:
			cmd.linear.y = self.targetY - self.y
		else:
			cmd.linear.y = self.y - self.targetY
		if self.targetTheta > self.theta:
			cmd.angular.z = self.targetTheta - self.theta
		else:
			cmd.angular.z = self.theta - self.targetTheta
		self.pub.publish(cmd)

# Exercicio receber posição e calcular velocidade da turtlesim
# Main routine

if __name__ == "__main__":
	rospy.init_node('simple_subscriber') # Melhor inicializar primeiro o node

	robot = RobotControlLoop()

# Se o nó é unicamente subscriber, usar rospy.spin() como loop infinito
# Como vamos interagir escrevendo de volta, usar laço while
	x = 0.0
	y = 0.0
	theta = 0.0  #theta em radianos!

	while not rospy.is_shutdown():
		robot.printMsg()
		if x and y and theta:
			dif_x = x - robot.x
			dif_y = y - robot.y
			dif_theta = theta - robot.theta
			print(f'Velocidades por tick:\n{dif_x} x\n{dif_y} y\n{dif_theta} rad')
			x = robot.x
			y = robot.y
			theta = robot.theta # atualizar os valores
		else:
			x = robot.x # atualizar os valores
			y = robot.y
			theta = robot.theta
		robot.publish_cmd()
