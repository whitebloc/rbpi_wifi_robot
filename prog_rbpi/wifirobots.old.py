#coding:utf-8
'''
Raspberry Pi WiFi video robot car drive souce code
Writer: liuviking
Copyright:Kuman Tech
The code can be used free,but not for commerce purpose.
All rights reserved, unauthorized use will be prosecuted by Kuman! 
'''

from socket import *
from time import ctime
import binascii
import RPi.GPIO as GPIO
import time
import threading

print '....WIFIROBOTS START!!!...'


#######################################
#############Signal pin defination##############
#######################################
GPIO.setmode(GPIO.BCM)

########LED prot defination#################
LED0 = 10
LED1 = 9
LED2 = 25

########Morot drive port defination#################
ENA = 13	#//L298 Enalbe A
ENB = 20	#//L298 Enable B
IN1 = 19	#//Motor port 1
IN2 = 16	#//Motor port 2
IN3 = 21	#//Motor port 3
IN4 = 26	#//Motor port 4

########Servo port defination#################
SER1 = 11	#Servo1
SER2 = 8	#Servo2
SER3 = 7	#Servo3
SER4 = 5	#Servo4
SER7 = 6	#Vertical servo  port servo7 
SER8 = 12	#Horizontal servo port servo8

########Ultrasonic port defination#################
ECHO = 4	#Ultrasonic receiving foot position  
TRIG = 17	#Ultrasonic sending foot position

########Infrared sensor port defination#################
IR_R = 18	#Right line following infrared sensor
IR_L = 27	#Left line following infrared sensor
IR_M = 22	#Middle obstacle avoidance infrared sensor
IRF_R = 23	#Right object tracking infrared sensror
IRF_L = 24	#Left object tracking infrardd sensor
global Cruising_Flag
Cruising_Flag = 0	#//Current circulation mode
global Pre_Cruising_Flag
Pre_Cruising_Flag = 0 	#//Precycling mode
Left_Speed_Hold = 255	#//Define left speed variable
Right_Speed_Hold = 255	#//Define right speed variable
buffer = ['00','00','00','00','00','00']

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
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)



#########Infrared initialized to input，and internal pull up#########
GPIO.setup(IR_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_M,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IRF_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IRF_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)


#GPIO.output(ENA,True)
#GPIO.output(ENB,True)

##########Ultrasonic module pin type set#########
GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW)#ultrasonic module transmitting end pin set trig
GPIO.setup(ECHO,GPIO.IN,pull_up_down=GPIO.PUD_UP)#ultrasonic module receiving end pin set echo

##########Servo pin type set#########

GPIO.setup(SER1,GPIO.OUT)#Servo1
GPIO.setup(SER2,GPIO.OUT)#Servo2
GPIO.setup(SER3,GPIO.OUT)#Servo3
GPIO.setup(SER4,GPIO.OUT)#Servo4
GPIO.setup(SER7,GPIO.OUT)#Horizontal servo port servo7
GPIO.setup(SER8,GPIO.OUT)#Vertical servo port servo8
Servo7=GPIO.PWM(SER7,50) #50HZ  
Servo7.start(0)  
Servo8=GPIO.PWM(SER8,50) #50HZ  
Servo8.start(0)  


####################################################
##Functin name Open_Light()
##Function performance Open headlight LED0
##Entrance parameter ：none
##Exit parameter：none
####################################################
def	Open_Light():#turn on headlight LED0
	GPIO.output(LED0,False)#Headlight's anode to 5V, cathode to IO port
	time.sleep(1)

####################################################
##Function name Close_Light()
##Function performance Close headlight
##Enterance parameter：无none
##Exit parameter：无 none
####################################################
def	Close_Light():#Close headlight
	GPIO.output(LED0,True)#Headlight's anode to 5V, cathode to IO port
	time.sleep(1)
	
