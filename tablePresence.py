from neo import Accel # import accelerometer
from time import sleep # to add delays

import string
import time
import os
import sys

virtualSensorName = 'tablePresence'

	
#########################

th = 98
windowTime = 30
falsePositiveRatio = 0.016
maxTh = 155
cycleDelay = 0.01

#########################



status = 0
presence = 0
prevPresence = 0

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

	presence = 0
	max = 0
	
	for x in range(0, int(cycles)):

		accelVals = accel.get() 
	
		if abs( accelVals[0]   - mean[0] ) > th:
			#print "presence" + str(time.time())
			#dot()
			presence = presence + 1
		elif abs( accelVals[1] - mean[1] ) > th:
			#print "presence" + str(time.time())
			#dot()
			presence = presence + 1
		elif abs( accelVals[2] - mean[2] ) > th:
			#print "presence" + str(time.time())	
			#dot()
			presence = presence + 1
		#else:
			#presence = 0

## evaluate max
		if abs( accelVals[0]   - mean[0] ) > max:
			max = accelVals[0]   - mean[0]

		if abs( accelVals[1]   - mean[1] ) > max:
			max = accelVals[1]   - mean[1]

		if abs( accelVals[2]   - mean[2] ) > max:
			max = accelVals[2]   - mean[2]
#################

		sleep(cycleDelay)

	print "-------WINDOW-------" + str(presence) + "     max acc value: " + str(max)

	if presence > noiseTh or max > maxTh:
		presence = 1
	else:
		presence = 0
	
	if prevPresence != presence:
		printVS(presence)
		prevPresence = presence
		print str(time.time())	 + "Update Virtual Sensor - value: " + str(presence) 