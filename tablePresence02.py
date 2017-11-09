from neo import Accel # import accelerometer
from time import sleep # to add delays

import string
import time
import os
import sys
import math

virtualSensorName = 'tablePresence'

	
#########################

th = 35
windowTime = 2
falsePositiveRatio = 0.075
maxThDelta = 30
cycleDelay = 0.005
meanCycles = 1000
subMeanCycles = 5

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

def magnitude(x,y,z):
	p = x*x +y*y + z*z
	return math.sqrt(p)

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

print "calculating bias..."
mean = 0	
for x in range (0, meanCycles):
	accelVals = accel.get() 
	
	mag = magnitude( accelVals[0], accelVals[1], accelVals[2])
	mean = mean + mag
	sleep(cycleDelay)

mean = mean / meanCycles
print "bias calculated: " + str(mean) 

maxTh = mean + maxThDelta

cycles = windowTime * (1/cycleDelay)
noiseTh = falsePositiveRatio * cycles

print "accelerometer treshold = " + str(th)
print "maximum treshold = " + str(maxTh)
print "False Positive Ratio = " + str(falsePositiveRatio)
print "windowTime = " + str(windowTime)
print "noiseTh = " + str(noiseTh)

max = 0;

while True: # Run forever

	presence = 0
	max = 0
	
	for x in range(0, int(cycles)):
		subMean = 0
		for x in range (0, subMeanCycles):
			accelVals = accel.get() 
	
			mag = magnitude( accelVals[0], accelVals[1], accelVals[2])
			subMean = subMean + mag
			sleep(cycleDelay)

		mag = subMean / subMeanCycles

		#accelVals = accel.get() 
		#mag = magnitude( accelVals[0], accelVals[1], accelVals[2])
	
		if abs( mag  ) > th:
			presence = presence + 1

		## evaluate max
		if abs( mag  ) > max:
			max = mag 

		print mag
		#sleep(cycleDelay)

	print "-------WINDOW-------" + str(presence) + "     max acc value: " + str(max)

	if presence > noiseTh or max > maxTh:
		presence = 1
	else:
		presence = 0
	
	if prevPresence != presence:
		printVS(presence)
		prevPresence = presence
		print str(time.time())	 + "Update Virtual Sensor - value: " + str(presence) 