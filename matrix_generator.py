#!/usr/bin/python

#Christopher Ray
#Professor Wang
#CSE 40437
#2 March 2016

#matrix_generator.py
#program for generating sensing matrix from twitter data set and clustering results file

import sys
import json
import re

def initialize(tweet_file, cluster_file):	#function to initialize user and cluster dicts
	users = {}
	for line in tweet_file:	#reading in user information from tweets file
		temp = json.loads(line)
		if(users.has_key(str(temp['from_user_id']))):
			users[str(temp['from_user_id'])]['tweets'].append(str(temp['id']))
		else:
			users[str(temp['from_user_id'])] = {'tweets':  [str(temp['id'])], 'clusters':  []}

	clusters = {}
	for line in cluster_file:	#reading in clusters
		line_array = re.split(':|,|\n', line)
		clusters[line_array[0]] = line_array[1:]

	return (users, clusters)	#returning user and cluster dicts
	

def main():
	if(len(sys.argv) < 3):	#checking for proper number of arguments
		sys.exit("Error:  Not enough arguments\n./matrix_generator.py [tweets] [cluster results] [optional output]")

	try:
		tweet_file = open(sys.argv[1], "r")
	except:
		sys.exit("Error:  could not open " + sys.argv[1])

	try:
		cluster_file = open(sys.argv[2], "r")
	except:
		sys.exit("Error:  could not open " + sys.argv[2])

	try:
		output_file = open(sys.argv[3], "w")
	except:
		output_file = open("sc_matrix.txt", "w")

	users = {}
	clusters = {}

	temp = initialize(tweet_file, cluster_file)	#initializing dictionary
	users = temp[0]
	clusters = temp[1]
	tweet_file.close()
	cluster_file.close()

	for cluster in clusters.keys():	#updating user information with whatever clusters the user's tweets belong to
		for tweet in clusters[cluster]:
			for user in users.keys():
				if((users[user]['clusters'].count(cluster) < 1) and (users[user]['tweets'].count(tweet) >= 1)):
					users[user]['clusters'].append(cluster)

	for key in users.keys():	#writing matrix to file
		for cluster in users[key]['clusters']:
			output_file.write(str(key) + "," + str(cluster) + "\n")

	output_file.close()

	
if __name__ == '__main__':
	main()
