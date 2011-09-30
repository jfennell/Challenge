"""
Two words are friends if they have a Levenshtein distance of 1. That is, you
can add, remove, or substitute exactly one letter in word X to create word Y. A
word's social network consists of all of its friends, plus all of their
friends, and all of their friends' friends, and so on. Write a program to tell
us how big the social network for the word "causes" is, using this word list.

This module tries to solve this problem.

---

Checked the charset of the dictionary.  It is just a-z, which makes things simpler.

78482 is the right answer (if you include "causes" itself).
"""
import datetime
import unittest

A_TO_Z = tuple(chr(idx) for idx in xrange(97, 123))
A_TO_Z_AND_EMPTY = tuple(list(A_TO_Z) + [''])
def all_one_edits(word):
	"""Generate all strings one edit from `word`."""
	# Note that a generator is faster than appending
	# to a result list (by cProfile)

	# Avoid an extra call to len
	n = len(word)

	result = []
	# Replace and delete
	for i in xrange(n):
		for char in A_TO_Z_AND_EMPTY:
			yield word[:i] + char + word[i+1:]

	# Insert
	for i in xrange(n+1):
		for char in A_TO_Z:
			yield word[:i] + char + word[i:]


def one_edit_find_friend_closures(start):
	"""Factory function for a trie loaded with word.list."""
	# Get the dictionary
	dictionary = set()
	with open('word.list', 'r') as f:
		for line in f:
			dictionary.add(line.strip())

	all_friends = set([start])
	to_expand = [start]

	count = 0
	while to_expand:
		s = to_expand.pop(0)
		for w in all_one_edits(s):
			if w in dictionary and w not in all_friends:
				to_expand.append(w)
				all_friends.add(w)

		count += 1
		if count > 0 and count % 1000 == 0:
			print 'Expanded %d times. %d in queue.  %d friends so far.' % (
				count, len(to_expand), len(all_friends)
			)
	return all_friends


def main():
	start = datetime.datetime.now()
	friends = one_edit_find_friend_closures('causes')
	print 'Took %s to find friends.' % (datetime.datetime.now() - start,)
	print 'There are %d friends.' % (len(friends),)

	
if __name__ == '__main__':
	main()
