from neo import Accel # import accelerometer
from time import sleep # to add delays

import string
import time
import os
import sys
import math

virtualSensorName = 'tablePresence'
	
#########################
th = 98
windowTime = 30
falsePositiveRatio = 0.016
maxTh = 155
cycleDelay = 0.01
timerMax = 5
#########################

status = 0
presence = 0
prevPresence = 0
counter = 0

def printVS( data ):
	global status
	data = str(data).strip()		
	print data
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
	

def resetTimer():
	global counter
	counter = timerMax * (1/cycleDelay)
	sleep(1)
	print "counter reset"


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

max = 0;

while True: # Run forever
	
	max = 0
	
	accelVals = accel.get() 
	
	## evaluate max
	if abs( accelVals[0] - mean[0] ) > maxTh:
		resetTimer()
	elif abs( accelVals[1] - mean[1] ) > maxTh:
		resetTimer()
	elif abs( accelVals[2] - mean[2] ) > maxTh:
		resetTimer()	

	sleep(cycleDelay)

	if counter > 0 :
		counter = counter - 1	
		presence = 1
	elif counter == 1 :
		presence = 1
		print "ready to zero"
	else:
		presence = 0
	
	if prevPresence != presence:
		printVS(presence)
		prevPresence = presence
		print str(time.time())	 + "Update Virtual Sensor - value: " + str(presence) 