
#Copyright Nick Prowse 2017. Code Licenced under Apache 2.
#Version 36. 16/10/2017.
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
#import islice
#from itertools import islice

print("Copyright Nick Prowse 2017. Code Licenced under Apache 2.")
print("Version 36. 16/10/2017.")
print("Programmed & tested in Python 2.76 only.")
print("---------------------------------------------------------------------")
print("This program attemps to import a prime list, and use the primes to factorise a number specified by user.")
print("Results printed are three arrays - first for prime factors, second for powers of those primes, third for any remainder (where a larger prime list is needed).")
print("Prime list file should be a .CSV file with each prime separated by commas.")
print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used.")
print("The larger the prime file is that is used, the longer the factorisation will take!")
print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to factorise most numbers under 2.5x10^9 in 1 second.")
print("---------------------------------------------------------------------")

prime_list_path="/home/mint/Desktop/"
prime_list_filename="primes_upto_10000000.csv"
primefile=prime_list_path + prime_list_filename
	
def main():
	#print(sys.version_info)

	#Check if primefile exists.
	if os.path.exists(primefile) is False:
		#File doesn't exist in location. Exit process.
		print('Prime file doesn\'t exist in location specified. Exiting.')
		sys.exit()

	print('Number to attempt to factorise?')
	N_initial = raw_input()
	if N_initial.isdigit() is False:
		print('You have not an integer. Please reenter.')
		sys.exit()

	#now convert type for N into a long:
	N = long(N_initial)

	result=factorise(N)
	prime_factors=result[0]
	powers=result[1]
	remainder=result[2]
	print prime_factors, powers, remainder

def factorise(N):
	#Simple Checks for N:
	#print('Running simple checks for number...')
	if N==0:
		print('Number entered is 0. Please choose another value for N')
		sys.exit()
	if N==1:
		print('1 doesn\'t have a prime power factorisation. Please choose another number.')
		sys.exit()
	if N<0:
		print('Number entered is negative. Please enter another number')
		sys.exit()

	#if size of N_initial >= 2*10^8 then return message about memory & exit
	#if N>2*(10**8):
	#	print('Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory errors..')
	#	sys.exit()
	
	
	# Largest number to consider primes upto is floor_sqrt_N
	floor_sqrt_N=int(math.floor(math.sqrt(N)))
	
	#print('floor_sqrt_N is: '+str(floor_sqrt_N))	
	#print('Largest number to consider primes upto is: '+str(floor_sqrt_N))

	primes=[]
	
	#Check if primefile exists.
	#print('Checking if Prime file exists in location specified..')
	if os.path.exists(primefile) is False:
		#File doesn't exist in location. Exit process.
		print('Prime file doesn\'t exist in location specified. Exiting.')
		sys.exit()

	with open(primefile,'r') as csvfile:
		# Want to limit highest prime imported from csv to be <= math.sqrt(N)
		# Need to get index of the highest prime <= math.sqrt(N)
		# Strip quotes, eol chars etc, and convert strings to integers	
		#print('Storing primes in Prime file into primes list...')

		#Use generator to get number of primes to use in prime file..
		#print 'Running generator..'
		z1=(int(x) for row in csv.reader(csvfile) for x in row)
		a1=list(z1)				
		b=max_element_below_or_equal_target(a1,floor_sqrt_N)
		#print 'Number of primes to extract from list is: '+str(b)

		#Run generator again to populate prime list
		#print 'Obtaining Primes from imported list..'		
		csvfile.seek(0)			
		if b>=1:	
			primes=list(itertools.islice(a1,b))		
		elif b==0:
			primes=list("")		
		
		csvfile.close()	

	#print 'primes list is: '+str(primes)

	#Create array / "list" to hold factors of N
	prime_factors = []
	powers = []
	remainder=[]

	#initialise N_remainder
	N_remainder = N
	i=2	

	#print('Calculating prime factors, powers and initial remainder...')
	#Check if there are elements in prime list
	if not primes:	
		#There are no elements in primes list		
		prime_factors=[]
		powers=[]
		N_remainder=[]
		
	else:
		#There are elements in primes list
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

	#Check if there are elements in N_remainder list
	if not N_remainder:	
		#There are no elements in N_remainder list		
		N_remainder=[]
	else:
		#There are elements in N_remainder list
		#check if N_remainder is also a prime
		if N_remainder > long(primes[-1]) and math.sqrt(N_remainder) <= primes[-1]:
			#N_remainder is prime since its square root is less than largest prime in prime list file, and all those primes have been checked earlier.			
			#print('Appending last prime factor and power..')
			prime_factors.append(N_remainder)
			powers.append(1)
	
		elif N_remainder > long(primes[-1]) and math.sqrt(N_remainder) > primes[-1]:	
			#print('Appending remainder..')
			remainder.append(N_remainder)

	#Now set N_remainder to ''
	N_remainder=''
		
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


