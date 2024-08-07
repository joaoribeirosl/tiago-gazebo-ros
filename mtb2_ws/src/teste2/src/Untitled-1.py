#! /usr/bin/python3
import rospy
# Import the service classes : servive definition , response message
from teste2.srv import AddTwoInts , AddTwoIntsResponse
# Definition of the function called by the serice
def callback_AddTwoInts(req):

    # Create a response variable
    res = AddTwoIntsResponse()
    # Compute the sum
    res = req.A + req.B
    # Return the response variable
    return res


if __name__ == " __main__ ":

# Start the node
    rospy.init_node("AddTwoInts_server_node")
    # Start the service server
    my_service = rospy.Service("add_two_ints_service_name", AddTwoInts, callback_AddTwoInts)

    print("Ready to add two ints.")

    # Wait to be closed by the user
    rospy.spin()

    

#! /usr/bin/python3

import rospy
from teste2.srv import *

if __name__ == "__main__":
     # Wait for the server to be started
    rospy.wait_for_service('add_two_ints_service_name')
    print("add_two_ints service is active")

    try:
        # Connect to the server
        h_AddTwoInts = rospy.ServiceProxy('add_two_ints_service_name', AddTwoInts)

        # Create and fill the resquest
        request = AddTwoIntsRequest()
        print ('Service call')
        request.A = 2
        request.B = 3
        # Call the service
        response = h_AddTwoInts(request)
        print(response.Sum)
    
        # If the connection fails ( DEBUG )
    except rospy.ServiceException as e :
        print ("Service call failed : %s"% e )
