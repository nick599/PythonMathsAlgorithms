#Copyright Nick Prowse 2017. Code Licenced under Apache 2.
#Version 11. 21/10/2017.
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
#import cProfile
#import re
import time
import factorise

def main():
	prime_list_path="/home/mint/Desktop/"
	prime_list_filename="primes_upto_10000000.csv"
	primefile=prime_list_path + prime_list_filename

	print("Copyright Nick Prowse 2017. Code Licenced under Apache 2.")
	print("Version 11. 21/10/2017.")
	print("Programmed & tested in Python 2.76 only.")
	print("---------------------------------------------------------------------")
	print("This program tests factorise.py - time for factorising first M numbers supplied by user.")
	print("Results printed are stored in 2 lists - first for Number factorisations done upto, second for cumulatative time taken to factorise those numbers, third for average time.")
	print("Prime list file should be a .CSV file with each prime separated by commas.")
	print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used in factorise.py file.")
	print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997.")
	print("---------------------------------------------------------------------")
	print('what number do you want to test factorisations upto?')
	M = raw_input()
	s1 = time.clock()
	#print('s1 is: '+str(s1))
	print('Number input is: '+str(M))
	#print('type of M is: '+str(type(M)))
		
	#Convert M to a long
	M=long(M)

	s_before_number_checks = time.clock()

	#Simple Checks for M:
	print("Running checks on "+str(M))	
	if M==0:
		print('Number entered is 0. Please choose another number.')
		sys.exit()
	if M==1:
		print('1 is not a prime. Please choose another number.')
		sys.exit()
	if M<0:
		print('Number entered is negative. Please enter another number')
		sys.exit()

	c_number_checks = time.clock() - s_before_number_checks
	
	#Check if primefile exists.
	print('Checking if Prime file exists in location specified..')
	if os.path.exists(primefile) is False:
		#File doesn't exist in location. Exit process.
		print('Prime file doesn\'t exist in location specified. Exiting.')
		sys.exit()
	
	#only import primes <= sqrt(M)	
	# Largest number to consider primes upto is floor_sqrt_M
	print('Calculating floor of square root of '+str(M)+'..')
	s_before_floor_sqrt_M= time.clock()
	floor_sqrt_M=int(math.floor(math.sqrt(M)))	
	c_floor_sqrt_M = time.clock() - s_before_floor_sqrt_M	
	
	# Want to limit highest prime imported from csv to be <= math.sqrt(M)	
	print('Storing primes upto '+str(floor_sqrt_M)+' from csvfile..')
	s_before_primes = time.clock()
	primes=factorise.csvfile_store_primes(primefile,floor_sqrt_M)
	c_primes = int(10000 * (time.clock() - s_before_primes)) / 10000.0

	print('Running factorise_test ..')
	s_before_factorise_test = time.clock()
	result=factorise_test(M,primes)
	c_factorise_test = int(10000 * (time.clock() - s_before_factorise_test)) / 10000.0

	print('Collating results..')
	cumulative_time=int(10000 * result[0]) / 10000.0 #need to 4.d.p
	average_time=result[1] #no need to round
	check=result[2]
	cumul_check_time=int(10000 * result[3]) / 10000.0 #need to 4.d.p
	c_forloop=int(10000 * result[4]) / 10000.0 #need to 4.d.p
	cumul_add1toN=int(10000 * result[5]) / 10000.0 #need to 4.d.p
	cumul_R=int(10000 * result[6]) / 10000.0 #need to 4.d.p
	c_definerange=int(10000 * result[7]) / 10000.0 #need to 4.d.p
	cumul_pp_time=int(10000 * result[8]) / 10000.0 #need to 4.d.p
	cumul_nrem_time=int(10000 * result[9]) / 10000.0 #need to 4.d.p
	c_total_time = int(10000 * (time.clock() - s1)) / 10000.0 #need to 4.d.p

	print('-----------------------------')
	print('M is: '+str(M))
	print('Total time for main() algorithm to run: '+str(c_total_time)+' seconds')
	print('-----------------------------')
	#print('Total time taken for number_checks: '+str(c_number_checks)+' seconds')
	#print('Total time taken for floor_sqrt_M: '+str(c_floor_sqrt_M)+' seconds')
	print('Total time taken for prime list creation: '+str(c_primes)+' seconds')
	
	print('Total time taken for factorise_test(): '+str(c_factorise_test)+' seconds')
	print('-----------------------------')
	#print('Total time taken for define range in factorise_test(): '+str(c_definerange)+' seconds')
	print('Total time taken for for loop in factorise_test(): '+str(c_forloop)+' seconds')
	print('Total time taken for R calculation in factorise_test(): '+str(cumul_R)+' seconds')
	print('Total time taken for adding 1 to N in factorise_test(): '+str(cumul_add1toN)+' seconds')
	print('-----------------------------')
	print('Cumulative factorisation time is: '+str(cumulative_time)+' seconds')
	print('Average factorisation time is: '+str(average_time)+' seconds')
	#print('-----------------------------')
	#print('Total time taken - for loop - checks in factorise_test(): '+str(cumul_check_time)+' seconds')
	print('-----------------------------')
	print('Total time taken - calc primes powers in calc_primes_powers_remainder(): '+str(cumul_pp_time)+' seconds')
	print('Total time taken - N remainder in calc_primes_powers_remainder(): '+str(cumul_nrem_time)+' seconds')
	print('-----------------------------')
	print('Numbers that took >= 0.0003s to try to factorise are: '+str(check))

