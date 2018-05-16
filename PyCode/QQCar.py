###################################################
#               智能小车1.0
#
#               @author chenph
#               @date 2018/5/15
###################################################
# 光敏传感器           红 黑 任意
# 超声波传感器-发送     红 黑  任意 * 2啦啦啦啦吧
# 超声波传感器-接收
# 红外避障传感器-左     红 黑  任意
# 红外避障传感器-右     红 黑  任意
# 无源蜂鸣器           红 黑   任意
# 寻迹传感器           红 黑   任意
# 七彩大灯R-G-B         黑 任意 * 3
# 超声波云台舵机-左右转   任意
# 摄像头云台舵机-左右转   红   黑   任意
# 摄像头云台舵机-上下转   红   黑   任意
# 左轮in1-in2         任意 * 2
# 右轮in1-in2         任意 * 2

# 接电：红 8
# 接地：黑 9
# 其他：17

import threading

from PyCode.Modules.RGBLightModule import *
from PyCode.Modules.ServoModule import *
from PyCode.Modules.WheelModule import *
from PyCode.Sensors.BeeSensor import *
from PyCode.Sensors.InfraredSensor import *
from PyCode.Sensors.LightSensor import *
from PyCode.Sensors.TraceSensor import *
from PyCode.Sensors.UltrasonicSensor import *


class QQCar:

    def __init__(self):
        # 初始化智能小车使用控制脚--------------
        self.PIN_LIGHT = 18             # 01：光敏
        self.PIN_ULTRASON_TRIG = 11     # 02：超声波-发射
        self.PIN_ULTRASON_ECHO = 13     # 03：超声波-接收
        self.PIN_INFRARED_L = 7         # 04：左避障
        self.PIN_INFRARED_R = 25        # 05：右避障
        self.PIN_BEE = 26               # 06：蜂鸣
        self.PIN_TRACE = 15             # 07：寻迹
        self.PIN_LIGHT_R = 19           # 08：大灯
        self.PIN_LIGHT_G = 21           # 09：大灯
        self.PIN_LIGHT_B = 23           # 10：大灯
        self.PIN_SERVO_U = 29           # 11：超声波云台
        self.PIN_SERVO_CH = 31          # 12：摄像头水平云台
        self.PIN_SERVO_CV = 33          # 13：摄像头垂直云台
        self.WHEEL_L_IN1 = 32           # 14：左轮
        self.WHEEL_L_IN2 = 36           # 15：左轮
        self.WHEEL_R_IN1 = 40           # 16：右轮
        self.WHEEL_R_IN2 = 38           # 17：右轮
        # 初始化树莓派gpio控制脚----------------
        # 大灯
        self.rgbLightModule = RGBLightModule(self.PIN_LIGHT_R, self.PIN_LIGHT_G, self.PIN_LIGHT_B)
        # 超声波云台
        self.servoModule_U = ServoModule(self.PIN_SERVO_U)
        # 摄像头水平云台
        self.servoModule_CH = ServoModule(self.PIN_SERVO_CH)
        # 摄像头垂直云台
        self.servoModule_CV = ServoModule(self.PIN_SERVO_CV)
        # 车轮控制
        self.wheelModule = WheelModule(self.WHEEL_L_IN1, self.WHEEL_L_IN2, self.WHEEL_R_IN1, self.WHEEL_R_IN2)
        # 蜂鸣器
        self.beeSensor = BeeSensor(self.PIN_BEE)
        # 左避障
        self.infraredSensor_L = InfraredSensor(self.PIN_INFRARED_L)
        # 右避障
        self.infraredSensor_R = InfraredSensor(self.PIN_INFRARED_R)
        # 光敏
        self.lightSensor = LightSensor(self.PIN_LIGHT)
        # 寻迹
        self.traceSensor = TraceSensor(self.PIN_TRACE)
        # 超声波
        self.ultrasonicSensor = UltrasonicSensor(self.PIN_ULTRASON_TRIG, self.PIN_ULTRASON_ECHO)
        # -------------------------------------
        # 启动传感器
        threading.Thread(target=self.start, args=(self,))

    # 启动传感器
    def start(self):
        while True:
            # 红外检测障碍物
            if self.infraredSensor_L.getStatus() == InfraredSensor.INFRARED_SENSOR_BLOCK or self.infraredSensor_R.getStatus() == InfraredSensor.INFRARED_SENSOR_BLOCK:
                self.beeSensor.play()
            # 超声波检测障碍物
            if self.ultrasonicSensor.getDistance() <= 0.3:
                self.beeSensor.play()
            # 寻迹
            #if self.traceSensor.getStatus() == TraceSensor.TRACE_SENSOR_ONWAY:
            #    self.beeSensor.play(0.5)
            # 检测光亮
            if self.lightSensor.getStatus() == LightSensor.LIGHT_SENSOR_DARK:
                self.rgbLightModule.turnOn()
            else:
                self.rgbLightModule.turnOff()
            time.sleep(1)

    # 前进的代码
    def forward(self):
        self.wheelModule.forward()

    # 后退
    def backOff(self):
        self.wheelModule.backOff()

    # 左转
    def leftTurn(self):
        self.wheelModule.leftTurn()

    # 右转
    def rightTurn(self):
        self.wheelModule.rightTurn()

    # 停车
    def stop(self):
        self.wheelModule.stop()

    # 超声波云台，左转
    def servoUltrasonicTurnLeft(self):
        self.servoModule_U.turnLeft()

    # 超声波云台，右转
    def servoUltrasonicTurnRight(self):
        self.servoModule_U.turnRight()

    # 摄像头水平云台，左转
    def servoCameraHTurnLeft(self):
        self.servoModule_CH.turnLeft()

    # 摄像头水平云台，右转
    def servoCameraHTurnRight(self):
        self.servoModule_CH.turnRight()

    # 摄像头垂直云台，上翻
    def servoCameraVTurnUp(self):
        self.servoModule_CV.turnLeft()

    # 摄像头垂直云台，下翻
    def servoCameraVTurnDown(self):
        self.servoModule_CV.turnRight()

    # 开灯
    def turnOnLight(self):
        self.rgbLightModule.turnOn()

    # 关灯
    def turnOffLight(self):
        self.rgbLightModule.turnOff()
