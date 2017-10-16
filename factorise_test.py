#Copyright Nick Prowse 2017. Code Licenced under Apache 2.
#Version 3. 11/10/2017.
#Programmed & tested in Python 2.76 only
#This program tests factorise.py - time for factorising first 1*10^20 numbers.
#Results printed are ...
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 50,000 and took ... seconds.

import sys
import math
import csv
import os.path
import cProfile
import re

print("Copyright Nick Prowse 2017. Code Licenced under Apache 2.")
print("Version 3. 11/10/2017.")
print("Programmed & tested in Python 2.76 only.")
print("---------------------------------------------------------------------")
print("This program tests factorise.py - time for factorising first 1*10^20 numbers.")
print("Results printed are ...")
print("Prime list file should be a .CSV file with each prime separated by commas.")
print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used.")
print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 100,000,000 and took ... seconds.")
print("---------------------------------------------------------------------")

def main():
	print('what number do you want to test factorisations upto?')
	M=raw_input()

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

	result=factorise_test(M)
	N_values=result[0]	
	primepower_factorisations=result[1] 
	times=result[2]
	print('N_values are: '+str(N_values))
	print('primepower_factorisations are: '+str(primepower_factorisations))
	print('times are: '+str(times))

def factorise_test(M):
	N_values=[]
	primepower_factorisations=[]	
	times=[]
	N=3
	while N in xrange(3,M): 
		start_time= time.clock()				
		print('N is now: '+str(N))
		b=factorise.factorise(N)
		print('primepower factorisation is now: '+str(b))
		c=time.clock() - start_time
		print('time taken is: '+str(c))
		N_values.append(N)
		primepower_factorisations.append(b)
		times.append(c)
		raw_input('waiting for user to continue..')
	return N_values, primepower_factorisations, times

if __name__=='__main__':
	main()


