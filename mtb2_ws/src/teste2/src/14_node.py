#! /usr/bin/python
import rospy
import cv2
from cv_bridge import CvBridge , CvBridgeError
from sensor_msgs.msg import Image


class myCamera () :
    def __init__(self):
        print ('init camera')
        # Bridge to convert ROS message to openCV
        self.bridge = CvBridge()
        # Subscriber to the camera image
        self.image_sub = rospy.Subscriber("/xtion/rgb/image_color", Image, self.imageCallBack)

    #def callback_SubscribeCamera(self, msg):
    def imageCallBack(self, msg): # Nome do método deve ser igual ao do parâmetro de Subscriber
        print('callback_camera')
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

            # identificando tamanho da imagem por meio da mensagem
            # padrão do ROS
            imgheight = msg.height
            imgwidth = msg.width

            #redimensionando a imagem
            height = int(imgheight / 2)
            width = int(imgwidth / 2)
            self.cv_image = cv2.resize(self.cv_image, (width, height))

            # checar pixels um a um
            redThreshold = 50
            for h in range(height):
                for w in range(width):
                    if self.cv_image[h,w,2] < redThreshold:
                        self.cv_image[h,w,0] = 203
                        self.cv_image[h,w,1] = 192
                        self.cv_image[h,w,2] = 255

        except CvBridgeError as e:
            print(e)

         # cv_image[linha][coluna][bgr] 
         # bgr-> 0: blue , 1: green , 2: red
        print(self.cv_image[0][0])
        print(self.cv_image[0][0][0])

        #exercicio - identificar onde a bola está na imagem, e trocar
        # apenas a cor da bola na imagem

        # Display the image
        cv2.imshow("raw", self.cv_image)
        cv2.waitKey(3)

#programa principal
if __name__ == "__main__":
    rospy.init_node('cam_node')
    cam = myCamera()

    rospy.spin()
