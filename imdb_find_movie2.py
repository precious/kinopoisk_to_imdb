#!/usr/bin/python

import urllib
import urllib2
import re
import sys
from romanization import romanize
from parser import get_between, remove_tags

imdb_url_str = 'http://www.imdb.com'

def get_response(path,headers = None):
	global imdb_url_str
	headers_dict = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1"}
	request = urllib2.Request(imdb_url_str + path,None,headers_dict)
	return urllib2.urlopen(request)
	
def check_imdb_movie_year(path,year):
	global imdb_url_str
	response = get_response(path)
	re_html_h1_header = re.compile('(?P<h1><h1.*?class="header".*?</h1>)',re.U|re.M|re.I|re.S)
	html_h1_header = re_html_h1_header.search(response.read()).group('h1')
	return year in html_h1_header
	
def get_movie_url(movie_data):
	global imdb_url_str
	params_dict = {'s': 'tt'}
	data_list = movie_data.split('*')	
	params_dict['q'] = data_list[1] if data_list[1] else romanize(data_list[0])

	response = get_response('/find?' + urllib.urlencode(params_dict))
	
	# first check whether response is desired movie page
	re_movie_url = re.compile(r'(?P<path>/title/[\d\w]+/)')
	response_url = response.geturl()
	if re_movie_url.search(response_url):
		return response_url

	# then check 1st link to movie in response page
	response_str = response.read()
	url_match = re_movie_url.search(response_str)
	
	if url_match and  check_imdb_movie_year(url_match.group('path'),data_list[2]):
		return imdb_url_str + url_match.group('path')
	
	# finally try to find movie in exact matches table
	if response_str.find('Titles (Exact Matches)') != -1:
		table_str = get_between(response_str,'<table>','</table>',response_str.find('Titles (Exact Matches)'))
		for row in re.findall(r'<tr>.*?</tr>',table_str,flags = re.I|re.M|re.U|re.S):
			if data_list[2] in row:
				return imdb_url_str + get_between(row,'href="','"')

