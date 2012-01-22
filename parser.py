#!/usr/bin/python

import sys
import re

def get_between(data, first, last, initial = 0):
	if data.find(first) == -1 or data.find(last) == -1:
		return None
	begin = data.find(first, initial) + len(first)
	end = data.find(last, begin)
	return data[begin:end]

def remove_tags(string):
	return re.sub(u'<[^>]*>','',string).strip()

def parser(filename):
	with open(filename,'r') as rates_file:
		file_as_str = rates_file.read().decode('windows-1251') #unicode(rates_file.read(),'windows-1251')
		# skip spreadsheet headers and jump to first row with movie:
		last_occurrence = file_as_str.find('<tr>', file_as_str.find('<tr>') + 4)
		while last_occurrence != -1:
			movie_fields = get_between(file_as_str,'<tr>','</tr>',last_occurrence)
			last_occurrence = file_as_str.find('<tr>',last_occurrence + 4)
			movie_str = ''
			for field in map(remove_tags, re.findall(u'<td.*$', movie_fields, flags = re.I|re.M|re.U)):
				movie_str += field.encode('utf-8') + '*'
			yield movie_str[:-1]
			
			
if __name__ == "__main__":
	if len(sys.argv) > 1:
		for arg in sys.argv[1:]:
			for movie in parser(arg):
				print movie
			
		
