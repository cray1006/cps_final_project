#!/usr/bin/python

#Christopher Ray
#Professor Wang
#CSE 40437
#2 March 2016

#A3.py
#Program to perform EM algorithm on Twitter data sets

import sys
from random import randint
from math import pow
import operator

def init_theta(input_file):	#function for initializing source database and claims dict
	database = {}
	claims = {}

	for line in input_file:	#iterate through sensing matrix file
		line_array = line.split(',')	
		claim = line_array[1][:len(line_array[1]) - 1]	#getting claim ID
		if (not claims.has_key(claim)):	#adding claim to claims dict
			claims[claim] = None

		if database.has_key(line_array[0]):	
			database[line_array[0]]['claims'].append(claim)	#adding claim to source database
		else:
			database[line_array[0]] = {'claims': [claim], 's':  0, 'a':  0, 'b':  0}	#adding source to database

	num_claims = float(len(claims.keys()))
	for key in database.keys():	#initializing s, a, and b for each source
		si = float(len(database[key]['claims'])) / num_claims
		database[key]['s'] = si
		database[key]['a'] = si
		database[key]['b'] = 0.5 * si

	return (database, claims, num_claims)	#returning source databse, claims, and the number of claims

def em(database, claims, num_claims, d):	#function that performs EM algorithm
	for i in range(0, 20):	#running algorithm 20 times
		sum_Z = 0
		for claim in claims.keys():	#iterate through all claims
			A = 1
			B = 1
			for key in database.keys():
				if(database[key]['claims'].count(claim) >= 1):
					temp = 1.0	#user has made the claim
				else:	
					temp = 0.0	#user has not made the claim
				a = database[key]['a']	
				b = database[key]['b']
				A *= pow(a, temp) * pow((1 - a), (1 - temp))	#calculating A
				B *= pow(b, temp) * pow((1 - b), (1 - temp))	#calculating B

			temp_Z = (A * d) / ((A * d) + (B * (1 - d)))	#calculating Z for each claim
			claims[claim] = temp_Z	
			sum_Z += temp_Z

		for key in database.keys():	#updating a and b for each source
			temp_Z = 0
			for c in database[key]['claims']:
				temp_Z += claims[c]
			database[key]['a'] = temp_Z / sum_Z
			database[key]['b'] = (len(database[key]['claims']) - temp_Z) / (num_claims - sum_Z)

		d = sum_Z / num_claims	#update d

	return claims	#return claims database
	

def main():
	if(len(sys.argv) < 2):	#checking for proper number of arguments
		sys.exit("Error:  Not enough input\n./A3.py [input sensing matrix] [flags] [optional output file]")

	try:	#attempting to open input file
		input_file = open(sys.argv[1], "r")
	except:
		sys.exit("Error:  Could not open " + sys.argv[1])

	
	try:
		output_file = open(sys.argv[3], "w")
	except:	
		output_file = open("A3_results.txt", "w")	#output file

	d = 0	#initializing d and cred based on user flags
	cred = 0
	try:
		if(sys.argv[2] == "-YY"):
			d = 0.5
			cred = 1
		elif(sys.argv[2] == "-NY"):
			d = .10 * randint(1,9)
			cred = 1
		elif(sys.argv[2] == "-YN"):
			d = 0.5
			cred = 0
		else:
			d = .10 * randint(1,9)
			cred = 0
	except:
		d = .10 * randint(1,9)
		cred = 0


	theta = init_theta(input_file)	#initializing database, claims, and num_claims
	input_file.close()
	
	database = theta[0]
	claims = theta[1]
	num_claims = theta[2]

	claims = em(database, claims, num_claims, d)	#running em algorithm
			
	if(cred == 1):	#writing results to outputfile in sorted order (based on Z)
		sorted_claims = sorted(claims.items(), key=operator.itemgetter(1))
		for item in sorted_claims[::-1]:
			if(item[1] >= 0.5):
				output_file.write(str(item[0]) + ",1\t" + str(item[1]) + "\n")
			else:
				output_file.write(str(item[0]) + ",0\t" + str(item[1]) + "\n")
	else:	#writing results to outputfile (ordered by claim id)
		for i in range(1, len(claims.keys()) + 1):
			if(claims[str(i)] >= 0.5):
				output_file.write(str(i) + ",1\n")
			else:
				output_file.write(str(i) + ",0\n")
		
	output_file.close()
	

if __name__ == '__main__':
	main()
