#coding:utf-8
'''
Raspberry Pi WiFi video robot car drive souce code
Writer: liuviking
Copyright:XiaoR Geek Tech
The code can be used free,but not for commerce purpose.
All rights reserved, unauthorized use will be prosecuted by XiaoR Geek! 
'''
import os
from socket import *
from time import ctime
import binascii
import RPi.GPIO as GPIO
import time
import threading
from smbus import SMBus
import cv2
import numpy as np
from subprocess import call

XRservo = SMBus(1)
print '....WIFIROBOTS START!!!...'
global Path_Dect_px
Path_Dect_px = 320
global Path_Dect_on
Path_Dect_on = 0
#from serial import *
import serial
serialArduino = serial.Serial('/dev/ttyACM0', 9600)
##serialArduino.readline()
##serialArduino.write()




#######################################
#############Signal pin defination##############
#######################################
GPIO.setmode(GPIO.BCM)

########LED port defination#################
LED0 = 10
LED1 = 9
LED2 = 25

########Motor drive port defination#################
ENA = 13        #//L298 Enable A 
ENB = 20        #//L298 Enable B
IN1 = 19        #//Motor port 1
IN2 = 16        #//Motor port 2
IN3 = 21        #//Motor port 3
IN4 = 26        #//Motor port 4
########Buzer port #########################
BUZ = 10

########Servo port defination#################

########Ultrasonic port defination#################
ECHO = 4        #Ultrasonic receiving foot position   
TRIG = 17       #Ultrasonic sending foot position

########Infrared sensor port defination#################
IR_R = 18       #Right line following infrared sensor
IR_L = 27       #Left line following infrared sensor
IR_M = 22       #Middle obstacle avoidance infrared sensor
IRF_R = 23      #Right object tracking infrared sensror
IRF_L = 24      #Left object tracking infrardd sensor
global Cruising_Flag
Cruising_Flag = 0       #//Current circulation mode
global Pre_Cruising_Flag
Pre_Cruising_Flag = 0   #//Precycling mode

global RevStatus
RevStatus = 0
global TurnAngle
TurnAngle=0;
global Golength
Golength=0
buffer = ['00','00','00','00','00','00']
global motor_flag
motor_flag=1


global left_speed
global right_speed
global left_speed_hold
global right_speed_hold




left_speed=100
right_speed=100
#######################################
#########Pin type setup and initialization##########
#######################################
GPIO.setwarnings(False)

#########led initialized to 000##########
GPIO.setup(LED0,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(LED1,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(LED2,GPIO.OUT,initial=GPIO.HIGH)

#########motor initialized to LOW##########
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
ENA_pwm=GPIO.PWM(ENA,1000) 
ENA_pwm.start(0) 
ENA_pwm.ChangeDutyCycle(100)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
ENB_pwm=GPIO.PWM(ENB,1000) 
ENB_pwm.start(0) 
ENB_pwm.ChangeDutyCycle(100)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)



#########Infrared initialized to input，and internal pull up#########
GPIO.setup(IR_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_M,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IRF_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IRF_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)



##########Ultrasonic module pin type set#########
GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW)#ultrasonic module transmitting end pin set trig
GPIO.setup(ECHO,GPIO.IN,pull_up_down=GPIO.PUD_UP)#ultrasonic module receiving end pin set echo



####################################################
##Functin name Open_Light()
##Function performance Open headlight LED0
##Entrance parameter ：none
##Exit parameter：none
####################################################
def     Open_Light():#turn on headlight LED0
        GPIO.output(LED0,False)#Headlight's anode to 5V, cathode to IO port
        ##read = serialArduino.readline()
        while s[0:len(s)-1] != "LED01":
                s = str(serialArduino.readline())
                serialArduino.write("LED01")
        while s[0:len(s)-1] != "LED61":
                s = str(serialArduino.readline())
                serialArduino.write("LED61")
        time.sleep(1)
####################################################
##Function name Close_Light()
##Function performance Close headlight
##Enterance parameter：none
##Exit parameter：none
####################################################
def     Close_Light():#Close headlight
        GPIO.output(LED0,True)#Headlight's anode to 5V, cathode to IO port
        ##read = serialArduino.readline()
        while s[0:len(s)-1] != "LED00":
                s = str(serialArduino.readline())
                serialArduino.write("LED00")
        while s[0:len(s)-1] != "LED60":
                s = str(serialArduino.readline())
                serialArduino.write("LED60")
        time.sleep(1)

