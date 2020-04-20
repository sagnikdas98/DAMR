#!/usr/bin/env python
import rospy

from std_msgs.msg import Int16
from std_msgs.msg import Float32

from azure.servicebus.control_client import ServiceBusService, Message, Topic, Rule, DEFAULT_RULE_NAME

class queueRead():


    def __init__(self):
        rospy.init_node("queueRead", anonymous=True)
        self.nodename = rospy.get_name()
        
        rospy.loginfo("%s started" % self.nodename)

        ### initialize variables
        self.topic_vel = 'cmd_vel'
        self.topic_stop = 'motor_stop'

       
        ### get parameters #### 
        self.SAS_name = (rospy.get_param("~SAS_NAME"))
        self.SAS_value = (rospy.get_param("~SAS_VALUE"))
        self.namespace = (rospy.get_param("~TOPIC_NAMESPACE"))
        self.bot_id = (rospy.get_param("~BOT_ID"))



        self.bus_service = ServiceBusService(                                
        service_namespace=self.namespace,
        shared_access_key_name=self.SAS_name,
        shared_access_key_value=self.SAS_value)


        self.bus_service.create_subscription((self.topic_vel+self.bot_id), self.bot_id)
        self.bus_service.create_subscription((self.topic_stop+self.bot_id), self.bot_id)

        


        ### setup ###
        self.pub_lmotor = rospy.Publisher('lmotor_cmd', Float32, queue_size=10)
        self.pub_rmotor = rospy.Publisher('rmotor_cmd', Float32, queue_size=10)
        self.pub_motor_stop = rospy.Publisher('motorStop', Int16, queue_size=10)
        


    def read(self):
        while not rospy.is_shutdown():
            try:
                msg = self.bus_service.receive_subscription_message((self.topic_vel+self.bot_id), self.bot_id, peek_lock=False)
                if msg.body is not None:
                    res = list(map(float, msg.body.split(' ')))
                    self.pub_lmotor.publish(res[0])
                    self.pub_lmotor.publish(res[1])

                msg = self.bus_service.receive_subscription_message((self.topic_stop+self.bot_id), self.bot_id, peek_lock=False)
                if msg.body is not None:
                    self.pub_lmotor.publish(int(msg.body))

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
        qRead.bus_service.delete_subscription((qRead.topic_vel+qRead.bot_id), qRead.bot_id)
        qRead.bus_service.delete_subscription((qRead.topic_stop+qRead.bot_id), qRead.bot_id)