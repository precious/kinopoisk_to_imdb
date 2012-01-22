#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys; reload(sys); sys.setdefaultencoding('utf-8')
from imdb_find_movie import get_movie_url

movie_data = '*'
#with open('lol','r') as data_file:
#	while movie_data:
#		movie_data = data_file.readline()
#		data_list = movie_data.split('*')
#		movie_name = data_list[1] if data_list[1] else data_list[0]
#	
#		url = get_movie_url(movie_data)
#		print movie_name, ' | ', url if url else 'movie not found; see error.log'

while True:
	input_line = sys.stdin.readline().strip()
	if input_line == '':
		break
	print '!',input_line


