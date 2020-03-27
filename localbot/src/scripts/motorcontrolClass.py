#!/usr/bin/env python
import RPi.GPIO as GPIO
import rospy
from std_msgs.msg import String

from std_msgs.msg import Int16
from std_msgs.msg import Float32

class MotorControl():


    def __init__(self):
        rospy.init_node("motorControl", anonymous=True)
        self.nodename = rospy.get_name()
        
        rospy.loginfo("%s started" % self.nodename)

        ### initialize variables

       
        ### get parameters #### 



        self.GPWM = int(rospy.get_param("~GPWM"))
        self.GIN1 = int(rospy.get_param("~GIN1"))
        self.GIN2 = int(rospy.get_param("~GIN2"))


        ### setup ###

        rospy.Subscriber("motor_cmd", Float32, self.motorCall)
        rospy.Subscriber("motorStop", Int16, self.motorStop)

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.GPWM, GPIO.OUT)
        GPIO.setup(self.GIN1, GPIO.OUT)
        GPIO.setup(self.GIN2, GPIO.OUT)

        self.pwm = GPIO.PWM(self.GPWM, 1000)
        self.pwm.start(0)




    def motorCall(self, msg):
        if(msg.data > 0):
            GPIO.output(self.GIN1, GPIO.HIGH)
            GPIO.output(self.GIN2, GPIO.LOW)
            
        else:
            GPIO.output(self.GIN1, GPIO.LOW)
            GPIO.output(self.GIN2, GPIO.HIGH)
        pwm_per = abs(msg.data)
        self.pwm.ChangeDutyCycle(pwm_per)
        rospy.loginfo("%s called" % self.nodename) 

    def motorStop(self,msg):

        self.pwm.ChangeDutyCycle(0)
        GPIO.output(self.GIN1, GPIO.LOW)
        GPIO.output(self.GIN2, GPIO.LOW)


    def motor(self):
        while not rospy.is_shutdown():
            rospy.spin()


if __name__ == '__main__':
    """ main """
    try:
        motorcontrol = MotorControl()
        motorcontrol.motor()
    except rospy.ROSInterruptException:
        pass
    finally:
        GPIO.cleanup()