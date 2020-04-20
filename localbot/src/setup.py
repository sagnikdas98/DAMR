import os




def setEnvironment():
    os.environ["SAS_NAME"] = None
    os.environ["SAS_VALUE"] = None
    os.environ["TOPIC_NAMESPACE"] = None
    os.environ["BOT_ID"] = None
    os.environ["TOPIC_VELOCITY"] = 'cmd_vel'
    os.environ["TOPIC_STOP"] = 'motor_stop'

    os.environ["LGPWM"] = int(12)
    os.environ["LGIN1"] = int(5)
    os.environ["LGIN2"] = int(6)

    os.environ["RGPWM"] = int(13)
    os.environ["RGIN1"] = int(16)
    os.environ["RGIN2"] = int(26)
    

