#Copyright Nick Prowse 2017. Code Licenced under Apache 2.
#Version 15. 25/10/2017.
#Programmed & tested in Python 2.76 only
#This program creates a prime list in CSV format with comma delimiter for all primes upto N inclusive using sieve of eratosthenes.
#It has been tested on Linux Mint v3.19 x64.
#Using Lists instead of sets for storage to minimise memory usage

import sys
import math
import csv
import os.path
import time
import itertools

print("Copyright Nick Prowse 2017. Code Licenced under Apache 2.")
print("Version 15. 25/10/2017.")
print("Programmed & tested in Python 2.76 only.")
print("---------------------------------------------------------------------")
print("This program creates a prime list in CSV format with comma delimiter for all primes upto number inclusive specified by user.")
print("It has been tested on Linux Mint v3.19 x64.")
print("---------------------------------------------------------------------")

def main():
	print('What is the largest number you want primes to go upto in the prime list?')
	# Problem with generated primes when N = 10000
	# Examples: after 61 (prime), next is 8731
	# Examples: after 73 (prime), next is 8893
	# Examples: after 97 (prime), next is 8293
	#N = 10000	
	N_initial = raw_input()
	if N_initial.isdigit() is False:
		print('You have not entered an integer. Please reenter.')
		sys.exit()

	#now convert type for N into a long:
	N = long(N_initial)
	
	#Simple Checks for N:
	if N==0:
		print('Number entered is 0. Please choose another number.')
		sys.exit()
	if N==1:
		print('1 is not a prime. Please choose another number.')
		sys.exit()
	if N<0:
		print('Number entered is negative. Please enter another number')
		sys.exit()

	primes_and_times=prime_list_create(N)
	
	primes=primes_and_times[0]	
	c_oddintegers=primes_and_times[1]
	c_markednumbers=primes_and_times[2]
	c_primes=primes_and_times[3]

	prime_list_path="/home/mint/Desktop/"
	prime_list_filename='primes_upto_'+str(N)+'.csv'
	primefile=prime_list_path + prime_list_filename
	
	#Check if primefile already exists.
	if os.path.exists(primefile) is False: 
		print('Now creating file for primes in prime list upto '+str(N))
		csvfile_create(primes,primefile)
	else:
		print('Prime file already exists in that location. Existing prime file will be deleted before new one is created.')
		os.remove(primefile)
		csvfile_create(primes,primefile)
		print('Prime list for primes upto '+str(N)+' created.')
	
	print 'Time to create odd integers list: '+str(c_oddintegers) 
	print 'Time to create marked numbers list: '+str(c_markednumbers)
	print 'Time to create prime list: '+str(c_primes)