####################################################
##Functin name Open_Buzer()
##Function performance Open headlight LED0
##Entrance parameter ：none
##Exit parameter：none
####################################################
def     Open_Buzer():#turn on headlight LED0
        GPIO.output(BUZ,False)#Headlight's anode to 5V, cathode to IO port
        time.sleep(1)

####################################################
##Function name Close_Buzer()
##Function performance Close headlight
##Enterance parameter：none
##Exit parameter：none
####################################################
def     Close_Buzer():#Close headlight
        GPIO.output(BUZ,True)#Headlight's anode to 5V, cathode to IO port
        time.sleep(1)   
####################################################
##Function name init_light()
##Function performance running light
##Enterance parameter：none
##Exit parameter：none
####################################################
def     init_light():#running light
        for i in range(1, 5):
                GPIO.output(LED0,False)#running light LED0
                GPIO.output(LED1,False)#running light LED1
                GPIO.output(LED2,False)#running light LED2
                time.sleep(0.5)
                GPIO.output(LED0,True)#running light LED0
                GPIO.output(LED1,False)#running light LED1
                GPIO.output(LED2,False)#running light LED2
                time.sleep(0.5)
                GPIO.output(LED0,False)#running light LED0
                GPIO.output(LED1,True)#running light LED1
                GPIO.output(LED2,False)#running light LED2
                time.sleep(0.5)
                GPIO.output(LED0,False)#running light LED0
                GPIO.output(LED1,False)#running light LED1
                GPIO.output(LED2,True)#running light LED2
                time.sleep(0.5)
                GPIO.output(LED0,False)#running light LED0
                GPIO.output(LED1,False)#running light LED1
                GPIO.output(LED2,False)#running light LED2
                time.sleep(0.5)
                GPIO.output(LED0,True)#running light LED0
                GPIO.output(LED1,True)#running light LED1
                GPIO.output(LED2,True)#running light LED2
##########Robot's direction control###########################
def Motor_Forward():
        print 'motor forward'
        GPIO.output(ENA,True)
        GPIO.output(ENB,True)
        GPIO.output(IN1,True)
        GPIO.output(IN2,False)
        GPIO.output(IN3,True)
        GPIO.output(IN4,False)
        GPIO.output(LED1,False)#LED1 turn on
        GPIO.output(LED2,False)#LED1 turn on
        
def Motor_Backward():
        print 'motor_backward'
        GPIO.output(ENA,True)
        GPIO.output(ENB,True)
        GPIO.output(IN1,False)
        GPIO.output(IN2,True)
        GPIO.output(IN3,False)
        GPIO.output(IN4,True)
        GPIO.output(LED1,True)#LED1 turn off
        GPIO.output(LED2,False)#LED2 turn on
        
def Motor_TurnLeft():
        print 'motor_turnleft'
        GPIO.output(ENA,True)
        GPIO.output(ENB,True)
        GPIO.output(IN1,True)
        GPIO.output(IN2,False)
        GPIO.output(IN3,False)
        GPIO.output(IN4,True)
        GPIO.output(LED1,False)#LED1 turn on 
        GPIO.output(LED2,True) #LED2 tren off
def Motor_TurnRight():
        print 'motor_turnright'
        GPIO.output(ENA,True)
        GPIO.output(ENB,True)
        GPIO.output(IN1,False)
        GPIO.output(IN2,True)
        GPIO.output(IN3,True)
        GPIO.output(IN4,False)
        GPIO.output(LED1,False)#LED1 turn on
        GPIO.output(LED2,True) #LED2 turn off
def Motor_Stop():
        print 'motor_stop'
        GPIO.output(ENA,False)
        GPIO.output(ENB,False)
        GPIO.output(IN1,False)
        GPIO.output(IN2,False)
        GPIO.output(IN3,False)
        GPIO.output(IN4,False)
        GPIO.output(LED1,True)#LED1 trun off
        GPIO.output(LED2,True)#LED2 turn on
        
        
##########Robot direction calibration (used in mode)###########################
def forward():
        global motor_flag
        if motor_flag == 1:
                Motor_Forward()
        elif motor_flag == 2:
                Motor_Forward()
        elif motor_flag == 3:
                Motor_Backward()
        elif motor_flag == 4:
                Motor_Backward()
        elif motor_flag == 5:
                Motor_TurnLeft()
        elif motor_flag == 6:
                Motor_TurnLeft()
        elif motor_flag == 7:
                Motor_TurnRight()
        elif motor_flag == 8:
                Motor_TurnRight()
