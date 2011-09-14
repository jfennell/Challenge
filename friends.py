"""
Two words are friends if they have a Levenshtein distance of 1. That is, you
can add, remove, or substitute exactly one letter in word X to create word Y. A
word's social network consists of all of its friends, plus all of their
friends, and all of their friends' friends, and so on. Write a program to tell
us how big the social network for the word "causes" is, using this word list.

This module tries to solve this problem.

---

Checked the charset of the dictionary.  It is just a-z, which makes things simpler.
"""
import datetime

class Node(object):
	__slots__ = ['char', 'is_word', 'children']

	def __init__(self, char=None, is_word=False):
		self.char = char 
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

	def _find_edits(self, prefix, suffix, maxedit, node, strings):
		if maxedit < 0:
			return

		# If our consumed string matches a word in the dict, add it
		if len(suffix) == 0:
			if node.is_word:
				strings.append(prefix)
			return

		c = suffix[0]

		for child in node.children.itervalues():
			if c == child.char:
				# No edit
				self._find_edits(prefix + c, suffix[1:], maxedit, child, strings)
			else:
				# Replace
				self._find_edits(prefix + child.char, suffix[1:], maxedit-1, child, strings)
			# Insert
			self._find_edits(prefix + child.char, suffix, maxedit-1, child, strings)
			# Delete
			self._find_edits(prefix, suffix[1:], maxedit-1, child, strings)
			
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

def test_trie():
	t = Trie()
	words = ['baz', 'foo', 'fob', 'far', 'food']
	for w in words:
		t.add(w)

	print str(t)

	for w in words:
		assert w in t, 'Expected %s in the trie.'

def big_load():
	"""Quick test to see how long/how much memory it takes
	to load everything into the trie.  Watching mem in top.

	Take 3 seconds and 206MB to load everything, which is acceptable to me.
	"""
	t = Trie()
	start = datetime.datetime.now()
	with open('word.list', 'r') as f:
		for i, line in enumerate(f):
			t.add(line.strip())

			if i > 0 and i % 1000 == 0:
				print datetime.datetime.now(), i
	print 'Elapsed: %s' % (datetime.datetime.now() - start)
	raw_input('Waiting')

import pprint
def test_causes():
	print 'Loading trie'
	t = get_loaded_trie()
	print 'Getting edits'
	pprint.pprint(t.find_edits('causes', 1))

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
		print 'Expanded %d times. %d in queue.  %d friends so far.' % (count, len(to_expand), len(all_friends))
	return all_friends

def main():
	start = datetime.datetime.now()
	friends = find_friend_closure('causes')
	print 'Took %s to find friends.' % (datetime.datetime.now() - start,)
	print 'There are %d friends.' % (len(friends),)
	
if __name__ == '__main__':
	#test_trie()
	#big_load()
	test_causes()
	#main()