def prime_list_create(N):

	#Initialise marked_numbers
	marked_numbers=[]

	#Step 1
	#Populate marked_numbers with even numbers >= 4 upto including N
	j=4	
	print('Populating marked_numbers tuple with 4 <= even numbers <= '+str(N)+'...')
	s_evenintegers=time.clock()
	while j<=N:
		#a = marked_numbers + (j,)
		#marked_numbers = a[1:]
		#marked_numbers=marked_numbers+(j,)
		#marked_numbers.add(j)
		marked_numbers.append(j)
		j+=2
	c_evenintegers=time.clock()-s_evenintegers
	print'Memory used by even integers: '+str(sys.getsizeof(marked_numbers))

	odd_integers=[]
	n=3
	#Step 2 
	#create list of all positive odd_integers from 2 upto including N
	#eg N=10000
	print('creating odd_integers tuple for odd_integers upto '+str(N)+'...')
	#- This takes O(N) operations
	s_oddintegers=time.clock()	
	while n<=N:
		#b = odd_integers + (n,)
		#odd_integers = b[1:]
		#odd_integers=odd_integers+(n,)
		#odd_integers.add(n)
		odd_integers.append(n)
		n+=2
	c_oddintegers=time.clock()-s_oddintegers
	#small_set=set(itertools.islice(odd_integers, 10))
	#print('small_set is: '+str(small_set))
	#small_list=list(itertools.islice(odd_integers, 10))	
	#print('small_list is: '+str(small_list))
	print('slice of odd_integers[0:10]: '+str(odd_integers[0:10])+' ...')
	print'Memory used by odd integers: '+str(sys.getsizeof(odd_integers))

	#Step 3
	#initialise p
	p=3

	#Step 4
	#enumerate multiples of p by counting to N from 2p in increments of p, and store them in marked_numbers list.
	print('creating marked numbers list for odd_integers upto '+str(N)+'...')
	#======Total time complexity for step 3 is O(N^4) !!!======
	s_markednumbers=time.clock()
	for odd_integer in odd_integers:  
	#--- This takes upto O(N) operations, average O(1) operations due to "x in s" and is a set.
		floor_sqrt_oddint = math.sqrt(odd_integer)	
		#print('odd_integer now is: '+str(odd_integer))		
		#if floor_sqrt_oddint in marked_numbers:
			#no need to add since it & its multiples would be already in marked_numbers			
			#print('no need to add '+str(odd_integer)+' since it & its multiples are already in marked_numbers')	
			#break
		#else:
		if floor_sqrt_oddint not in marked_numbers:
			if odd_integer not in marked_numbers:
			#--- This takes upto O(N) operations, average O(1) operations due to "x not in s" and is a set.
				#next marked number to be added
				p=odd_integer
				#print('next odd_integer to try is: '+str(p))
				#every time marked_numbers function is called it takes O(N^2) operations
				marked_numbers=marked_numbers_update(p, N, marked_numbers) 
				#print('multiples of '+str(p)+' added to marked_numbers')		
				#print('marked_numbers are now: '+str(marked_numbers))
				#increment p
				p=p+1
	
			#elif odd_integer not in marked_numbers: 
			#--- This takes upto O(N) operations, average O(1) operations due to "x not in s" and is a set.
				#next marked number to be added
			#	p=odd_integer
				#p=odd_integer**2
				#print('next odd_integer to try is: '+str(p))
			#	marked_numbers=marked_numbers_update(p, N, marked_numbers) #every time function is called it takes O(N^2) operations
			#	print('multiples of '+str(p)+' added to marked_numbers')		
				#print('marked_numbers are now: '+str(marked_numbers))
				#increment p
			#	p=p+1	

			#print('marked_numbers for N='+str(N)+' are now: '+str(marked_numbers))
	c_markednumbers=time.clock() - s_markednumbers	
	print'Memory used by marked numbers: '+str(sys.getsizeof(marked_numbers))

	#Step 4
	#Total time complexity for step 4 is between O(N) and O(N^2)
	
	#create list of primes
	primes=[]
	s_primes=time.clock()
	#Add first prime
	primes.append(2)
	
	print('creating primes list for primes upto '+str(N)+'...')
	for odd_integer in odd_integers: 			#This takes O(N) operations
		if odd_integer not in marked_numbers: 		#This takes average of O(1) operations (worst case O(N)) due to "x not in s" & marked_numbers is a set.
			#print('Appending '+str(odd_integer)+' to primes list..')
			primes.append(odd_integer)
	c_primes=time.clock() - s_primes
	print'Memory used by primes: '+str(sys.getsizeof(primes))

	return primes, c_oddintegers, c_markednumbers, c_primes

def marked_numbers_update(p, N, marked_numbers):  
#Whole function takes O(N^2) operations
	n=2	
	#chunk=[]
	while n*p <= N:  					#This takes O(N) operations
		#print('n is now: '+str(n))
		#append new marked numbers to marked_numbers	
		if n*p not in marked_numbers:  			#This takes O(N) operations
			marked_numbers.append(n*p)
			#marked_numbers.add(n*p) 
			#print('marked_numbers is now: '+str(marked_numbers))
		#increment n
		n=n+1			
	return marked_numbers

	#===========================
	#--- TO DO --- ADD CHUNKING! - ie split marked_numbers into chunks of 1000 so not all memory is in use ----

	#number_chunks = int(math.ceil(N / 1000))
	#i=0			
	#for i in xrange(0,number_chunks)  
	#	chunk[i].append(marked_numbers(1:(1000-1)))
	#	i = i+1
			
	#=========================== 


def csvfile_create(data,filepath):
	#create csv file using data
	with open(filepath,'wb') as csvfile:
		wr = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_ALL)
		wr.writerow(data)		
		csvfile.close()	

if __name__=='__main__':
	main()

	#with open(primefile,'r') as csvfile:
			#primes_data=csvfile.read().replace('\n','').split(',')
			#primes_data=csvfile.read().replace('\n','')
		
			#check if last character in primes_data is a ','
			#print('Last character in primes_data is currently: '+str(primes_data[-1]))
		
			#if primes_data[-1]==',':
				#print('Last character in primes_data is currently: '+str(primes_data[-1]))
				#raw_input('Waiting for user..')
				#primes_data=primes_data[:-1]
				#primes_data=primes_data.rstrip('/')
				#print('Last character in primes_data is now: '+str(primes_data[-1]))
			#Now use .split() to store primes in elements  
			#primes_data_final=primes_data.split(',')
			#primes=primes_data_final
			#csvfile.close()

	#result=marked_numbers_update(p, N, marked_numbers)
	#print('marked_numbers is now: '+str(result[0]))