def back():
        global motor_flag
        if motor_flag == 1:
                Motor_Backward()
        elif motor_flag == 2:
                Motor_Backward()
        elif motor_flag == 3:
                Motor_Forward()
        elif motor_flag == 4:
                Motor_Forward()
        elif motor_flag == 5:
                Motor_TurnRight()
        elif motor_flag == 6:
                Motor_TurnRight()
        elif motor_flag == 7:
                Motor_TurnLeft()
        elif motor_flag == 8:
                Motor_TurnLeft()
                
def left():
        global motor_flag
        if motor_flag == 1:
                Motor_TurnLeft()
        elif motor_flag == 2:
                Motor_TurnRight()
        elif motor_flag == 3:
                Motor_TurnLeft()
        elif motor_flag == 4:
                Motor_TurnRight()
        elif motor_flag == 5:
                Motor_Forward()
        elif motor_flag == 6:
                Motor_Backward()
        elif motor_flag == 7:
                Motor_Forward()
        elif motor_flag == 8:
                Motor_Backward()

def right():
        global motor_flag
        if motor_flag == 1:
                Motor_TurnRight()
        elif motor_flag == 2:
                Motor_TurnLeft()
        elif motor_flag == 3:
                Motor_TurnRight()
        elif motor_flag == 4:
                Motor_TurnLeft()
        elif motor_flag == 5:
                Motor_Backward()
        elif motor_flag == 6:
                Motor_Forward()
        elif motor_flag == 7:
                Motor_Backward()
        elif motor_flag == 8:
                Motor_Forward()

##########Robot's speed control###########################
def ENA_Speed(EA_num):
        global left_speed
        left_speed=EA_num
        print 'EA_A改变啦 %d '%EA_num
        ENA_pwm.ChangeDutyCycle(EA_num)

def ENB_Speed(EB_num):
        global right_speed
        right_speed=EB_num
        print 'EB_B改变啦 %d '%EB_num
        ENB_pwm.ChangeDutyCycle(EB_num)
##Function performance ：servo control function
##Entrance parameter ：ServoNum(servo number)，angle_from_protocol(servo angle)
##Exit parameter：none
####################################################
def Angle_cal(angle_from_protocol):
        angle=hex(eval('0x'+angle_from_protocol))
        angle=int(angle,16)
        if angle > 160:
                angle=160
        elif angle < 15:
                angle=15
        return angle
        
def SetServoAngle(ServoNum,angle_from_protocol):
        GPIO.output(LED0,True)
        GPIO.output(LED1,True)
        GPIO.output(LED2,False)
        time.sleep(0.01)
        GPIO.output(LED0,True)
        GPIO.output(LED1,True)
        GPIO.output(LED2,True)
        if ServoNum== 1:
                XRservo.XiaoRGEEK_SetServo(0x01,Angle_cal(angle_from_protocol))
                return
        elif ServoNum== 2:
                XRservo.XiaoRGEEK_SetServo(0x02,Angle_cal(angle_from_protocol))
                return
        elif ServoNum== 3:
                XRservo.XiaoRGEEK_SetServo(0x03,Angle_cal(angle_from_protocol))
                return
        elif ServoNum== 4:
                XRservo.XiaoRGEEK_SetServo(0x04,Angle_cal(angle_from_protocol))
                return
        elif ServoNum== 5:
                XRservo.XiaoRGEEK_SetServo(0x05,Angle_cal(angle_from_protocol))
                return
        elif ServoNum== 6:
                XRservo.XiaoRGEEK_SetServo(0x06,Angle_cal(angle_from_protocol))
                return
        elif ServoNum== 7:
                XRservo.XiaoRGEEK_SetServo(0x07,Angle_cal(angle_from_protocol))
                return
        elif ServoNum== 8:
                XRservo.XiaoRGEEK_SetServo(0x08,Angle_cal(angle_from_protocol))
                return
        else:
                return




####################################################
##Function name ：Avoiding()
##Function performance ：Infrared obstacle avoidance function
##Entrance parameter ：none
##Exit parameter ：none
####################################################
def     Avoiding(): #infrared obstacle avoidance
        if GPIO.input(IR_M) == False:
                Motor_Stop()
                time.sleep(0.1)
                return

