
#Copyright Nick Prowse 2017. Code Licenced under Apache 2.
#Version 7. 18/10/2017.
#Programmed & tested in Python 2.76 only
#This program tests factorise.py - time for factorising first 1*10^20 numbers.
#Results are: Number input, average_time of factorisations, cumulative_time of factorisations, and total time for algorithm.
#Ensure that "prime_list_path" and "prime_list_filename" are edited for the location of prime list file used in factorise.py file.
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997. 
#For M = 10^4, cumulative_time is < 0.1 seconds, and total algorithm time is < 2 seconds. 
#For M = 10^5, cumulative_time is < 1.9 seconds, and total algorithm time is < 60 seconds. 

import sys
import math
import os.path
import cProfile
import re
import time
import factorise

def main():
	prime_list_path="/home/mint/Desktop/"
	prime_list_filename="primes_upto_10000000.csv"
	primefile=prime_list_path + prime_list_filename

	print("Copyright Nick Prowse 2017. Code Licenced under Apache 2.")
	print("Version 7. 18/10/2017.")
	print("Programmed & tested in Python 2.76 only.")
	print("---------------------------------------------------------------------")
	print("This program tests factorise.py - time for factorising first M numbers supplied by user.")
	print("Results printed are stored in 2 lists - first for Number factorisations done upto, second for cumulatative time taken to factorise those numbers, third for average time.")
	print("Prime list file should be a .CSV file with each prime separated by commas.")
	print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used in factorise.py file.")
	print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997.")
	print("---------------------------------------------------------------------")
	print('what number do you want to test factorisations upto?')
	M=raw_input()
	s2= time.clock()
	print('Number input is: '+str(M))
	#print('type of M is: '+str(type(M)))
		

	#Convert M to a long
	M=long(M)

	#Simple Checks for M:
	if M==0:
		print('Number entered is 0. Please choose another number.')
		sys.exit()
	if M==1:
		print('1 is not a prime. Please choose another number.')
		sys.exit()
	if M<0:
		print('Number entered is negative. Please enter another number')
		sys.exit()

	#Check if primefile exists.
	#print('Checking if Prime file exists in location specified..')
	if os.path.exists(primefile) is False:
		#File doesn't exist in location. Exit process.
		print('Prime file doesn\'t exist in location specified. Exiting.')
		sys.exit()

	#only import primes <= sqrt(M)	
	# Largest number to consider primes upto is floor_sqrt_M
	floor_sqrt_M=int(math.floor(math.sqrt(M)))	

	# Want to limit highest prime imported from csv to be <= math.sqrt(M)	
	primes=factorise.csvfile_store_primes(primefile,floor_sqrt_M)

	# M = 10
	print('Running factorise_test ..')
	result=factorise_test(M,primes)
	#M=result[0]	
	primepower_factorisations=result[1] 
	cumulative_time=result[2]
	average_time=result[3]
	check=result[4]
	#print('N_values are: '+str(N_values))
	c2=time.clock() - s2
	print('-----------------------------')
	print('M is: '+str(M))
	#print('primepower_factorisations are: '+str(primepower_factorisations))
	print('Cumulative factorisation time is: '+str(cumulative_time))
	print('Average factorisation time is: '+str(average_time))
	print('Numbers that took more than 2s to try to factorise are: '+str(check))
	print('Total time for algorithm to run: '+str(c2))

def factorise_test(M,primes):
	print("Running checks on M")	
	factorise.number_checks(M)
	# M = 10 
	N_values=[]
	primepower_factorisations=[]	
	times=[]
	check=[]
	N=2
        #c=0
	cumulative_time=0
	r=0
	print("Looping through N values..")
	while N in xrange(2,M): 
		s1= time.clock()				
		#print('N is now: '+str(N))
		b=factorise.factorise(N,primes)
		#print('primepower factorisation is now: '+str(b))
		c1=time.clock() - s1
		#print('time taken is: '+str(c))
		#N_values.append(N)
		#primepower_factorisations.append(b)
		times.append(c1)
		cumulative_time = cumulative_time + c1
		if c1 >= 0.05:
			#append N to check[] list - values to look at
			check.append(N)
			#print('check is now: '+str(check))

		#print('cumulative time is: '+str(cumulative_time))
		#print('average_time time is: '+str(average_time))
		#print('------------------------')
		#R = int(math.floor(float(N) / M))		
		
		R = float(N) / M				
		#update_progress(R)
		
		N = N + 1
		#raw_input('waiting for user to continue..')
	average_time = cumulative_time / (M-1)
	return M, primepower_factorisations, cumulative_time, average_time, check

def update_progress(progress):
	barLength=2
	status=""
	if isinstance(progress,int):
		progress=float(progress)
	if not isinstance(progress, float):
		progress=0
		status="error: process variable must be a float\r\n"
	if progress < 0:
		progress = 0
		status="Halt...\r\n"
	if progress >= 1:
		progress = 1
		status="Done...\r\n"
	block = int(round(barLength*progress))
	text = "\rPercent: [{0}] {1}% {2}".format("="*block + " "*(barLength-block), progress*100, status)
	return text

if __name__=='__main__':
	main()

#def drawProgressBar(percent, barLen = 10):
#	sys.stdout.write('\r')
#	progress=""
#	for i in xrange(barLen):
#		if i < int(barLen * percent):
#			progress += "="
#		else:
#			progress += " "
#	sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
#	sys.stdout.flush()

#sys.stdout.write('\r')		
		#sys.stdout.write("[%-20s] %d%%" % ('='*R, 5*R))
		#sys.stdout.flush()



		#if r>0:
		#	#Write over previous line and call drawProgressBar
		#	sys.stdout.write('\r')			
		#	drawProgressBar(R,M)
		#	r=r+1
		#else:
		#	#Don't call drawProgressBar on first run
		#	sys.stdout.write('\r')
		#	r=r+1
		# M is 10
		#total=M-1 # total = 9
		#print('total is: '+str(total))
		#point=float(total)/100 #point = 0.09
		#print('point is: '+str(point))
		#increment=float(total)/10 #increment = 0.9
		#print('increment is: '+str(increment))
		
		#for i in xrange(total): # xrange(9)
		#	if (i % (5 * point) == 0):
		#	#1st loop i=0, 5*point=
		#		sys.stdout.write("\r[" + "=" * (i / increment)+ " " * ((total - i)/increment) + "]" + str(i / point) + "%")
		
