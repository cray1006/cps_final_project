# -*- coding: utf-8 -*-
#Christopher Ray
#Professor Wang
#CSE 40437

#extract_text.py
#Program for extracting cluster text

import sys
from io import open
from nltk.tokenize import word_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import state_union
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem import PorterStemmer
from nltk import bigrams
import math
import nltk
import json
import string
import re

negative_words = 'negativeWords.txt'
positive_words = 'positiveWords.txt'

positive_dictionary = []
negative_dictionary = []

ps = PorterStemmer()

punctuation = list(string.punctuation)

defaultStop = ['rt', '#rt', '#follow', 'via', '…', 'http', ':/', 'https://t.co/rbue24q9zh', 'amp', 'u', 'says',
               '️', '\U0001f644', '\U0001f644', '\U0001f3fc']

syriaStop = [':\\', 'say', 'co', '#breaking', '#news', '0', '1', '2', '3', '4', '5', '6', '7',
             '8', '9', '10', 'w', '”']

newsStop = ['@ap', '@ajenglish', '@ajarabic', '@cbsdavidmartin', '@france24', '@cnn', '@yahoonews',
            '@reuters', '@cnnbrk', '@breakingnews', '@buzzfeedandrew', '@nbcnews', '@nytimes', '@time',
            '@huffingtonpost', '@bbcnews', '@guardian', '@bbcbreaking', '@mailonline', '@sana_english',
            '@foreignpolicy', '@reutersworld', '@lbci_news_en', '@foxnews', '@bbcworld', '@youranonnews',
            '@rt_com', '@usatoday', '@abc', '@cnni', '@washingtonpost', '@newsbreaker', '@wsj', '@sharethis']

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

stop = stopwords.words('english') + punctuation + defaultStop + syriaStop + newsStop

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=True):
    tokens = tokenize(s.lower())
    return tokens

def main():
	try:
		cluster_file = open(sys.argv[1], "r")
	except:
		sys.exit("Could not open cluster file")

	try:
		tweet_file = open(sys.argv[2], "r", encoding = "utf-8")
	except:
		sys.exit("Could not open tweet file")

	try:
		pos_file = open(positive_words, "r", encoding = "latin-1")
	except:
		sys.exit("Could not open positive words file.")

	try:
		neg_file = open(negative_words, "r", encoding = "latin-1")
	except:
		sys.exit("Could not open positive words file.")

	output_file = open("new_clusters.txt", "w", encoding = "utf-8")

	for line in pos_file:
		try:
			positive_dictionary.append(ps.stem(line.strip()))
		except:
			continue
	pos_file.close()

	for line in neg_file:
		try:
			negative_dictionary.append(ps.stem(line.strip()))
		except:	
			continue
	neg_file.close()

	tweets = {}

	for line in tweet_file:
		temp = json.loads(line)
		tweets[str(temp['id'])] = temp['text']

	tweet_file.close()

	i = 0
	for line in cluster_file:
		no_cID = line.split()
		if(len(no_cID) >= 2):
			t_list = no_cID[1].split(',')
			temp = []
			for t in t_list:
				temp.append(tweets[str(t)])

			cluster_string = "\t".join(temp)
			cluster_string = cluster_string.replace('\n', '\t')

			tokens = preprocess(cluster_string)
			#print tokens

			terms_stop = [term for term in tokens if term not in stop and not term.startswith(('#', '@'))]  
			
			tagged = nltk.pos_tag(tokens)

			adjectives = []
			pos = 0
			neu = 0
			neg = 0
			score = 0

			#print tagged
			for word in tagged:
				if word[1] == 'JJ' or word[1] == 'JJR' or word[1] == 'JJS':
					adjectives.append(word[0])

			count_bigrams = Counter()
			cluster_bigrams = bigrams(terms_stop)
			count_bigrams.update(cluster_bigrams)

			#print adjectives 

			for adjective in adjectives:
				if ps.stem(adjective) in positive_dictionary:
					pos = pos + 1
            			if ps.stem(adjective) in negative_dictionary:
               			 	neg = neg + 1
				else:
					neu = neu + 1

			score = (pos - neg) / math.sqrt(len(tokens))
			#print score

			output_file.write(unicode(str(i) + ": " + str(count_bigrams.most_common(3)) + "\t" + str(score) + "\t" + str(pos) + "\t" + str(neg) +  "\t" + str(neu) + "\n"))
			i += 1
			
			
	cluster_file.close()
	output_file.close()

if __name__ == '__main__':
	main()
