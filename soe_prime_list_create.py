#Copyright Nick Prowse 2017. Code Licenced under Apache 2.
#Version 8. 13/10/2017.
#Programmed & tested in Python 2.76 only
#This program creates a prime list in CSV format with comma delimiter for all primes upto N inclusive using sieve of eratosthenes.
#It has been tested on Linux Mint v3.19 x64.

import sys
import math
import csv
import os.path

print("Copyright Nick Prowse 2017. Code Licenced under Apache 2.")
print("Version 8. 13/10/2017.")
print("Programmed & tested in Python 2.76 only.")
print("---------------------------------------------------------------------")
print("This program creates a prime list in CSV format with comma delimiter for all primes upto N inclusive.")
print("It has been tested on Linux Mint v3.19 x64.")
print("---------------------------------------------------------------------")

def main():
	print('What is the largest number you want primes to go upto in the prime list?')
	N_initial = raw_input()
	if N_initial.isdigit() is False:
		print('You have not entered a positive odd_integer. Please reenter.')
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

	primes=prime_list_create(N)
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
	
def prime_list_create(N):

	odd_integers=[]
	n=3
	#Step1 
	#create list of all positive odd_integers from 2 upto including N
	#eg N=1000
	print('creating odd_integers list for odd_integers upto '+str(N)+'...')
	#- This takes O(N) operations
	while n<=N:
		odd_integers.append(n)
		n+=2

	#Step 2
	#initialise p
	p=3

	#Step 3
	#enumerate multiples of p by counting to N from 2p in increments of p, and store them in marked_numbers list.
	marked_numbers=set()
	print('creating marked numbers list for odd_integers upto '+str(N)+'...')
	#======Total time complexity for step 3 is O(N^4) !!!======
	for odd_integer in odd_integers:  
	#--- This takes O(N) operations
		#print('odd_integer now is: '+str(odd_integer))		
		if odd_integer==3 and odd_integer not in marked_numbers: 
		#--- This takes O(N) operations due to "x not in s"
			#next marked number to be added
			p=odd_integer
			#print('next odd_integer to try is: '+str(p))
			#every time marked_numbers function is called it takes O(N^2) operations
			marked_numbers=marked_numbers_update(p, N, marked_numbers) 
			#print('multiples of '+str(p)+' added to marked_numbers')		
			#print('marked_numbers are now: '+str(marked_numbers))
			#increment p
			p=p+1
		elif odd_integer not in marked_numbers: 
		#--- This takes O(N) operations due to "x not in s"
			#next marked number to be added
			p=odd_integer**2
			#print('next odd_integer to try is: '+str(p))
			marked_numbers=marked_numbers_update(p, N, marked_numbers) #every time function is called it takes O(N^2) operations
			#print('multiples of '+str(p)+' added to marked_numbers')		
			#print('marked_numbers are now: '+str(marked_numbers))
			#increment p
			p=p+1	

	#print('marked_numbers for N='+str(N)+' are: '+str(marked_numbers))
	
	#Step 4
	#create list of primes
	primes=[]
	#Add first prime	
	primes.append(2)
	#Total time complexity for step 4 is O(N^2)
	print('creating primes list for primes upto '+str(N)+'...')
	for odd_integer in odd_integers: #--- This takes O(N) operations
		if odd_integer not in marked_numbers: 
		#--- This takes O(1) operations due to "x not in s" & marked_numbers is a set.
			primes.append(odd_integer)

	return primes

def marked_numbers_update(p, N, marked_numbers):  
#Whole function takes O(N^2) operations
	n=2	
	while n*p <= N:  #--- This takes O(N) operations
		#print('p is now: '+str(p))
		#append new marked numbers to marked_numbers_after
		#if str(n*p) not in marked_numbers:  #--- This takes O(N) operations		
		if n*p not in marked_numbers:  #--- This takes O(N) operations		#===========================
			#--- TO DO --- ADD CHUNKING! - ie split marked_numbers into chunks of 1000 so not all memoery is in use ----
			#===========================
			#marked_numbers.append(n*p) 
			marked_numbers.add(n*p) 
			#print('marked_numbers is now: '+str(marked_numbers))
		#increment n
		n=n+1			
	return marked_numbers

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
