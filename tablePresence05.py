from neo import Accel # import accelerometer
from time import sleep # to add delays

import string
import time
import os
import sys
import math
from time import gmtime, strftime

virtualSensorName = 'tablePresence'
	
#########################
th = 98
windowTime = 30
falsePositiveRatio = 0.016
maxTh = 140
cycleDelay = 0.01
timerMax = 300
#########################

status = 0
presence = 0
prevPresence = 0
counter = 0

def printVS( data ):
	global status
	data = str(data).strip()		
	print str(strftime("%Y-%m-%d %H:%M:%S", gmtime())) + "  Update Virtual Sensor - value: " + str(data)
	dataIot = open(directory + file, "w")
	dataIot.write(str(status) + ',' + data)
	dataIot.flush()
	dataIot.close()
	if status == 0 :
		status = 1
	elif status == 1:
		status = 0

def dot():
	sys.stdout.write('.')
	sys.stdout.flush()
	

def resetTimer(val):
	global counter
	counter = timerMax * (1/cycleDelay)
	sleep(1)
	print str(strftime("%Y-%m-%d %H:%M:%S", gmtime())) + "  TImer reset - Value: " + str(val)


file = 'data'
directory = '/sensors/'+ virtualSensorName +'/'
print 'Checking directory exists ...'
if not os.path.exists(directory):
	print 'Directory does not exists... creating... '
	try:
		os.makedirs(directory)
		print 'OK'
	except OSError as e:
		print 'NO \n ERROR:' + e
		exit()
else:
	print 'OK'


accel = Accel()
accel.calibrate()

mean = [0,0,0]
	
for x in range (0, 20):
	accelVals = accel.get() 
	mean[0] = mean[0] + accelVals[0]
	mean[1] = mean[1] + accelVals[1]
	mean[2] = mean[2] + accelVals[2]
	sleep(0.02)

mean[0] = mean[0] / 20
mean[1] = mean[1] / 20
mean[2] = mean[2] / 20	

print "average calculated"

cycles = windowTime * (1/cycleDelay)
noiseTh = falsePositiveRatio * cycles

print "accelerometer treshold = " + str(th)
print "False Positive Ratio = " + str(falsePositiveRatio)
print "windowTime = " + str(windowTime)
print "noiseTh = " + str(noiseTh)

# Set the presence at 0 at boot
printVS(0)

#First Read
accelVals = accel.get() 
prevModulus = math.sqrt((accelVals[0]*accelVals[0]) + (accelVals[1]*accelVals[1]) + (accelVals[2]*accelVals[2]))

while True: # Run forever
	
	accelVals = accel.get() 
	modulus = math.sqrt((accelVals[0]*accelVals[0]) + (accelVals[1]*accelVals[1]) + (accelVals[2]*accelVals[2]))

	diff = abs(modulus - prevModulus)

	## evaluate max
	if abs( diff ) > maxTh:
		resetTimer( diff )
	elif abs( diff ) > maxTh:
		resetTimer( abs( diff ))
	elif abs( diff ) > maxTh:
		resetTimer(abs( diff ))	

	sleep(cycleDelay)

	if counter > 0 :
		counter = counter - 1	
		presence = 1
	else:
		presence = 0
	

	if prevPresence != presence:
		printVS(presence)
		prevPresence = presence 