####################################################
##Function name init_light()
##Function performance running light
##Enterance parameter：none
##Exit parameter：none
####################################################
def	init_light():#running light
	GPIO.output(LED0,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED1,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,False)#Headlight's anode to 5V, cathode to IO port
	time.sleep(0.5)
	GPIO.output(LED0,True)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED1,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,False)#Headlight's anode to 5V, cathode to IO port
	time.sleep(0.5)
	GPIO.output(LED0,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED1,True)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,False)#Headlight's anode to 5V, cathode to IO port
	time.sleep(0.5)
	GPIO.output(LED0,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED1,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,True)#Headlight's anode to 5V, cathode to IO port
	time.sleep(0.5)
	GPIO.output(LED0,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED1,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,False)#Headlight's anode to 5V, cathode to IO port
	time.sleep(0.5)
	GPIO.output(LED0,True)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED1,True)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,True)#Headlight's anode to 5V, cathode to IO port
##########Robot's direction control###########################
def Motor_Forward():
	print 'motor forward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
	GPIO.output(LED1,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,False)#Headlight's anode to 5V, cathode to IO port
	
def Motor_Backward():
	print 'motor_backward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
	GPIO.output(LED1,True)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,False)#Headlight's anode to 5V, cathode to IO port
	
def Motor_TurnLeft():
	print 'motor_turnleft'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
	GPIO.output(LED1,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,True)#Headlight's anode to 5V, cathode to IO port
def Motor_TurnRight():
	print 'motor_turnright'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
	GPIO.output(LED1,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,True)#Headlight's anode to 5V, cathode to IO port
def Motor_Stop():
	print 'motor_stop'
	GPIO.output(ENA,False)
	GPIO.output(ENB,False)
	GPIO.output(IN1,False)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,False)
	GPIO.output(LED1,True)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,True)#Headlight's anode to 5V, cathode to IO port



#Servo angle drive function   
def SetServo7Angle(angle_from_protocol):
	angle=hex(eval('0x'+angle_from_protocol))
	angle=int(angle,16)
	Servo7.ChangeDutyCycle(2.5 + 10 * angle / 180) #set horizontal servo rotation angle
	GPIO.output(LED0,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED1,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,True)#Headlight's anode to 5V, cathode to IO port
	time.sleep(0.01)
	GPIO.output(LED0,True)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED1,True)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,True)#Headlight's anode to 5V, cathode to IO port
def SetServo8Angle(angle_from_protocol):
	angle=hex(eval('0x'+angle_from_protocol))
	angle=int(angle,16)
	Servo8.ChangeDutyCycle(2.5 + 10 * angle / 180) #Set vertical servo rotation angel
	GPIO.output(LED0,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED1,True)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,False)#Headlight's anode to 5V, cathode to IO port
	time.sleep(0.01)
	GPIO.output(LED0,True)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED1,True)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,True)#Headlight's anode to 5V, cathode to IO port


####################################################
##Function name：Avoiding()
##Function performance：Infrared obstacle avoidance function
##Entrance parameter：none
##Exit parameter：none
####################################################
def	Avoiding(): #infrared obstacle avoidance
	if GPIO.input(IR_M) == False:
		Motor_Stop()
		return
	else:
		Motor_Forward()
		return

####################################################
##Function name FollowLine()
##Function performance Black line following
##Entrance parameter：none
##Exit parameter：none
####################################################
def FollowLine():
	if (GPIO.input(IR_L) == False)&(GPIO.input(IR_R) == False): #Black line is high, ground is low
		Motor_Forward()
		return
	elif (GPIO.input(IR_L) == False)&(GPIO.input(IR_R) == True):
		Motor_TurnRight()
		return
	elif (GPIO.input(IR_L) == True)&(GPIO.input(IR_R) == False):
		Motor_TurnLeft()
		return
	elif (GPIO.input(IR_L) == True)&(GPIO.input(IR_R) == True): #Both sides touch black line
		Motor_Stop()
		return