def factorise_test(M,primes):
	times=[]
	check=[]
	N=2
	cumulative_time=0
	r=0
	#cumul_ls_time=0
	#cumul_fs_time=0
	#cumul_ft_time=0
	cumul_check_time=0
	cumul_R=0
	cumul_add1toN=0
	cumul_pp_time=0
	cumul_nrem_time=0
	print("Looping through values from 2 to "+str(M)+"..")
	
	s_definerange = time.clock()
	number_range=tuple(xrange(2,M))
	c_definerange = time.clock() - s_definerange

	s_forloop = time.clock()
	for N in number_range:
		#print('N is now: '+str(N))
		s1 = time.clock()				
		b=factorise.factorise(N,primes)
		c_pp=b[5]
		cumul_pp_time = cumul_pp_time + c_pp
		c_nrem=b[6]
		cumul_nrem_time = cumul_nrem_time + c_nrem

		c1=time.clock() - s1
		cumulative_time = cumulative_time + c1
		
		s_check=time.clock()
		if c1 >= 0.0003:
			#append N to check[] list - values to look at
			check.append(N)
			#print('check is now: '+str(check))
		c_check = time.clock() - s_check
		cumul_check_time = cumul_check_time + c_check

		s_R = time.clock()
		R = float(N) / M				
		c_R = time.clock() - s_R
		cumul_R = cumul_R + c_R
		#update_progress(R)
		
		s_add1toN = time.clock()
		N = N + 1
		c_add1toN = time.clock() - s_check
		cumul_add1toN = cumul_add1toN + c_add1toN
		#raw_input('waiting for user to continue..')
	c_forloop = time.clock() - s_forloop
	average_time = cumulative_time / (M-1)
	return cumulative_time, average_time, check, cumul_check_time, c_forloop, cumul_R, cumul_add1toN, c_definerange, cumul_pp_time, cumul_nrem_time

if __name__=='__main__':
	main()

#def update_progress(progress):
#	barLength=2
#	status=""
#	if isinstance(progress,int):
#		progress=float(progress)
#	if not isinstance(progress, float):
#		progress=0
#		status="error: process variable must be a float\r\n"
#	if progress < 0:
#		progress = 0
#		status="Halt...\r\n"
#	if progress >= 1:
#		progress = 1
#		status="Done...\r\n"
#	block = int(round(barLength*progress))
#	text = "\rPercent: [{0}] {1}% {2}".format("="*block + " "*(barLength-block), progress*100, status)
#	return text

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
		
