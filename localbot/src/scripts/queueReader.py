#!/usr/bin/env python
import rospy

from std_msgs.msg import Int16
from std_msgs.msg import Float32

from azure.servicebus import SubscriptionClient

class queueRead():


    def __init__(self):
        rospy.init_node("queueRead", anonymous=True)
        self.nodename = rospy.get_name()
        
        rospy.loginfo("%s started" % self.nodename)

        ### initialize variables

       
        ### get parameters #### 
        self.connect_str = (rospy.get_param("~CONNECT_STR"))
        self.topic_name = (rospy.get_param("~TOPIC_NAME"))
        self.sub_client = SubscriptionClient.from_connection_string(
        self.connect_str, name=self.topic_name, debug=False)
        
        ### setup ###
        self.pub_lmotor = rospy.Publisher('lmotor_cmd', Float32, queue_size=10)
        self.pub_rmotor = rospy.Publisher('rmotor_cmd', Float32, queue_size=10)
        


    def read(self):
        while not rospy.is_shutdown():
            try:
                msg = next(queue_client.receive_messages())
                self.pub_lmotor.publish(msg[0])
                self.pub_lmotor.publish(msg[1])
                queue_client.delete_message(msg)
            except:
                pass


            


if __name__ == '__main__':
    """ main """
    try:
        qRead = queueRead()
        qRead.read()
    except rospy.ROSInterruptException:
        pass
    finally:
        self.queue_client.delete_queue()
        pass




