#!/usr/bin/python

import urllib2
import urllib
import sys
import re
import json
from parser import get_between

cookie = {"uu": "###",
	"id": "###",
	"cs": "###"}

def cookie_to_str(cookie_dict):
	res = ''
	for key in cookie_dict:
		res += str(key) + '=' + str(cookie_dict[key]) + '; '
	return res.strip()


def imdb_rate_movie(link,rate):
	global cookie
	imdb_url_str = 'http://www.imdb.com'
	path = "/ratings/_ajax/title"
	tt = link.split('/')[-2]
	
	data_dict = {"tconst": tt,
		"rating": str(rate),
		"auth": None,
		"tracking_tag": "title-maindetails"}
		
	# updaiting cookie & data
	headers_dict = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1",
		"Cookie": cookie_to_str(cookie),
		"Pragma": "no-cache",
		"Cache-Control": "no-cache"}
	request = urllib2.Request(link,None,headers_dict)
	response = urllib2.urlopen(request)
	
	for header in response.info().headers:
		if header.startswith('Set-Cookie'):
			pair = header.replace('Set-Cookie:','').split(';')[0].strip().split('=')
			cookie[pair[0]] = pair[1]
	data_dict["auth"] = get_between(response.read(),'data-auth="','"')

	# movie ranking
	data = urllib.urlencode(data_dict)
	headers_dict.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1",
		"X-Requested-With": "XMLHttpRequest",
		"Referer": link,
		"Content-Length": str(len(data)),
		"Cookie": cookie_to_str(cookie)})
	
	request = urllib2.Request(imdb_url_str + path,data,headers_dict)
	response = urllib2.urlopen(request)
	if not json.loads(response.read())["status"] == 200:
		sys.exit(1)
	
if __name__ == "__main__":
	if len(sys.argv) > 2: # read from command line
		if sys.argv[2] != '-':
			imdb_rate_movie(sys.argv[1],int(sys.argv[2]))