####################################################
##Function name TrackLine()
##Function performance Black line following
##Entrance parameter：none
##Exit parameter：none
####################################################
def TrackLine():
        if (GPIO.input(IR_L) == False)&(GPIO.input(IR_R) == False): #Black line is high, ground is low
                forward()
                return
        elif (GPIO.input(IR_L) == False)&(GPIO.input(IR_R) == True):
                right()
                return
        elif (GPIO.input(IR_L) == True)&(GPIO.input(IR_R) == False):
                left()
                return
        elif (GPIO.input(IR_L) == True)&(GPIO.input(IR_R) == True): #Both sides touch black line
                Motor_Stop()
                return

####################################################
##Function name Follow()
##Function performance Follow mode
##Entrance parameter：none
##Exit parameter：none
####################################################
def Follow(): 
        if(GPIO.input(IR_M) == True): #Middle sensor is OK
                if(GPIO.input(IRF_L) == False)&(GPIO.input(IRF_R) == False):    #Both sides detected obstacles at the same time
                        Motor_Stop()                    #stop
                if(GPIO.input(IRF_L) == False)&(GPIO.input(IRF_R) == True):   #Left sides detected obstacles
                        right()         #turn right
                if(GPIO.input(IRF_L) == True)& (GPIO.input(IRF_R) == False):  #Right sides detected obstacles
                        left()          #turn left
                if(GPIO.input(IRF_L) == True)& (GPIO.input(IRF_R) == True):   #Did not detect obstacles
                        forward()                       #straight
        else:
                Motor_Stop()


