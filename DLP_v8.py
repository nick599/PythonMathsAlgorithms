#Copyright Nick Prowse 2017. Code Licenced under Apache 2.
#Version 8. 29/10/2017.
#Programmed & tested in Python 2.76 only
#This program attemps to solve a Discrete Log Problem (DLP) specified by user, via factorisation of (p-1) where p is a prime number. 
#Results printed are three arrays ...
#Prime list file should be a .CSV file with each prime separated by commas.
#Ensure that "prime_list_path" and "prime_list_filename" are edited for the location of prime list file used.
#The larger the prime file is that is used, the longer the factorisations will take!
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to solve a DLP with a prime of xxx in xxx seconds.

import sys
import math
import os
import itertools
import factorise

print("Copyright Nick Prowse 2017. Code Licenced under Apache 2.")
print("Version 8. 29/10/2017.")
print("Programmed & tested in Python 2.76 only.")
print("---------------------------------------------------------------------")
print("This program attemps to solve a Discrete Log Problem (DLP) specified by user, via factorisation of (p-1) where p is a prime number.")
print("Results printed are three arrays ...")
print("Prime list file should be a .CSV file with each prime separated by commas.")
print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used.")
print("The larger the prime file is that is used, the longer the factorisation will take!")
print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to solve a DLP with a prime of xxx in xxx seconds")
print("---------------------------------------------------------------------")
	
def main():
	prime_list_path="/home/mint/Desktop/"
	prime_list_filename="primes_upto_10000.csv"
	primefile=prime_list_path + prime_list_filename
	print('primefile currently is: '+str(primefile))

	#print(sys.version_info)

	print('What is g?')
	g_initial = raw_input()
	if g_initial.isdigit() is False:
		print('You have not entered an integer for g. g is: '+str(g)+'. Please reenter.')
		sys.exit()

	#now convert g into a long:
	g = long(g_initial)

	print('What is h?')
	h_initial = raw_input()
	if h_initial.isdigit() is False:
		print('You have not entered an integer for h. h is: '+str(h)+'. Please reenter.')
		sys.exit()

	#now convert h into a long:
	h = long(h_initial)

	print('What is p?')
	p_initial = raw_input()
	if p_initial.isdigit() is False:
		print('You have not entered an integer for p. p is: '+str(p)+'. Please reenter.')
		sys.exit()

	#now convert p into a long:
	p = long(p_initial)

	print("---------------------")
	print("g: "+str(g)+", h: "+str(h)+", p: "+str(p))

	floor_sqrt_p = int(math.floor(math.sqrt(p)))
	print('floor_sqrt_p is: '+str(floor_sqrt_p))

	#Run checks on g, h & p	
	result=ghp_checks(g,h,p,floor_sqrt_p)
	if result == 0:
		sys.exit

	#problem here currently floor_sqrt_p doesn't bring back primes being (2) !!!
	#define prime list
	print('Importing primes from csv file')
	primes=factorise.csvfile_store_primes(primefile)
	#primes=factorise.csvfile_store_primes(primefile,floor_sqrt_p, p)
	#b=max_element_below_or_equal_target(('2', '3', '5', '7', ...),1)
	#print('primes currently are:'+str(primes))
	#raw_input('Waiting for user..')

	#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.

	print('Running dlp()..')
	result = dlp(g,h,p, primes)
	x=result[0]
	y=result[1]
	print x, y

def ghp_checks(g,h,p,floor_sqrt_p):

	status=1
	
	#Need to check if p is prime
	a = isprime(p,floor_sqrt_p)
	#print("isprime(p) is: "+str(a))	
	if a==0:
		print('The number entered for p:'+str(p)+' is not prime. Please choose a number that is prime for p.')
		status=0
		sys.exit()

	#Simple Checks for g, h & p:
	print('Running simple checks on g..')
	if (g==0 or h==0 or p==0):
		print('One or more numbers entered for g, h and p are 0. Please choose numbers that are not 0.')
		status=0
		sys.exit()
	elif g==1:
		print('g = 1 has trivial solutions for the dlp. Please choose another number.')
	#elif h==1:
	#	print('g = 1 has trivial solutions for the dlp. Please choose another number.')
	#	status=0
	#	sys.exit()
	elif g<0:
		print('Number for g is negative. Please enter another number')
		status=0
		sys.exit()
	return status

def isprime(p,floor_sqrt_p):
	#print('p is: '+str(p))	
	status=0
	if p % 2 == 0:
		status=1
	
	#floor_sqrt_p = int(math.floor(math.sqrt(p)))	
	
	n=1
	while n <= floor_sqrt_p:
		if p % n == 0:
			status=1
			break 
		else:
			status=0
			n = n+2
	#print('status is: '+str(status))	
	return status		

#def modulo(x,p):
#	r = x % p
#	return r

