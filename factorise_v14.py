#Copyright Nick Prowse 2017. Code Licenced under Apache 2.

#Version 14. 05/10/2017.
#Programmed & tested in Python 2.76 only
#This program attemps to import a prime list, and use the primes to factorise a number N. 
#Results printed are two arrays - first for prime factors, second for powers of those primes.
#prime list file should be a .CSV file with each prime separated by commas.
#Ensure that "prime_list_path" and "prime_list_filename" are edited for the location of prime list file used.
#It has been tested on Linux Mint v3.19 x64 and was able to factorise 10^8 in a few seconds.Trying to factorise 10^9 gave a memory error, and 5x10^8 hung the OS.
#Hence I suggest only trying to factorise numbers upto 10^8 with this version currently.

import sys
print(sys.version_info)
import math
import csv

print("Copyright Nick Prowse 2017. Code Licenced under Apache 2")
print("Version 10. 31/07/2017.")
print("This program attemps to import a prime list, and use the primes to factorise a number N.")
print("Results printed are two arrays - first for prime factors, second for powers of those primes.")
print("prime list file should be a .CSV file with each prime separated by commas.")
print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used.")
print("It has been tested on Linux Mint v3.19 x64 and was able to factorise 10^8 in a few seconds.Trying to factorise 10^9 gave a memory error, and 5x10^8 hung the OS.")
print("Hence I suggest only trying to factorise numbers upto 10^8 with this version currently.")

prime_list_path="/home/mint/Desktop/"
prime_list_filename="primes_upto50k_edited_v2.csv"
primefile=prime_list_path + prime_list_filename
#print(primeFile)

def main():
	print('Number to attempt to factorise?')
	N_initial = raw_input()
	#print('N is now: ' + str(N))

	#check type of N
	#print type(N)	
	#type_N=type(N)
	if N_initial.isdigit() is False:
		print('You have not entered a positive integer. Please reenter.')
		sys.exit()

	#now convert type for N into a long:
	N = long(N_initial)
	print ('N is of type: ' + str(type(N)))

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
	#check size of N
	#
	#
	#
	#

	result=factorise(N)
	#prime_factors=factorise(N)[0]
	#powers=factorise(N)[1]
	
	prime_factors=result[0]
	powers=result[1]
	print prime_factors, powers

def factorise(N):
	primes=[]
	with open(primefile,'r') as csvfile:
		primes_data=csvfile.read().replace('\n','').split(',')
		primes=primes_data
		#print ('Number of elements is: '+str(len(primes)))
		#print ('First element is: '+primes[0])
		#print ('last element is: '+primes[-1])
		#max element in primes[]?
		#print ('Largest element is: '+max(primes)) 
		# This is 9973 ????
		csvfile.close()
	
	#bool=true

	#while bool=true:

	#Create array / "list" to hold factors of N
	prime_factors = []
	powers = []

	#initialise N_remainder
	N_remainder = N
	#print ('N_remainder is now: '+ str(N_remainder))
	i=2	

#--------------------------------------


	#result2=raw_input("Press enter to continue")	
#--------------------------------------

	for prime in primes:
		#raw_input("Press enter to continue")
		#print prime		
		#print ('N_remainder % i is:' + str(N_remainder % i))
		#print ('i is now: '+ str(i))
		#print ('prime is: '+ str(prime))
		prime_int=int(prime)
		#print ('prime_int is: '+ str(prime_int))
		while N_remainder <> 1:
			
			#print ('N_remainder is: '+ str(N_remainder))
			#print ('prime_int is of type: ' + str(type(prime_int)))
			#print ('N_remainder is of type: ' + str(type(N_remainder)))
			#raw_input("Press enter to continue")		
			#if N_remainder == 1:
				#break
			#print prime_int
			if N_remainder % prime_int == 0:		
				#prime is a factor
				#print ('prime factor is: '+ str(prime))
				#How many times does i go into N_remainder? exactly?		
				# prime^m divides N_remainder, m integer
				m = MaxPower(prime_int,N_remainder)		
				#print ('Maximum power is: '+ str(m))
				
				prime_factors.append(prime_int)
				powers.append(m)
				#print ('prime factor added: ' + str(prime))
				#print ('power added: ' + str(m))
				N_remainder = N_remainder/long(prime_int**m)
				#print ('N_remainder is now: '+ str(N_remainder))
				#print ('----------')
				#count+=1		
				#i+=1
				#print ('before 1st break')			
				break
			else:
				#i+=1
				#print ('before 2nd break')
				break
			#print ('before 3rd break')			
			#break

	#Return factors of N using factors() list
	return prime_factors, powers

	#print('Number to attempt to factorise?')
	#N = input()
	
	#bool=false

def MaxPower(i,N_remainder):
	m=1
	MxP=1
	for n in range (2, N_remainder + 1):	
		#N_remainder=25, n=1, i=5, MxP=1		
		b = long(i**n)		
		a = long(N_remainder % b)
		#print("a is: " + str(a))
		if a==0: 	
			#print("n is: " + str(n))
			m = m+1					
			#break
		else: #first run: n=2, i=5, a=5, n*i=10
			#print("n is: " + str(n))
			#print('jgkdfjgdf')
			MxP = m
			#print("MxP is: " + str(MxP))			
			break
	return MxP

if __name__=='__main__':
	main()

#prime_list_with_line_returns=csv.reader(csvfile, delimiter=',')	
	#for row in prime_list_with_line_returns:
	#	#primes=''.join(row)
	#	primes=(line.replace('\n', "") for line in prime_list_with_line_returns)
	#	#primes=(line.replace('\n', "") for line in csvfile)
		#print row
		#print "-------------"
		#print ", ".join(row)
	#print(prime_list_with_line_returns)
	#primes=Print_list_with_line_returns.", ".join(row)
	#print(primes)

#open('workfile','r') 
#first arg is a string containing the filename
#second arg is another string containing a few charactersdescribing the way a file will be used.
#r - file will only be read
#w - for only writing - existing file with same name will be erased
#a - opens the file for appending
#r+ - opens the file for both reading and appending
#b - opens the file in binary mode
