#Copyright Nick Prowse 2017. Code Licenced under Apache 2.
#Version 19. 07/10/2017.
#Programmed & tested in Python 2.76 only
#This program attemps to import a prime list, and use the primes to factorise a number N. 
#Results printed are three arrays - first for prime factors, second for powers of those primes, third for any remainder (where a larger prime list is needed).
#Prime list file should be a .CSV file with each prime separated by commas.
#Ensure that "prime_list_path" and "prime_list_filename" are edited for the location of prime list file used.
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 50,000 and was able to factorise most numbers under 2.5x10^9 in 1 second.

import sys
print(sys.version_info)
import math
import csv

print("Copyright Nick Prowse 2017. Code Licenced under Apache 2.")
print("Version 19. 07/10/2017.")
print("Programmed & tested in Python 2.76 only.")
print("This program attemps to import a prime list, and use the primes to factorise a number N.")
print("Results printed are three arrays - first for prime factors, second for powers of those primes, third for any remainder (where a larger prime list is needed).")
print("Prime list file should be a .CSV file with each prime separated by commas.")
print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used.")
print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 50,000 and was able to factorise most numbers under 2.5x10^9 in 1 second.")

prime_list_path="/home/mint/Desktop/"
prime_list_filename="primes_upto50k_edited_v2.csv"
primefile=prime_list_path + prime_list_filename

def main():
	print('Number to attempt to factorise?')
	N_initial = raw_input()
	if N_initial.isdigit() is False:
		print('You have not entered a positive integer. Please reenter.')
		sys.exit()

	#now convert type for N into a long:
	N = long(N_initial)
	
	#Simple Checks for N:
	if N==0:
		print('Number entered is 0. Please choose another value for N')
		sys.exit()
	if N==1:
		print('1 doesn\'t have a prime power factorisation. Please choose another number.')
		sys.exit()
	if N<0:
		print('Number entered is negative. Please enter another number')
		sys.exit()

	#---- TO DO ----
	#check size of N_initial
	#
	#
	#
	#

	result=factorise(N)
	prime_factors=result[0]
	powers=result[1]
	remainder=result[2]
	print prime_factors, powers, remainder

def factorise(N):
	primes=[]
	with open(primefile,'r') as csvfile:
		primes_data=csvfile.read().replace('\n','').split(',')
		primes=primes_data
		csvfile.close()
	
	#bool=true

	#while bool=true:

	#Create array / "list" to hold factors of N
	prime_factors = []
	powers = []
	remainder=[]

	#initialise N_remainder
	N_remainder = N
	i=2	

	for prime in primes:
		prime_int=int(prime)
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
	
	#check if N_remainder is also a prime
	#print ('N_remainder is: '+str(N_remainder))
	#print ('sqrt of N_remainder is: '+str(math.sqrt(N_remainder)))
	#print ('Largest prime in prime list is: '+primes[-1])

	if N_remainder > long(primes[-1]) and math.sqrt(N_remainder) < primes[-1]:
		#N-remainder is prime since its square root is less than largest prime in prime list file, and all those primes have been checked earlier.
		#print ('N_remainder > largest prime in prime list, and sqrt of N_remainder < largest prime in prime list')	
		prime_factors.append(int(N_remainder))
		
		#print ('prime added: '+str(N_remainder))
		#now set N_remainder to 0		
		N_remainder=1
	
	if N_remainder<>1:
		remainder.append(N_remainder)	

	#Return factors of N using factors() list
	return prime_factors, powers, remainder
	
	#print('Number to attempt to factorise?')
	#N = input()
	
	#bool=false

def MaxPower(i,N_remainder):
	m=0
	while N_remainder > 1 and not N_remainder % i:	
		m += 1		
		N_remainder //= i
	return m

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

if __name__=='__main__':
	main()

#Return N_remainder if N_remainder > largest prime in list
	#print('N_remainder is now: '+str(N_remainder))
	#print('Last prime in prime list is: '+str(primes[-1]))
	#if long(N_remainder) > long(primes[-1]):
		#remainder.append(N_remainder)		
		#print('abc')
		#print('Remainder is: '+str(remainder[0]))		
		#return remainder[0]
	#elif N_remainder <= primes[-1]:
		#remainder.append(0)
		#print('def')
	#	return prime_factors, powers, N_remainder

	#return prime_factors, powers, Remainder

	#if N_remainder > long(primes[-1]):
	#	print ('N_remainder > largest prime in prime list')

	#if math.sqrt(N_remainder) < primes[-1]:
	#	print ('sqrt of N-remainder < largest prime in prime list')