def max_element_below_or_equal_target(List,target):
	#bool1=False
	if target in List:
		return List.index(target)#, bool1
	elif target > List[-1]:
		#Target value is not in list. Return index of last number in list.
		#bool1=True
		return List.index(List[-1])#, bool1
	elif target < List[-1]:
		#Target value is less than largest prime in list
		# start from 2 and increase until last number is found that is less than target.
		i=0
		while List[i] < target:
			i = i + 1 
		return i#, bool1
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


#def my_condition(y)
#	if y >= floor_sqrt_N:
#		return y
# 	if y < floor_sqrt_N:
#		n=2
#		count=0
#		while n < y:
#			count = count+1
#			n = n + 1 
#		return count

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

		#if N_remainder <= sys.maxint and N_remainder<>1:
			#N_remainder is an integer			
		#	remainder.append(int(N_remainder))	
		#elif N_remainder > sys.maxint and N_remainder<>1:
			#N_remainder is a long
		#	remainder.append(N_remainder)

		#print ('prime added: '+str(N_remainder))
		#now set N_remainder to 1		
		#N_remainder=1

#check size of N_remainder
		#min size of a long = sys.maxint
		#print('sys.maxint is: '+str(sys.maxint))

	#print ('N_remainder is: '+str(N_remainder))
	#print ('sqrt of N_remainder is: '+str(math.sqrt(N_remainder)))
	#print ('Largest prime in prime list is: '+primes[-1])

#primes_data=primes_data.rstrip('/')
			#print('Last character in primes_data is now: '+str(primes_data[-1]))

#print('Last character in primes_data is currently: '+str(primes_data[-1]))
			#raw_input('Waiting for user..')

		#Now use .split() to store primes in elements  
		#primes_data_final=primes_data.split(',')
		#primes=primes_data_final

		#check if last character in primes_data is a ','
		#if primes_data[-1]==',':
		#	primes_data=primes_data[:-1]
		
#primes_data=csvfile.read().replace('\n','').split(',')
		#primes_data=csvfile.read().replace('\n','')
		
		#primes_data=csvfile.read().replace('\n',''); print(primes[:160])
		#raw_input('waiting for user..')
	
		#while n < target:
		#	count = count+1
		#	n = n + 1 
		#return count

#primes=list(next(z1) for _ in xrange(floor_sqrt_N))
			#print 'Last prime in z1 list is: '+str(list(z)[-1])
			

#print 'target < List[-1]'
		#print 'target is: '+str(target)	
		#print 'List is'+str(List)
		#print 'List[-1] is: '+str(List[-1])

		#print '(target in List) or (target > List[-1])'
		#print 'target is: '+str(target)	
		#print 'List is'+str(List)
		#print 'List[-1] is: '+str(List[-1])

	#print 'target is: '+str(target)	
	#print 'List is'+str(List)
	#print 'List[-1] is: '+str(List[-1])
	#raw_input('waiting for user..')	
	#if target > List[-1]:
	#	print str(target)+" > "+str(List[-1])
	#	#raw_input('waiting for user..')	
	#	return target
	#else:
	#	print str(target)+" <= "+str(List[-1])
	#	#raw_input('waiting for user..')	
	#	return target 	

#a2=list(z2)
			#--------------------------------				
			#print 'type of b is:'+str(type(b))
			#print 'a2 list is:'+str(a2) #List is empty!!!!
			#--------------------------------
			#print 'Last prime in z2 list is: '+str(list(z2)[-1])
			#print 'Last prime in a2 list is: '+str(a2[-1])
			#primes=list(next(z2,0) for _ in xrange(b))
			#while z2 <= b:
			#	print int(x)				
			
			#print 'type of b is: '+str(type(b))
			#print 'primes list is: '+str(primes)
			#z2=''
			#a2=''

		#else:
		#	print 'python version is >= 3'			
		#	z3=(int(x) for row in csv.reader(csvfile) for x in row)
		#	a3=list(z)
		#	b=max_element_below_or_equal_target(a3,floor_sqrt_N)
		#	print 'max_element = '+str(b)
		#	primes=list(next(z) for _ in range(b))

#print 'prime list is: '+str(primes)
		#raw_input('Waiting for user..')
		#print('primes[0] is: '+str(primes[0])+', primes[1] is '+str(primes[1])+', primes[2] is: '+str(primes[2]))
				
		#except:
		#except StopIteration:
		#	print('floor_sqrt_N is: '+str(floor_sqrt_N))	
		#	#print('a[-1] is: '+str(a[-1]))
		#	print('primes[0] is: '+str(primes[0]))
		#	print('primes[-1] is: '+str(primes[-1]))

		#list_index=b[0]
		#bool_check=b[1]

		# Check if target greater than last number in prime list 
		#if bool_check is True:
			#target is not in prime list


# when N=6930693693486986863. N_remainder is not displayed!!!
	#print 'N_remainder is '+str(N_remainder)
	#print 'Last prime in prime file is: '+str(primes[-1])
	#print 'math.sqrt(N_remainder) is '+str(math.sqrt(N_remainder))	
	



