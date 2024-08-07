#! shebang

import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class myCamera():

    def __init__(self):
        print('init camera')
        # Bridge to convert ROS message to openCV
        self.bridge = CvBridge()

        # Subscriber to the camera image
        self.image_sub = rospy.Subscriber("/xtion/rgb/image_color",Image,self.imageCallBack)

        # Server Service camera
        # ...

    def callback_ServiceCamera(self, request):
        print('image service')
        # ...
        # return

    def callback_SubscribeCamera(self, msg):
        print('callback camera')
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            print(e)

        # cv_image[linha][coluna][bgr] bgr-> 0:blue, 1:green, 2:red
        print(self.cv_image[0][0])
        print(self.cv_image[0][0][0])

        # Display the image
        cv2.imshow("raw", self.cv_image)
        cv2.waitKey(3)
