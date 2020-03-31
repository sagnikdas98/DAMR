import RPi.GPIO as GPIO
import os

from azure.servicebus.control_client import ServiceBusService, Message, Topic, Rule, DEFAULT_RULE_NAME

class queueRead():


    def __init__(self):
        


        


        ### initialize variables
        self.topic_vel = os.environ["TOPIC_VELOCITY"]
        self.topic_stop = os.environ["TOPIC_STOP"]

       
        ### get parameters #### 
        self.SAS_name = os.environ["SAS_NAME"]
        self.SAS_value = os.environ["SAS_VALUE"]
        self.namespace = os.environ["TOPIC_NAMESPACE"]
        self.bot_id = os.environ["BOT_ID"]



        self.LGPWM = os.getenv('LGPWM', int(12))
        self.LGIN1 = os.getenv('LGIN1', int(5))
        self.LGIN2 = os.getenv('LGIN2', int(6))

        self.RGPWM = os.getenv('RGPWM', int(13))
        self.RGIN1 = os.getenv('RGIN1', int(16))
        self.RGIN2 = os.getenv('RGIN2', int(26))



        self.bus_service = ServiceBusService(                                
        service_namespace=self.namespace,
        shared_access_key_name=self.SAS_name,
        shared_access_key_value=self.SAS_value)


        self.bus_service.create_subscription((self.topic_vel+self.bot_id), self.bot_id)
        self.bus_service.create_subscription((self.topic_stop+self.bot_id), self.bot_id)

        


        ### setup ###
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.LGPWM, GPIO.OUT)
        GPIO.setup(self.LGIN1, GPIO.OUT)
        GPIO.setup(self.LGIN2, GPIO.OUT)

        self.Lpwm = GPIO.PWM(self.LGPWM, 1000)
        self.Lpwm.start(0)


        GPIO.setup(self.RGPWM, GPIO.OUT)
        GPIO.setup(self.RGIN1, GPIO.OUT)
        GPIO.setup(self.RGIN2, GPIO.OUT)

        self.Rpwm = GPIO.PWM(self.RGPWM, 1000)
        self.Rpwm.start(0)

    @staticmethod
    def motorCall(Gpwm, GIN1, GIN2, msg):
        if(msg > 0):
            GPIO.output(GIN1, GPIO.HIGH)
            GPIO.output(GIN2, GPIO.LOW)
            
        else:
            GPIO.output(GIN1, GPIO.LOW)
            GPIO.output(GIN2, GPIO.HIGH)
        pwm_per = abs(msg)
        Gpwm.ChangeDutyCycle(pwm_per)
        

    def motorStop(self):

        self.Lpwm.ChangeDutyCycle(0)
        self.Rpwm.ChangeDutyCycle(0)
        GPIO.output(self.LGIN1, GPIO.LOW)
        GPIO.output(self.LGIN2, GPIO.LOW)
        GPIO.output(self.RGIN1, GPIO.LOW)
        GPIO.output(self.RGIN2, GPIO.LOW)        


    def read(self):
        while(1):
            try:
                msg = self.bus_service.receive_subscription_message((self.topic_vel+self.bot_id), self.bot_id, peek_lock=False)
                if msg.body is not None:
                    res = list(map(int, msg.body.split(' ')))
                    queueRead.motorCall(self.Lpwm, self.LGIN1, self.LGIN2, res[0])
                    queueRead.motorCall(self.Rpwm, self.RGIN1, self.RGIN2, res[1])

                msg = self.bus_service.receive_subscription_message((self.topic_stop+self.bot_id), self.bot_id, peek_lock=False)
                if msg.body is not None:
                    self.motorStop()

            except:
                pass


            


if __name__ == '__main__':
    """ main """
    try:
        qRead = queueRead()
        qRead.read()
    except:
        pass
    finally:
        qRead.bus_service.delete_subscription((qRead.topic_vel+qRead.bot_id), qRead.bot_id)
        qRead.bus_service.delete_subscription((qRead.topic_stop+qRead.bot_id), qRead.bot_id)
        GPIO.cleanup()