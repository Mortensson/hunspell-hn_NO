#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os, sys
import re

# TODO: TEST: read whatever format, output iso-8859-1. Probably should
# store everything in utf-8 no matter what

# TODO: strip numbers/lines containing only numbers


# skòra, acceptable variant skora? Maybe automatically make additional variants
# [(u'ò','o')]

cwd = os.getcwd()
excludes = cwd + '/exclude.words'
includes = cwd + '/include/'
hn_NO = cwd + '/hn_NO.dic'

# Read excludes, find wordlist files.
exclude = [a.strip() for a in open(excludes).readlines() if a.strip()]
wordlists = [includes + F for F in os.listdir(includes) if F.endswith('.words')]

# Read replacements
with open(cwd + '/replacements.txt') as F:
	data = [a.strip() for a in F.read().decode('utf-8').splitlines()]
	replacements = [(b, a) for a, b in [x.split(' -> ') for x in data]]
	# [('kjensla', 'følelse'), etc ... ]	
	disallowed = dict([(a, b) for b, a in replacements])
	disallowed_reverse = dict([(b, a) for b, a in replacements])


lists = []
# Read text files
for F in wordlists:
	raw = open(F).read()
	text = raw.decode('utf-8')
	lists.append(text)
words = u'\n'.join(lists).splitlines()

# Sort unique words
sorted_words = sorted([a for a in list(set(words)) if a not in exclude])

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
	if a in disallowed.keys():
		line = '%s ph:%s' % (disallowed[a], a)
		print >> sys.stderr, 'Disallowed word form <%s>' % a 
		print >> sys.stderr, ' * Replacement line added\t\t %s' % line
	if a in disallowed_reverse.keys():
		line = '%s ph:%s' % (a, disallowed_reverse[a])
		print >> sys.stderr, 'Allowed word form <%s> with disallowed <%s>' % (a, disallowed_reverse[a])
		print >> sys.stderr, ' * Replacement line added\t\t %s' % line
	if line:
		replaced_words.append(line)
	else:
		replaced_words.append(a)

# Write
out = u'%d hn_NO.dic\n' % len(replaced_words)
out += u'\n'.join(replaced_words) + u'\n'
# No need for iso-8859?
# out = out.encode('iso-8859-1')
out = out.encode('utf-8')
write_out = open(hn_NO, 'w')
write_out.writelines(out)
write_out.close()
print >> sys.stderr, " * Done\n"
