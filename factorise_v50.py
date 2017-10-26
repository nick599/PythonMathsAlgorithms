#Copyright Nick Prowse 2017. Code Licenced under Apache 2.
#Version 50. 25/10/2017.
#Programmed & tested in Python 2.76 only
#This program attemps to import a prime list, and use the primes to factorise a number N. 
#Results printed are three arrays - first for prime factors, second for powers of those primes, third for any remainder (where a larger prime list is needed).
#Prime list file should be a .CSV file with each prime separated by commas.
#Ensure that "prime_list_path" and "prime_list_filename" are edited for the location of prime list file used.
#The larger the prime file is that is used, the longer the factorisation will take!
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to factorise most numbers under 2.5x10^9 in 1 second.

import sys
import math
import csv
import os
import itertools
import time
	
def main():
	prime_list_path="/home/mint/Desktop/"
	prime_list_filename="primes_upto_10000.csv"
	primefile=prime_list_path + prime_list_filename

	print("Copyright Nick Prowse 2017. Code Licenced under Apache 2.")
	print("Version 50. 25/10/2017.")
	print("Programmed & tested in Python 2.76 only.")
	print("---------------------------------------------------------------------")
	print("This program attemps to import a prime list, and use the primes to factorise a number specified by user.")
	print("Results printed are three arrays - first for prime factors, second for powers of those primes, third for any remainder (where a larger prime list is needed).")
	print("Prime list file should be a .CSV file with each prime separated by commas.")
	print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used.")
	print("The larger the prime file is that is used, the longer the factorisation will take!")
	print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to factorise most numbers under 2.5x10^9 in 1 second.")
	print("---------------------------------------------------------------------")
	
	#Check if primefile exists.
	if os.path.exists(primefile) is False:
		#File doesn't exist in location. Exit process.
		print('Prime file doesn\'t exist in location specified. Exiting.')
		sys.exit()

	print('Number to attempt to factorise?')
	N_initial = raw_input()
	if N_initial.isdigit() is False:
		print('You have not entered an integer. Please reenter.')
		sys.exit()

	#now convert type for N into a long:
	N = long(N_initial)

	#call number_checks() for simple checks on input 
	number_checks(N)	
	
	#Call size_input_check() if want to stop program running for very large numbers 
	#size_input_check()

	#initialise primes list & tuples	
	primes=[]
	prime_factors=()
	powers=()
	remainder=()

	#generate primes list
	print('Generating primes list..')
	primes=csvfile_store_primes(primefile)
	#result=csvfile_store_primes(primefile)
	
	#primes=result[0]

	#print primes # 2
	#print type(primes) # int
	#print('primes[0] is: '+str(primes[0]))
	#print('type of primes[0] is: '+str(type(primes[0])))

	#check if N is in primes - if it is, no need to factorise!
	#print('checking if '+str(N)+' is in primes..')
	#print('type of N is: '+str(type(N)))
	if N in primes:
		print(str(N)+' is in primes list..')
		prime_factors=(N)
		powers=(1)
		remainder=()
	else:
		print(str(N)+' is not in primes list..')

		# Largest number to consider primes upto is floor_sqrt_N
		floor_sqrt_N=int(math.floor(math.sqrt(N)))
		print('floor_sqrt_N is: '+str(floor_sqrt_N))	
		print('Largest number to consider primes upto is: '+str(floor_sqrt_N))

		# isliced_primes: those primes such that highest prime imported from csv  <= math.sqrt(N)	
		if floor_sqrt_N == 1:
			#Hence N must be 2 or 3.			
			#just use value of N			
			b=max_element_below_or_equal_target(primes,N)
		else:
			b=max_element_below_or_equal_target(primes,floor_sqrt_N)
	
		print 'Number of primes to extract from list is: '+str(b)

		#Reset to start of csvfile 
		#csvfile.seek(0)	

		#iSlice prime list using b
		print 'Obtaining isliced_primes from imported list..'
		if b>=1:	
			isliced_primes=tuple(itertools.islice(primes,b))
			print('isliced_primes are: '+str(isliced_primes))		
		elif b==0:		
			print('b is 0 !!!')
			isliced_primes=tuple("")
			#print('isliced_primes are: '+str(isliced_primes))
		
		#isliced_primes=result[1]

		# Now call factorise() function
		result2=factorise(N,isliced_primes)

		prime_factors=result2[0]
		powers=result2[1]
		remainder=result2[2]
	print('factorisation is..')
	print prime_factors, powers, remainder

def csvfile_store_primes(csv_filename_var):

	with open(csv_filename_var,'r') as csvfile:
		# Want to limit highest prime imported from csv to be <= math.sqrt(N)
		# Need to get index of the highest prime <= math.sqrt(N)
		# Strip quotes, eol chars etc, and convert strings to integers	
		#print('Storing primes in Prime file into primes list...')

		#Use generator to get number of primes to use in prime file..
		print 'Running generator..'
		z1=(int(x) for row in csv.reader(csvfile) for x in row)
		primes=list(z1)	
		#print 'primes is: '+str(primes)
		csvfile.close()	
	return primes

