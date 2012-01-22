#!/usr/bin/python
# -*- coding: utf-8 -*-

# BGN/PCGN system
dictionary = {u"а": "a", u"б": "b", u"в": "v", u"г": "g", u"д": "d", u"е": ["e","ye"], u"ё": "yo", u"ж": "zh", u"з": "z", u"и": "i", u"й": "y", u"к": "k", u"л": "l", u"м": "m", u"н": "n", u"о": "o", u"п": "p", u"р": "r", u"с": "s", u"т": "t", u"у": "u", u"ф": "f", u"х": "kh", u"ц": "ts", u"ч": "ch", u"ш": "sh", u"щ": "shch", u"ъ": '', u"ы": "y", u"ь": '', u"э": "e", u"ю": "yu", u"я": "ya"}
vowels = u"аеёиоуэюя"

def romanize(string):
	string = unicode(string,'utf-8')
	global dictionary, vowels
	result = ''
	previous = ' '
	for letter in string:
		letter = letter.lower()
		if letter in dictionary:
			if isinstance(dictionary[letter],list):
				if previous in ' \t' + vowels:
					result += dictionary[letter][1]
				else:
					result += dictionary[letter][0]
			else:
				result += dictionary[letter]
		else:
			result += letter
		previous = letter
	return result
		
if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		for arg in sys.argv[1:]:
			print(romanize(arg))
