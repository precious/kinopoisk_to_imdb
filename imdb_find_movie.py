#!/usr/bin/python

import urllib
# import urllib2
import sys
import json
import imdb_find_movie2
from romanization import romanize


def get_movie_url(movie_data):
	url = 'http://www.deanclatworthy.com/imdb/'
	params_dict = {}
	data_list = movie_data.split('*')
	if len(data_list) < 3:
		raise ValueError('invalid movie data')
	
	# first trying to find movie using api
	params_dict['q'] = data_list[1] if data_list[1] else romanize(data_list[0])
	params_dict['year'] = data_list[2]
	try:
		# first trying to find movie using api
		response = urllib.urlopen(url + '?' + urllib.urlencode(params_dict))
		response_dict = json.loads(response.read())
		if 'imdburl' in response_dict:
			return response_dict['imdburl']
		# then trying own function
		movie_url = imdb_find_movie2.get_movie_url(movie_data)
		if movie_url:
			return movie_url	
	except:
		pass

	return None


if __name__ == "__main__":
	if len(sys.argv) > 1: # read from command line
		for data in sys.argv[1:]:
			url = get_movie_url(data)
			if url: print url 
	else:
		while True: # read from stdin
			input_line = sys.stdin.readline().strip()
			if input_line == '':
				break
			url = get_movie_url(input_line)
			if url: print url

