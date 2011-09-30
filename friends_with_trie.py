"""
Two words are friends if they have a Levenshtein distance of 1. That is, you
can add, remove, or substitute exactly one letter in word X to create word Y. A
word's social network consists of all of its friends, plus all of their
friends, and all of their friends' friends, and so on. Write a program to tell
us how big the social network for the word "causes" is, using this word list.

This module tries to solve this problem by creating a trie that can find words
within n edits of a query string that are in a dictinoary.
---

Checked the charset of the dictionary.  It is just a-z, which makes things simpler.

78482 is the right answer (if you include "causes" itself).
"""
import datetime
import unittest

class Node(object):
	__slots__ = ['char', 'is_word', 'children']

	def __init__(self, char=None, is_word=False):
		self.char = char   # Could be dropped to lower memory usage
		self.is_word = is_word
		self.children = {}

	def __str__(self):
		return '%s: %s' % (self.char, self.is_word)

	def __repr__(self):
		return '%s(%s, %s)' % (self.__class__, self.char, self.is_word)

class Trie(object):
	"""Naive trie implementation to allow for quick edit distance computation."""

	def __init__(self):
		self.root = Node()

	def add(self, s):
		curr = self.root
		for c in s:
			nxt = curr.children.get(c)
			if nxt is None:
				nxt = Node(c)
				curr.children[c] = nxt
			curr = nxt
		nxt.is_word = True

	def find_edits(self, s, maxedit):
		"""Return all words in the trie within maxedit edits of s.

		Note that an edit is an insert, delete, or replace.
		"""
		strings = []
		self._find_edits('', s, maxedit, self.root, strings)
		return strings

	# XXX: Logic is well tested, but kind of ghetto... Should be simplified.
	def _find_edits(self, prefix, suffix, maxedit, node, strings):
		if maxedit < 0:
			return

		# If our consumed string matches a word in the dict, add it
		if len(suffix) == 0 and node.is_word:
			strings.append(prefix)

		# Make sure that no child chars can match if there is no suffix
		c = suffix[0] if suffix else ''

		# Delete -- Remove the leading character of the suffix and try again
		# from the same place
		if maxedit > 0 and len(suffix) > 0:
			self._find_edits(prefix, suffix[1:], maxedit-1, node, strings)

		for child in node.children.itervalues():
			new_prefix = prefix + child.char
			if c == child.char:
				# No edit
				self._find_edits(new_prefix, suffix[1:], maxedit, child, strings)
			elif maxedit > 0:
				if len(suffix) > 0:
					# Replace
					self._find_edits(new_prefix, suffix[1:], maxedit-1, child, strings)
				# Insert
				self._find_edits(new_prefix, suffix, maxedit-1, child, strings)

	def __contains__(self, s):
		return self._contains_from_node(s, self.root)

	def _contains_from_node(self, s, node):
		curr = node
		for c in s:
			nxt = curr.children.get(c)
			if nxt is None:
				return False
			curr = nxt
		return nxt.is_word

	def __str__(self):
		lines = []
		self._str_helper(self.root, 0, lines)
		return '\n'.join(lines)

	def _str_helper(self, node, depth, lines):
		lines.append(' '*depth + str(node))
		for child in node.children.itervalues():
			self._str_helper(child, depth+1, lines)


def get_loaded_trie():
	"""Factory function for a trie loaded with word.list."""
	t = Trie()
	with open('word.list', 'r') as f:
		for line in f:
			t.add(line.strip())
	return t


def find_friend_closure(start):
	"""Find the transitive closure of the friend relation, starting with `start`."""
	t = get_loaded_trie()

	all_friends = set([start])
	to_expand = [start]

	count = 0
	while to_expand:
		s = to_expand.pop(0)
		friends = t.find_edits(s, 1)
		for f in friends:
			if f not in all_friends:
				to_expand.append(f)
				all_friends.add(f)

		count += 1
		if count > 0 and count % 1000 == 0:
			print 'Expanded %d times. %d in queue.  %d friends so far.' % (
				count, len(to_expand), len(all_friends)
			)
	return all_friends


def main():
	start = datetime.datetime.now()
	friends = find_friend_closure('causes')
	print 'Took %s to find friends.' % (datetime.datetime.now() - start,)
	print 'There are %d friends.' % (len(friends),)


if __name__ == '__main__':
	main()
