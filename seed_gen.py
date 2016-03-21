#!/usr/bin/python

#Christopher Ray
#Professor Wang
#CSE 40437
#16 March 2016

#seed_gen.py
#Program for generating initial seeds for k-means algorithm

import sys
import json

def main():
	try:
		input_file = open(sys.argv[1], "r")
	except:
		sys.exit("Error:  Could not open " + sys.argv[1])

	try:
		num_clusters = int(sys.argv[2])
	except:
		num_clusters = 10

	try:
		num_tweets = int(sys.argv[3])
	except:
		sys.exit("Error:  Input number of tweets")

	gap = num_tweets / num_clusters
	#print gap

	i = 0
	c_count = 0
	for line in input_file:
		if(c_count >= num_clusters):
			break

		if(((i % gap) == 0) or (num_clusters >= num_tweets)):
			#print i
			temp = json.loads(line)
			print str(temp['id']) + ","
			c_count += 1
		i += 1

	input_file.close()

if __name__ == '__main__':
	main()