def dlp(g, h, p, primes):
	
	print('--------------------')

	#1st step: calculate p-1 from p
	p_minus_1 = p-1
	print('p-1 is: '+str(p-1))	

	#2nd step: factorise p_minus_1 into product of prime powers
	result=factorise.factorise(p_minus_1, primes)
	#primes_tuple=tuple(result[0])
	primes_list=list(result[0])
	#powers=tuple(result[1])
	powers=list(result[1])
	print('primes for factorisation of p-1 are:'+str(primes_list))
	print('powers for factorisation of p-1 are:'+str(powers))

	#3: Calculate C - number of unique primes in factorisation (also is number of congruences to solve)
	C=0
	for prime in primes_list:
		C = C + 1		
	print('Number of primes in primes_list = C = '+str(C))

	#4: Need to create a list (with C elements) for each of: q_i, e_i, W, g_i, h_i, z_i, & V_i 
	#C_tuples=tuple(xrange(1,C))
	C_list=list(xrange(1,C+1))
	print('C_list is: '+str(C_list))
	print('--------------------')

	#5: initialise lists
	qi=[]
	ei=[]
	Wi=[]
	gi=[]
	hi=[]
	zi=[]
	Bi=[]
	Vi=[]
	#Ui=[]

	#6: loop through each C calculating values & storing them
	i = 0
	for C in C_list:
		print('current C is:'+str(C))
		#modulo(x,p)
		print('i is: '+str(i))
		qi.append(primes_list[i])
		print('qi['+str(i)+'] is: '+str(qi[i]))
		ei.append(powers[i])
		print('ei['+str(i)+'] is: '+str(ei[i]))
		Wi.append(p_minus_1 / (qi[i]**ei[i]))
		print('Wi['+str(i)+'] = p_minus_1 / (qi['+str(i)+']**ei['+str(i)+'])  is: '+str(Wi[i]))
		
		gi.append(g**Wi[i])
		print('gi['+str(i)+'] = g**Wi['+str(i)+'] is: '+str(gi[i]))
		Bi.append(gi[i] % p)
		print('Bi['+str(i)+'] = gi['+str(i)+'] % p is: '+str(Bi[i]))
		
		hi.append(h**Wi[i])
		print('hi['+str(i)+'] = h**Wi['+str(i)+'] is: '+str(hi[i]))
		zi.append(hi[i] % p)
		print('zi['+str(i)+'] = hi['+str(i)+'] % p is: '+str(zi[i]))
		
		raw_input('Waiting for user..')

		#Ui.append(math.log(Bi[i])) #this needs to be log base g - is calc for Ui correct??
		#print('Ui['+str(i)+'] = math.log(Bi['+str(i)+']) is: '+str(Ui[i]))

		#What is python for log of base g ???

		Vi.append(math.log(zi[i])) #this needs to be log base g - is calc for Vi correct??
		print('Vi['+str(i)+'] = math.log(zi['+str(i)+']) is: '+str(Vi[i]))
		
		print('----------------------')
		i = i + 1

	raw_input('Waiting for user..')

	#Now zi_list[i] * yi_list[i] congruent to Vi mod p, where zi, Vi, p are known and yi are unknown
	
	#7:Use Euclids algorithm forward & reverse to find yi's
	
	euclid_f=[]
	euclid_r=[]
	yi=[]
	j = 0
	for C in C_tuples:	
		euclid_f=euclid_forward(zi_list[j],Vi_list[j],p)
		euclid_r=euclid_reverse(euclid_f[0],euclid_f[1],p)
		yi[j]=euclid_r[0]	
		j = j + 1

	#Now x = yi mod qi for each record
	
	#8: Take first congruence; x = qi * t + yi for some t unknown.
	k = 0
	for C in C_tuples:
		print('congruence '+str(k)+' is: x = '+str(qi_list[k])+'* t + '+str(yi_list[k]))
		
	#9: Substitute first congruence in all other congruences.
	#Now 	q1 * t + y1 = y2 mod q2
	#...................................
	#	q1 * t + y1 = yC mod qC
	# where t are unknown.


def euclid_forward(a,b,p):
	


	return k1,k2

def euclid_reverse(c,d,p):
	


	return y



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


		#qi_list[i] = primes_list[i]
		#qi_list[i] = primes_list(i)
		#Wi_list.append(p_minus_1 % (qi_list[i]**ei_list[i]))
		#Wi_list[i] = p_minus_1 % (qi_list[i]**ei_list[i]) 	
		#gi_list[i] = g**Wi_list[i]
		#hi_list[i] = h**Wi_list[i]
		#zi_list[i] = hi_list[i] % p
		
		#print('qi is:'+str(qi_list[i]))
		#print('ei is:'+str(ei_list[i]))
		#print('Wi is:'+str(Wi_list[i]))
		#print('gi is:'+str(gi_list[i]))
		#print('hi is:'+str(hi_list[i]))
		#print('zi is:'+str(zi_list[i]))
		#print('Vi is:'+str(Vi_list[i]))
