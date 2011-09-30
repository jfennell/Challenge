#!/usr/bin/python
"""
Script find the transitive closure of the friend relation.  See help string for
more details.

This script tries to solve this problem by iteratively finding all valid words
that are within one edit distance of the current candidate.

---

For the case of 'word.list' dictionary and the starting string 'causes':
Checked the charset of the default dictionary.  It is just a-z, which makes
things simpler.

78482 is the right answer (if you include "causes" itself).
"""
import datetime
import optparse
import sys
import unittest

_USAGE = """%prog [options] word

Print the size of the transitive closure of the `friend` relation
starting from AND INCLUDING word.

Words are friends if they are within one edit (insert/delete/replace).

The universe of words is defined by a dictionary, which can be overriden."""

A_TO_Z = tuple(chr(idx) for idx in xrange(97, 123))
A_TO_Z_AND_EMPTY = tuple(list(A_TO_Z) + [''])
def all_one_edits(word):
	"""Generate all strings one edit from `word`.

	NOTE: Assumes the alphabet is [a-z]."""
	# Note that a generator is faster than appending
	# to a result list (by cProfile)

	# Avoid an extra call to len
	n = len(word)

	# Replace and delete
	for i in xrange(n):
		for char in A_TO_Z_AND_EMPTY:
			yield word[:i] + char + word[i+1:]

	# Insert
	for i in xrange(n+1):
		for char in A_TO_Z:
			yield word[:i] + char + word[i:]


def find_friend_closure(start, dictionary, verbose=False):
	"""Find the closure of the friend relation over `dictionary` starting from `start`."""
	all_friends = set([start])
	to_expand = [start]

	count = 0
	while to_expand:
		s = to_expand.pop(0)
		for w in all_one_edits(s):
			if w in dictionary and w not in all_friends:
				to_expand.append(w)
				all_friends.add(w)

		if verbose:
			count += 1
			if count > 0 and count % 1000 == 0:
				print 'Expanded %d times. %d in queue.  %d friends so far.' % (
					count, len(to_expand), len(all_friends)
				)
	return all_friends


def main(passed_args=None):
	if passed_args is None:
		passed_args = sys.argv

	parser = optparse.OptionParser(_USAGE)
	parser.add_option(
		'-d', '--dictionary',
		default='word.list',
		help='Dictionary defining the universe of words, one per line [default: %default]'
	)
	parser.add_option(
		'-v', '--verbose',
		default=False,
		action='store_true',
		help='Print out timing info during execution [default: %default]'
	)
	ops, args = parser.parse_args(args=passed_args)

	if not len(args) == 2:
		parser.error('You must specify a single word to start finding friends of.')
	word = args[1]

	with open(ops.dictionary, 'r') as f:
		dictionary = set(line.strip() for line in f)

	start = datetime.datetime.now()
	friends = find_friend_closure(word, dictionary, verbose=ops.verbose)
	if ops.verbose:
		print 'Took %s to find friends.' % (datetime.datetime.now() - start,)
	print len(friends)

	
if __name__ == '__main__':
	main()
