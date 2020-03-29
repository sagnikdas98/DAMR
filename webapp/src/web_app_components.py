from azure.servicebus.control_client import ServiceBusService, Message, Topic, Rule, DEFAULT_RULE_NAME



class DAMRWEB:


    def __init__(self,namespace,SAS_name, SAS_value):

        self.topic_vel = 'cmd_vel'
        self.topic_stop = 'motor_stop'


        self.namespace = namespace
        self.SAS_name = SAS_name
        self.SAS_value=SAS_value


        self.topic_options = Topic()
        self.topic_options.max_size_in_megabytes = '10' #### Try : '1024'
        self.topic_options.default_message_time_to_live = 'PT5S'


        self.bus_service = ServiceBusService(                                
        service_namespace=self.namespace,
        shared_access_key_name=self.SAS_name,
        shared_access_key_value=self.SAS_value)

        



        


    #create topics of cmd_vel and motor stop
    def  createLocalbot(self,bot_id):

        self.bus_service.create_topic((self.topic_vel+bot_id), self.topic_options)
        self.bus_service.create_topic((self.topic_stop+bot_id), self.topic_options)
        # self.bus_service.create_subscription((self.topic_vel+bot_id), bot_id)
        # self.bus_service.create_subscription((self.topic_stop+bot_id), bot_id)

        pass


    def remoteControl(self, bot_id, cmd_value):

        msg = Message(str(cmd_value).encode('utf-8'))
        self.bus_service.send_topic_message((self.topic_vel+bot_id), msg)


    def remoteControlStop(self, bot_id):

        msg = Message('0 0'.encode('utf-8'))
        self.bus_service.send_topic_message((self.topic_vel+bot_id), msg)


    def deleteTopic(self, bot_id):
        self.bus_service.delete_topic((self.topic_vel+bot_id))
        self.bus_service.delete_topic((self.topic_stop+bot_id))

