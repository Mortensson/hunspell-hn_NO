#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os, sys
import re
import string
# TODO: TEST: read whatever format, output iso-8859-1. Probably should
# store everything in utf-8 no matter what

# TODO: strip numbers/lines containing only numbers


pat = re.compile(ur"[\w']+|[.,!?;]", re.U)
punc_re = re.compile('[\d%s]' % re.escape(string.punctuation.replace('-', '')), re.U)
def strip_punct(s):
	return punc_re.sub('', s)

def Tokenize(data):
	""" Yields a generator for a text, which iterates by each item.
	"""
	if type(data) == list:
		data = '\n'.join(data)
	for m in pat.finditer(data):
		token = m.group(0)
		yield strip_punct(token)
	yield None

# skòra, acceptable variant skora? Maybe automatically make additional variants
# [(u'ò','o')]

cwd = os.getcwd()
# excludes = cwd + '/exclude.words'
includes = cwd + '/include_landsmaal/'
hn_NO = cwd + '/lm_NO.dic'

# Read excludes, find wordlist files.
# exclude = [a.strip() for a in open(excludes).readlines() if a.strip()]
wordlists = [includes + F for F in os.listdir(includes) if F.endswith('.TXT') or F.endswith('.txt')]

# Read replacements
# with open(cwd + '/replacements.txt') as F:
	# data = [a.strip() for a in F.read().decode('utf-8').splitlines()]
	# replacements = [(b, a) for a, b in [x.split(' -> ') for x in data]]
	# [('kjensla', 'følelse'), etc ... ]	
	# disallowed = dict([(a, b) for b, a in replacements])
	# disallowed_reverse = dict([(b, a) for b, a in replacements])


lists = []
# Read text files
for F in wordlists:
	raw = open(F).read()
	text = raw.decode('utf-8')
	processed = [a for a in Tokenize(text) if a and a.strip()]
	lists.extend(processed)
words = u'\n'.join(lists).splitlines()

# Sort unique words
sorted_words = sorted([a for a in list(set(words))])

# TODO: forbidden forms.

# TODO: replacements

# Remove lines which are only numbers
number_filter = re.compile('^\d+$')
sorted_words = [a for a in sorted_words if len(number_filter.findall(a)) == 0 and a]

# Search for replacements in replacements.txt, and replace lines in wordlist with
# corresponding replacement lines if they exist.
replaced_words = []
for a in sorted_words:
	line = False
	# if a in disallowed.keys():
		# line = '%s ph:%s' % (disallowed[a], a)
		# print >> sys.stderr, 'Disallowed word form <%s>' % a 
		# print >> sys.stderr, ' * Replacement line added\t\t %s' % line
	# if a in disallowed_reverse.keys():
		# line = '%s ph:%s' % (a, disallowed_reverse[a])
		# print >> sys.stderr, 'Allowed word form <%s> with disallowed <%s>' % (a, disallowed_reverse[a])
		# print >> sys.stderr, ' * Replacement line added\t\t %s' % line
	if line:
		replaced_words.append(line)
	else:
		replaced_words.append(a)

# Write
out = u'%d lm_NO.dic\n' % len(replaced_words)
out += u'\n'.join(replaced_words) + u'\n'
# No need for iso-8859?
# out = out.encode('iso-8859-1')
out = out.encode('utf-8')
write_out = open(hn_NO, 'w')
write_out.writelines(out)
write_out.close()
print >> sys.stderr, " * Done\n"