####################################################
##Function name ：Get_Distence()
##Function performance ultrasonic ranging，return distance(unit is meter）
##Entrance parameter：none
##Exit parameter：none
####################################################
def     Get_Distence():
        time.sleep(0.1)
        GPIO.output(TRIG,GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(TRIG,GPIO.LOW)
        while not GPIO.input(ECHO):
                                pass
        t1 = time.time()
        while GPIO.input(ECHO):
                                pass
        t2 = time.time()
        time.sleep(0.1)
        return (t2-t1)*340/2*100

####################################################
##Function name AvoidByRadar()
##Function performance ultrasonic obstacle avoidance function
##Entrance parameter ：none
##Exit parameter ：none
####################################################
def     AvoidByRadar(distance):
        dis = int(Get_Distence())
        if(distance<20):
                distance = 20                                   #The minimum obstacle avoidance distance is 20cm
        if((dis>1)&(dis < distance)):           #Obstacle distance value (in cm), greater than 1 is to avoid the blind spot of ultrasound
                Motor_Stop()
        
                
def     Avoid_wave():
        dis = Get_Distence()
        if dis<20:
                Motor_Stop()
        else:
                forward()

####################################################
##Function name
##Function performance Route() Path planning
##Entrance parameter：none
##Exit parameter：none
####################################################
def Route():
        global RevStatus
        global TurnAngle
        global Golength
        global left_speed
        global right_speed
        global left_speed_hold
        global right_speed_hold
        while RevStatus !=0 :
                print 'RevStatus==== %d ' %RevStatus
                TurnA=float(TurnAngle*6)/1000
                Golen=float(Golength*10)/1000
                print 'TurnAngle====== %f ' %TurnA
                print 'Golength======= %f ' %Golen
                #ENA_Speed(85)
                #ENB_Speed(85)
                if RevStatus==1:
                        left()
                        time.sleep(TurnA)
                        Motor_Stop()
                        forward()
                        time.sleep(Golen)
                        Motor_Stop()
                        RevStatus = 0
                        tcpCliSock.send("\xFF")
                        time.sleep(0.005)
                        tcpCliSock.send("\xA8")
                        time.sleep(0.005)
                        tcpCliSock.send("\x00")
                        time.sleep(0.005)
                        tcpCliSock.send("\x00")
                        time.sleep(0.005)
                        tcpCliSock.send("\xFF")
                        time.sleep(0.01)
                elif RevStatus==2:
                        right()
                        time.sleep(TurnA)
                        Motor_Stop()
                        forward()
                        time.sleep(Golen)
                        Motor_Stop()
                        RevStatus = 0
                        tcpCliSock.send("\xFF")
                        time.sleep(0.005)
                        tcpCliSock.send("\xA8")
                        time.sleep(0.005)
                        tcpCliSock.send("\x00")
                        time.sleep(0.005)
                        tcpCliSock.send("\x00")
                        time.sleep(0.005)
                        tcpCliSock.send("\xFF")
                        time.sleep(0.01)
                #ENA_Speed(left_speed_hold)
                #ENB_Speed(right_speed_hold)
####################################################
##Function name Send_Distance()
##Function performance：ultrasonic distance PC terminal display
##Entrance parameter：none                       
##Exit parameter：none
####################################################
def     Send_Distance():
        dis_send = int(Get_Distence())
        #dis_send = str("%.2f"%dis_send)
        if dis_send < 255:
                print 'Distance: %d cm' %dis_send
                tcpCliSock.send("\xFF")
                time.sleep(0.005)
                tcpCliSock.send("\x03")
                time.sleep(0.005)
                tcpCliSock.send("\x00")
                time.sleep(0.005)
                tcpCliSock.send(chr(dis_send))
                time.sleep(0.005)
                tcpCliSock.send("\xFF")
                time.sleep(0.1)


####################################################
##Function name Cruising_Mod()
##Function performance ：Mode change function
##Entrance parameter：none                       
##Exit parameter：none
####################################################
def     Cruising_Mod(func):
        #print 'into Cruising_Mod-01'
        global Pre_Cruising_Flag
        print 'Pre_Cruising_Flag %d '%Pre_Cruising_Flag
        
        global Cruising_Flag
        #print 'Cruising_Flag %d '%Cruising_Flag
        while True:
                if (Pre_Cruising_Flag != Cruising_Flag):                        
                        if (Pre_Cruising_Flag != 0):
                                Motor_Stop()
                        Pre_Cruising_Flag = Cruising_Flag
                        #print 'Pre_Cruising_Flag = Cruising_Flag == 0'
                if(Cruising_Flag == 1):         #infrared follow
                        Follow()
                elif (Cruising_Flag == 2):      #infrared trackline
                        TrackLine()
                elif (Cruising_Flag == 3):      #infrared obstacle avoidance
                        Avoiding()
                elif (Cruising_Flag == 4):      #ultrasonic obstacle avoidance##
                        Avoid_wave()
                elif (Cruising_Flag == 5):      #ultrasonic distance PC terminal display
                        Send_Distance()
                elif (Cruising_Flag == 6):      #ultrasonic obstacle avoidance 
                        AvoidByRadar(15)
                elif (Cruising_Flag == 7):
                        Route()
                elif (Cruising_Flag == 8):      #Exit camera tracking or enter debug mode
                        time.sleep(3)
                        #os.system('sh start_mjpg_streamer.sh')
                        call("sh start_mjpg_streamer.sh &",shell=True)
                        Cruising_Flag = 0
                elif (Cruising_Flag == 9):      #Enter the camera tracking
                        Path_Dect()
                elif (Cruising_Flag == 0):
                        RevStatus=0
                else:
                        time.sleep(0.001)
                time.sleep(0.001)
####################################################
##Function name Path_Dect()
##Function performance：Mode change function
##Entrance paramete ：FF130800FF，camera debug，FF130801FF start camera tracking
##Exit parameter  
#int Path_Dect_px       Average pixel coordinates
#int Path_Dect_on       1:start to track，0 stop tracking
####################################################
def     Path_Dect():
        global Path_Dect_px
        global Path_Dect_on
        while (Path_Dect_on):
                if Path_Dect_px < 260:
                        print("turn left")
                        Motor_TurnLeft()
                elif Path_Dect_px> 420:
                        print("turn right")
                        Motor_TurnRight()
                else :
                        print("go stright")
                        Motor_Forward()
                time.sleep(0.007)
                Motor_Stop()
                time.sleep(0.006)
####################################################
##Function name Path_Dect_img_processing()
##Function performance ：Mode change function
##Entrance parameter  ：FF130800FF，camera debug，FF130801FF start camera tracking
##Exit parameter 
#int Path_Dect_px       Average pixel coordinates
#int Path_Dect_on       1:start to track，0 debug mode/stop tracking
####################################################
def     Path_Dect_img_processing(func):
        global Path_Dect_px
        global Path_Dect_on
        Path_Dect_fre_count = 0
        Path_Dect_px_sum = 0
        Path_Dect_cap = 0
        print("into theads Path_Dect_img_processing")
        while True:
                if(Path_Dect_on):
                        if(Path_Dect_cap == 0):
                                cap = cv2.VideoCapture(0)
                                Path_Dect_cap = 1
                        else:
                                Path_Dect_fre_count+=1
                                ret,frame = cap.read()  #capture frame_by_frame
                                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #get gray img
                                ret,thresh1=cv2.threshold(gray,70,255,cv2.THRESH_BINARY)        #binaryzation 
                                for j in range(0,640,5):
                                        if thresh1[240,j] == 0:
                                                Path_Dect_px_sum = Path_Dect_px_sum + j
                                Path_Dect_px = Path_Dect_px_sum>>5
                                Path_Dect_px_sum = 0
                                Path_Dect_fre_count = 0
                elif(Path_Dect_cap):
                        Motor_Stop()
                        time.sleep(0.001)
                        Path_Dect_cap = 0
                        cap.relese()
                time.sleep(0.1)
####################################################
##Function name  Communication_Decode()
##Function performance：Communication protocol decoding  
##Entrance parameter：none
##Exit parameter：none
####################################################    
def Communication_Decode():
        global RevStatus
        global TurnAngle
        global Golength
        global Pre_Cruising_Flag
        global Cruising_Flag
        global motor_flag
        global left_speed
        global right_speed
        global left_speed_hold
        global right_speed_hold
        global Path_Dect_on
        print 'Communication_decoding...'
        if buffer[0]=='00':
                if buffer[1]=='01':                             #forward
                        Motor_Forward()
                        while s[0:len(s)-1] != "LED10": #left turn signal
                                s = str(serialArduino.readline())
                                serialArduino.write("LED10")
                        while s[0:len(s)-1] != "LED20": #right turn signal
                                s = str(serialArduino.readline())
                                serialArduino.write("LED20")
                        while s[0:len(s)-1] != "LED30": #rear light
                                s = str(serialArduino.readline())
                                serialArduino.write("LED30")
                        while s[0:len(s)-1] != "LED50": #brake light
                                s = str(serialArduino.readline())
                                serialArduino.write("LED50")
                                
                elif buffer[1]=='02':                   #backward
                        Motor_Backward()
                        while s[0:len(s)-1] != "LED10": #left turn signal
                                s = str(serialArduino.readline())
                                serialArduino.write("LED10")
                        while s[0:len(s)-1] != "LED20": #right turn signal
                                s = str(serialArduino.readline())
                                serialArduino.write("LED20")
                        while s[0:len(s)-1] != "LED31": #rear light
                                s = str(serialArduino.readline())
                                serialArduino.write("LED31")
                        while s[0:len(s)-1] != "LED50": #brake light
                                s = str(serialArduino.readline())
                                serialArduino.write("LED50")
                                
                elif buffer[1]=='03':                   #turn left
                        Motor_TurnLeft()
                        while s[0:len(s)-1] != "LED11": #left turn signal
                                s = str(serialArduino.readline())
                                serialArduino.write("LED11")
                        while s[0:len(s)-1] != "LED20": #right turn signal
                                s = str(serialArduino.readline())
                                serialArduino.write("LED20")
                        while s[0:len(s)-1] != "LED30": #rear light
                                s = str(serialArduino.readline())
                                serialArduino.write("LED30")
                        while s[0:len(s)-1] != "LED50": #brake light
                                s = str(serialArduino.readline())
                                serialArduino.write("LED50")
                elif buffer[1]=='04':                   #turn right
                        Motor_TurnRight()
                        while s[0:len(s)-1] != "LED10": #left turn signal
                                s = str(serialArduino.readline())
                                serialArduino.write("LED10")
                        while s[0:len(s)-1] != "LED21": #right turn signal
                                s = str(serialArduino.readline())
                                serialArduino.write("LED21")
                        while s[0:len(s)-1] != "LED30": #rear light
                                s = str(serialArduino.readline())
                                serialArduino.write("LED30")
                        while s[0:len(s)-1] != "LED50": #brake light
                                s = str(serialArduino.readline())
                                serialArduino.write("LED50")
                elif buffer[1]=='00':                   #stop
                        Motor_Stop()
                elif buffer[1]=='04':                   #turn right
                        Motor_TurnRight()
                        while s[0:len(s)-1] != "LED10": #left turn signal
                                s = str(serialArduino.readline())
                                serialArduino.write("LED10")
                        while s[0:len(s)-1] != "LED20": #right turn signal
                                s = str(serialArduino.readline())
                                serialArduino.write("LED20")
                        while s[0:len(s)-1] != "LED30": #rear light
                                s = str(serialArduino.readline())
                                serialArduino.write("LED30")
                        while s[0:len(s)-1] != "LED51": #brake light
                                s = str(serialArduino.readline())
                                serialArduino.write("LED51")
                else:
                        Motor_Stop()
                        while s[0:len(s)-1] != "LED10": #left turn signal
                                s = str(serialArduino.readline())
                                serialArduino.write("LED10")
                        while s[0:len(s)-1] != "LED20": #right turn signal
                                s = str(serialArduino.readline())
                                serialArduino.write("LED20")
                        while s[0:len(s)-1] != "LED30": #rear light
                                s = str(serialArduino.readline())
                                serialArduino.write("LED30")
                        while s[0:len(s)-1] != "LED51": #brake light
                                s = str(serialArduino.readline())
                                serialArduino.write("LED51")
        elif buffer[0]=='02':
                if buffer[1]=='01':#left side speed
                        speed=hex(eval('0x'+buffer[2]))
                        speed=int(speed,16)
                        ENA_Speed(speed)
                elif buffer[1]=='02':#right side speed
                        speed=hex(eval('0x'+buffer[2]))
                        speed=int(speed,16)
                        ENB_Speed(speed)
        elif buffer[0]=='01':
                if buffer[1]=='01':#1 servo drive
                        SetServoAngle(1,buffer[2])
                elif buffer[1]=='02':#2 servo drive
                        SetServoAngle(2,buffer[2])
                elif buffer[1]=='03':#3 servo drive
                        SetServoAngle(3,buffer[2])
                elif buffer[1]=='04':#4 servo drive
                        SetServoAngle(4,buffer[2])
                elif buffer[1]=='05':#5 servo drive
                        SetServoAngle(5,buffer[2])
                elif buffer[1]=='06':#6 servo drive
                        SetServoAngle(6,buffer[2])
                elif buffer[1]=='07':#7servo drive
                        SetServoAngle(7,buffer[2])
                elif buffer[1]=='08':#8 servo drive
                        SetServoAngle(8,buffer[2])
                else:
                        print '舵机角度大于170'
        elif buffer[0]=='13':
                if buffer[1]=='01':
                        Cruising_Flag = 1#Enter infrared follow mode
                        print 'Cruising_Flag红外跟随模式 %d '%Cruising_Flag
                elif buffer[1]=='02':#Enter infrared trackline mode
                        Cruising_Flag = 2
                        print 'Cruising_Flag红外巡线模式 %d '%Cruising_Flag
                elif buffer[1]=='03':#Enter infrared obstacle avoidance mode
                        Cruising_Flag = 3
                        print 'Cruising_Flag红外避障模式 %d '%Cruising_Flag
                elif buffer[1]=='04':#Enter infrared obstacle avoidance
                        Cruising_Flag = 4
                        print 'Cruising_Flag超声波壁障 %d '%Cruising_Flag
                elif buffer[1]=='05':#Enter ultrasonic distance PC terminal display
                        Cruising_Flag = 5
                        print 'Cruising_Flag超声波距离PC显示 %d '%Cruising_Flag
                elif buffer[1]=='06':
                        Cruising_Flag = 6
                        print 'Cruising_Flag超声波遥控壁障 %d '%Cruising_Flag
                elif buffer[1]=='07':
                        left_speed_hold=left_speed
                        right_speed_hold=right_speed
                        tcpCliSock.send("\xFF")
                        time.sleep(0.005)
                        tcpCliSock.send("\xA8")
                        time.sleep(0.005)
                        tcpCliSock.send("\x00")
                        time.sleep(0.005)
                        tcpCliSock.send("\x00")
                        time.sleep(0.005)
                        tcpCliSock.send("\xFF")
                        time.sleep(0.005)
                        Cruising_Flag = 7
                elif buffer[1]=='08':
                        if buffer[2]=='00':#Path_Dect 调试模式
                                Path_Dect_on = 0
                                Cruising_Flag = 8
                                print 'Cruising_Flag Path_Dect调试模式 %d '%Cruising_Flag
                                #os.system('sh start_mjpg_streamer.sh')
                        elif buffer[2]=='01':#Path_Dect 循迹模式
                                #os.system('sh stop_mjpg_streamer.sh')
                                call("sh stop_mjpg_streamer.sh &",shell=True)
                                time.sleep(2)
                                Path_Dect_on = 1
                                Cruising_Flag = 9
                                print 'Cruising_Flag Path_Dect循迹模式 %d '%Cruising_Flag
                elif buffer[1]=='00':
                        RevStatus=0
                        Cruising_Flag = 0
                        print 'Cruising_Flag正常模式 %d '%Cruising_Flag
                #else:
                        #Cruising_Flag = 0def send_angle(angle) : 
        elif buffer[0]=='a0':
                RevStatus=2
                Tangle=hex(eval('0x'+buffer[1]))
                Tangle=int(Tangle,16)
                TurnAngle=Tangle
                Golen=hex(eval('0x'+buffer[2]))
                Golen=int(Golen,16)
                Golength=Golen
        elif buffer[0]=='a1':
                RevStatus=1
                Tangle=hex(eval('0x'+buffer[1]))
                Tangle=int(Tangle,16)
                TurnAngle=Tangle
                Golen=hex(eval('0x'+buffer[2]))
                Golen=int(Golen,16)
                Golength=Golen
        elif buffer[0]=='40':
                temp=hex(eval('0x'+buffer[1]))
                temp=int(temp,16)
                print 'mode_flag====== %d '%temp
                motor_flag=temp
        elif buffer[0]=='32':           
                XRservo.XiaoRGEEK_SaveServo()
        elif buffer[0]=='33':           
                XRservo.XiaoRGEEK_ReSetServo()
        elif buffer[0]=='04':           #Switch mode FF040000FF turn on  FF040100FF turn off
                if buffer[1]=='00':
                        Open_Light()
                elif buffer[1]=='01':
                        Close_Light()
                else:
                        print 'error1 command!'
        elif buffer[0]=='05':           #Read Voltage FF050000FF
                if buffer[1]=='00':
                        Vol = XRservo.XiaoRGEEK_ReadVol()
                        print 'Read_Voltage %d '%Vol
                else:
                        print 'error2 command!'
        elif buffer[0]=='06':           #Read pluse FF060000FF read 1 pluse  FF060100FF read 2 pluse
                if buffer[1]=='00':
                        Speed1 = XRservo.XiaoRGEEK_SpeedCounter1()
                        print 'Read_Voltage %d '%Speed1
                elif buffer[1]=='01':
                        Speed2 = XRservo.XiaoRGEEK_SpeedCounter2()
                        print 'Read_Voltage %d '%Speed2
                else:
                        print 'error3 command!'
        elif buffer[0]=='09':           #Switch mode FF040000FF turn on  FF040100FF turn off
                if buffer[1]=='00':
                        Open_Buzer()
                elif buffer[1]=='01':
                        Close_Buzer()
                else:
                        print 'error1 command!'
        else:
                print 'error4 command!'


def uart_user(func):
        global ser
        print('serial test start ...')
        while True:
                Uart_rcv=ser.read()
                ser.write(Uart_rcv)



init_light()
while s[0:len(s)-1] != "LED10": #left turn signal
                                s = str(serialArduino.readline())
                                serialArduino.write("LED10")
while s[0:len(s)-1] != "LED20": #right turn signal
                                s = str(serialArduino.readline())
                                serialArduino.write("LED20")
while s[0:len(s)-1] != "LED30": #rear light
                                s = str(serialArduino.readline())
                                serialArduino.write("LED30")
while s[0:len(s)-1] != "LED51": #brake light
                                s = str(serialArduino.readline())
                                serialArduino.write("LED51")
while s[0:len(s)-1] != "LED00": #disable front light
        s = str(serialArduino.readline())
        serialArduino.write("LED00")
while s[0:len(s)-1] != "LED60": #disable red light wen front activated                                                                                  
        s = str(serialArduino.readline())
        serialArduino.write("LED60")

#define TCP server related variable
HOST='192.168.1.1'
PORT=2002
BUFSIZ=1
ADDR=(HOST,PORT)
rec_flag=0
i=0
buffer=[]
#start TCP server, monitor 2001 port
tcpSerSock=socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(1)
s = ""
threads = []
t1 = threading.Thread(target=Cruising_Mod,args=(u'模式切换',))
threads.append(t1)
t2 = threading.Thread(target=Path_Dect_img_processing,args=(u'图像处理',))
threads.append(t2)

time.sleep(2)
for t in threads:
                t.setDaemon(True)
                t.start()
                print 'theads stat...'
print 'all theads stat...'
while True:
    print 'waitting for connection...'
    tcpCliSock,addr=tcpSerSock.accept()
    print '...connected from:',addr
    while True:
        try:
            data=tcpCliSock.recv(BUFSIZ)
            data=binascii.b2a_hex(data)
        except:
            print "Error receiving:"
            break
        
        if not data:
            break
        if rec_flag==0:
            if data=='ff':  
                buffer[:]=[]
                rec_flag=1
                i=0
        else:
            if data=='ff':
                rec_flag=0
                if i==3:
                    print 'Got data',str(buffer)[1:len(str(buffer)) - 1],"\r"
                    Communication_Decode();
                i=0
            else:
                buffer.append(data)
                i+=1
        #print(binascii.b2a_hex(data))
    tcpCliSock.close()
Motor_Stop()
tcpSerSock.close()
    