def factorise(N,list):		
	#Create lists to hold prime factors of N, corresponding powers and any remainder
	s_before_lists = time.clock()	
	prime_factors = []
	powers = []
	remainder=()

	c_lists = time.clock() - s_before_lists

	#initialise N_remainder
	N_remainder = N
	i=2	

	#call calc_primes_powers_remainder
	#print('Calculating prime factors, powers and initial remainder...')
	s_before_factorisations = time.clock()	
	#N=5 - gets listed as remainder instead of factor!!!	
	result2=calc_primes_powers_remainder(list,N_remainder)

	c_factorisations = time.clock() - s_before_factorisations

	prime_factors=result2[0] 
	powers=result2[1]
	remainder=result2[2]
	c_pps=result2[3]
	c_nrem=result2[4]

	return prime_factors, powers, remainder, c_lists, c_factorisations, c_pps, c_nrem

def calc_primes_powers_remainder(isliced_primes, N_remainder):

	prime_factors=[]
	powers=[]
	remainder=()

	#Check if there are elements in prime list
	s_primefactors_powers = time.clock()
	if not isliced_primes:	
		#There are no elements in isliced_primes list		
		print("There are no elements in isliced_primes list??")		
		
		N_remainder=[]
		#remainder=[]
		
	else:
		#There are elements in primes list
		#Check if N_remainder is prime
		if N_remainder in isliced_primes:
			print(str(N_remainder)+' is in prime list..')
			prime_factors.append(N_remainder)
			powers.append(1)
		else:
			#N_remainder is not in prime list
			#print(str(N_remainder)+' is not in prime list..')
			for prime in isliced_primes:
				#print("prime is now: "+str(prime))			
				prime_int=int(prime)
				#for N_remainder not in one:
				while N_remainder <> 1:
					if N_remainder % prime_int == 0:		
						#prime is a factor		
						#prime^m divides N_remainder, m integer
						m = MaxPower(prime_int,N_remainder)		
						prime_factors.append(prime_int)
						powers.append(m)
						N_remainder = N_remainder/(prime_int**m)
						break
					else:
						break
	c_primefactors_powers = time.clock() - s_primefactors_powers
	
	#Check if there are elements in N_remainder list
	s_nremainder = time.clock()
	if not N_remainder:	
		#There are no elements in N_remainder list		
		N_remainder=()
	else:
		#raw_input("Waiting for user.. problem with "+str(N_remainder)+" being prime??")
		#There are elements in N_remainder list
		if N_remainder <> 1:
			print('There is a remainder of: '+str(N_remainder))
		
		#check if N_remainder is also a prime
		if N_remainder > long(isliced_primes[-1]) and math.sqrt(N_remainder) <= isliced_primes[-1]:
			#N_remainder is prime since its square root is less than largest prime in prime list file, and all those primes have been checked earlier.			
			#print('Appending last prime factor and power..')
			prime_factors.append(N_remainder)
			powers.append(1)
	
		elif N_remainder > long(isliced_primes[-1]) and math.sqrt(N_remainder) > isliced_primes[-1]:	
			#print('Appending remainder..')
			#remainder.append(N_remainder)
			#remainder.add(N_remainder)
			remainder=(N_remainder)
	c_nremainder = time.clock() - s_nremainder
	
	#Now set N_remainder to ''
	N_remainder=()
		
	#Return factors of N using factors() list
	#print("prime_factors: "+str(prime_factors)+", powers: "+str(powers)+", remainder: "+str(remainder))
	return prime_factors, powers, remainder, c_primefactors_powers, c_nremainder

def number_checks(number):

	#Simple Checks for N:
	#print('Running simple checks for number...')
	if number==0:
		print('Number entered is 0. Please choose another value for N')
		sys.exit()
	if number==1:
		print('1 doesn\'t have a prime power factorisation. Please choose another number.')
		sys.exit()
	if number<0:
		print('Number entered is negative. Please enter another number')
		sys.exit()

def size_input_check(input_number):

	#if size of number >= 2*10^8 then return message about memory & exit
	if input_number>2*(10**8):
		print('Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory errors..')
		sys.exit()


def MaxPower(i,N_remainder):
	m=0
	while N_remainder > 1 and not N_remainder % i:	
		m += 1		
		N_remainder //= i
	return m


def max_element_below_or_equal_target(List,target):
	#bool1=False

	#List = primes
	#target = 25

	#raw_input("Waiting for user.. problem in max_element_below_or_equal_target()")
	if target in List:
		#print 'target is: '+str(target)
		#print 'List.index(target) is: '+str(List.index(target))
		#return List.index(target)
		return List.index(target) + 1
	elif target > List[-1]:
		#Target value is not in list. Return index of last number in list.
		#bool1=True
		#return List.index(List[-1])
		return List.index(List[-1]) + 1
	#elif target < 2:
	#	return ""
	elif target < List[-1]:
		#Target value is less than largest prime in list
		# start from 2 and increase until last number is found that is less than target.
		i=0
		while List[i] < target:
			i = i + 1 
		#return i
		return i
	else:
		print 'List[-1] is: '+str(List[-1])
		print 'target is: '+str(target)	
		print "Other Error - Troubleshoot! list.index(target) is: "+str(list.index(target))+", target is: "+str(list.index(target))
		return "Other Error - Troubleshoot! list.index(target) is: "+str(list.index(target))+", target is: "+str(list.index(target))


if __name__=='__main__':
	main()

#def MaxPower(i,N_remainder):
#	m=1
#	MxP=1
#	for n in xrange_mod(2, N_remainder + 1,1):	
#		b = i**n		
#		a = N_remainder % b
#		if a==0: 	
#			m = m+1					
#		else: 
#			MxP = m
#			break
#	return MxP

#def xrange_mod(start=0,stop=None,step=1):
#	if stop is None: 	
#		stop=start
#		start=0
#	i=start
#	while i < stop:
#		#function returns a generator i
#		yield i
#		i += step
	

