#!/usr/bin/python

#cray
#cse40437
#16 February 2016

#assignment2.py
#program for performing tweet clustering using k-means algorithm

import sys
import json
from math import * 

def jaccard(x, y):	#function for calculating jaccard distance between 2 strings
	set1 = set(x.split())	#converting strings into sets
	set2 = set(y.split())

	intersect = len(set1.intersection(set2))	#calculating intersection cardinality
	
	dist = 1 - (intersect / float(len(set1) + len(set2) - intersect))	#calculating jaccard distance
	
	return dist


def read_json(data_file):	#function for reading in json file
	tweets = {}	#initializing empty dictionary for tweets

	for line in data_file:	#adding each json object to tweets dictionary
		temp = json.loads(line)
		tweets[str(temp['id'])] = temp['text']

	return tweets


def read_seeds(seed_file, num_clusters):	#function for reading in initial seeds
	clusters = []	#initializing empty cluster list

	for seed in seed_file:
		if(len(clusters) < num_clusters):	#only creating as many clusters as user specified
			if(seed[len(seed) - 2] == ','):	#removing trailing comma and newline
				clusters.append({'centroid': seed[:len(seed) - 2], 'tweets':  [seed[:len(seed) - 2]]})
			else:
				clusters.append(({'centroid': seed, 'tweets':  [seed]}))
		else:
			break

	return clusters


def cluster_tweets(tweets, clusters):	#implementation of k-means algorithm
	changes = 0
	dist = 1
	center = None
	while True:
		#assigning data points to centroids
		for ID in tweets.keys():
			#calculating jaccard distance between each tweet and each centroid
			for cluster in clusters:
				j = jaccard(tweets[ID], tweets[cluster['centroid']])
				
				if(j < dist):	#update as we find centroids closer in similarity to the tweet
					center = cluster
					dist = j
	
			if ((center != None) and (center['tweets'].count(ID) <= 0)):	#if centroid does not have tweet, update its list
				changes += 1
				center['tweets'].append(ID)
				for c in clusters:	#removing tweet from other centroid lists
					if (c['centroid'] != center['centroid']) and (len(c['tweets']) != 0) and (c['tweets'].count(ID) > 0):
						c['tweets'].remove(ID)

			dist = 1
			center = None

		#checking if any tweets changed clusters
		if(changes <= 0):	
			return clusters	#algorithm has converged
		else:
			print "new iteration"	#calculating new centroids		
			changes = 0
			for cluster in clusters:
				averages = []
				for tweet in cluster['tweets']:	#go through every tweet in every cluster to calculate its average jaccard distance to other tweets in the cluster
					sum_j = 0
					for t in cluster['tweets']:
						sum_j += jaccard(tweets[tweet], tweets[t])

					averages.append(sum_j / len(cluster['tweets']))

				if(len(averages) != 0):
					cluster['centroid'] = cluster['tweets'][averages.index(min(averages))]	#update the centroid to be the tweet with the smallest average jaccard distance 


def main():
	if(len(sys.argv) < 4):	#checking for proper number of arguments
		sys.exit("Error:  Not enough arguments\npython assignment2.py [number of clusters] [dataset json] [initial seeds]")

	num_clusters = int(sys.argv[1])	#number of clusters to create

	try:	#attempting to open json file
		data_file = open(sys.argv[2], "r")
	except:
		sys.exit("Error:  Could not open " + sys.argv[2])

	try:	#attempting to open initial seed file
		seed_file = open(sys.argv[3], "r")
	except:
		sys.exit("Error:  Could not open " + sys.argv[3])
	
	tweets = read_json(data_file)	#initializing dictionary of tweets (key = tweet ID, value = tweet text)	
	data_file.close()	

	clusters = read_seeds(seed_file, num_clusters)	#initializing list of clusters
	seed_file.close()

	clusters = cluster_tweets(tweets, clusters) #performing k-means

	output = open("cluster_output.txt", "w")	#writing to output file	
	i = 0
	for cluster in clusters:
		output.write(str(i) + ":  " + ','.join(cluster['tweets']) + "\n")
		i += 1
	
	output.close()

if __name__ == '__main__':
	main()