####################################################
##Function name：Get_Distence()
##Function performanceultrasonic ranging，return distance(unit is meter）
##Entrance parameter：none
##Exit parameter：none
####################################################
def	Get_Distence():
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
	return (t2-t1)*340/2

####################################################
##Function name Avoid_wave()
##Function performance ultrasonic obstacle avoidance function
##Entrance parameter ：none
##Exit parameter ：none
####################################################
def	Avoid_wave():
	dis = Get_Distence()
	if dis<0.15:
		Motor_Stop()
	else:
		Motor_Forward()

####################################################
##Function name Send_Distance()
##Function performance：ultrasonic distance PC terminal display
##Entrance parameter：none			
##Exit parameter：noe
####################################################
def	Send_Distance():
	dis_send = Get_Distence()
	if dis < 4:
		print 'Distance: %0.3f m' %dis_send
		time.sleep(1)


def	Cruising_Mod(func):
	print 'into Cruising_Mod-01'
	global Pre_Cruising_Flag
	print 'Pre_Cruising_Flag %d '%Pre_Cruising_Flag
	
	global Cruising_Flag
	print 'Cruising_Flag %d '%Cruising_Flag
	while True:
		if (Pre_Cruising_Flag != Cruising_Flag):			
			if (Pre_Cruising_Flag != 0):
				Motor_Stop()
			Pre_Cruising_Flag = Cruising_Flag
			print 'Pre_Cruising_Flag = Cruising_Flag == 0'
		if(Cruising_Flag == 2):	#enter infrared line following mode
			FollowLine()
		elif (Cruising_Flag == 3):	#Enter infrared obstacle avoidance
			Avoiding()
		elif (Cruising_Flag == 4):	#Enter ultrasonic obstacle avoidance
			Avoid_wave()
		else:
			time.sleep(0.001)
		time.sleep(0.001)







    
#Communication protocol decoding  
def Communication_Decode():
	global Pre_Cruising_Flag
	global Cruising_Flag
	print 'Communication_decoding...'
	if buffer[0]=='00':
		if buffer[1]=='01':			#forward	
			Motor_Forward()
		elif buffer[1]=='02':			#backward
			Motor_Backward()
		elif buffer[1]=='03':			#turn left
			Motor_TurnLeft()
		elif buffer[1]=='04':			#turn right
			Motor_TurnRight()
		elif buffer[1]=='00':			#stop
			Motor_Stop() 
		else:
			Motor_Stop()
	elif buffer[0]=='01':
		if buffer[1]=='07':#Servo 7 drive
			SetServo7Angle(buffer[2])
		elif buffer[1]=='08':#Servo 8 drive
			SetServo8Angle(buffer[2])
	elif buffer[0]=='13':
		if buffer[1]=='02':
			Cruising_Flag = 2#Enter infrared line following mode
			print 'Cruising_Flag change %d '%Cruising_Flag
		elif buffer[1]=='03':#Enter infrared obstacle avoidance mode
			Cruising_Flag = 3
			print 'Cruising_Flag change %d '%Cruising_Flag
		elif buffer[1]=='04':#enter ultrasonic avoidance mode
			Cruising_Flag = 4
			print 'Cruising_Flag change %d '%Cruising_Flag
		elif buffer[1]=='00':
			Cruising_Flag = 0
			print 'Cruising_Flag change%d '%Cruising_Flag
		#else:
			#Cruising_Flag = 0
	elif buffer[0]=='05':
		if buffer[1]=='00':
			Open_Light()
		elif buffer[1]=='01':
			Close_Light()
		else:
			print '...'
	else:
		print '...'
            



init_light()

#define TCP server related variable
HOST=''
PORT=2001
BUFSIZ=1
ADDR=(HOST,PORT)
rec_flag=0
i=0
buffer=[]
#start TCP server, monitor 2001 port
tcpSerSock=socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(1)

threads = []
t1 = threading.Thread(target=Cruising_Mod,args=(u'monitor',))
threads.append(t1)

for t in threads:
		t.setDaemon(True)
		t.start()

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
tcpSerSock.close()
    

