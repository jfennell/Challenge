import unittest

from friends_with_trie import Trie

def all_strings_of_n(alphabet, n):
	"""Generate all strings of length `n` using characters from `alphabet`."""
	if n <= 0:
		yield ''
	else:
		for string in all_strings_of_n(alphabet, n-1):
			for char in alphabet:
				yield string + char


class TestTrie(unittest.TestCase):
	def setUp(self):
		self.t = Trie()

	def test_adding_and_containment(self):
		words = ['baz', 'foo', 'fob', 'far', 'food']
		for w in words:
			self.t.add(w)

		for w in words:
			assert w in self.t, 'Expected %s in the trie.'

	def test_single_edits_sparse(self):
		"""Check edits from a single string in the trie."""
		self.t.add('pizza')
		expected_contents = set(['pizza'])

		# Replace
		self.assertEqual(set(self.t.find_edits('zizza', 1)), expected_contents)
		self.assertEqual(set(self.t.find_edits('pizaa', 1)), expected_contents)
		self.assertEqual(set(self.t.find_edits('pizzz', 1)), expected_contents)

		# Insert
		self.assertEqual(set(self.t.find_edits('izza', 1)), expected_contents)
		self.assertEqual(set(self.t.find_edits('piza', 1)), expected_contents)
		self.assertEqual(set(self.t.find_edits('pizz', 1)), expected_contents)

		# Delete
		self.assertEqual(set(self.t.find_edits('ppizza', 1)), expected_contents)
		self.assertEqual(set(self.t.find_edits('piizza', 1)), expected_contents)
		self.assertEqual(set(self.t.find_edits('pizzaa', 1)), expected_contents)

	def test_single_edits_dense(self):
		"""Pack the trie with all 3-char strings, then check that we get the
		right number of edits.
		"""
		alphabet = 'abcdefghijk'
		alpha_len = len(alphabet)
		n = 3
		for word in all_strings_of_n(alphabet, n):
			self.t.add(word)

		# Insert (any char in the alphabet anywhere)
		# 'a' and 'b' can be inserted on either side of itself ('aab' and 'abb')
		# so we subtrace off 2 to avoid overcounting.
		self.assertEqual(len(set(self.t.find_edits('ab', 1))), 3*alpha_len - 2)

		# Remove (any char in our string)
		self.assertEqual(len(set(self.t.find_edits('bdfg', 1))), 4)

		# Replacement (any char in string with a *different* char + exact match)
		self.assertEqual(len(set(self.t.find_edits('ijk', 1))), 3*(alpha_len-1) + 1)

	def test_longer_edits(self):
		# Test empty trie
		self.assertEqual(set(self.t.find_edits('', 2000000000)), set())

		STAR_WARS = [
			'Luke Skywalker', 'Anakin Skywalker', 'Jedi Knights',
			'Jedi', 'force grip', 'force throw', 'force push', 'force pull',
			'force lift', 'Lucas Skywalker', 'George Lucas', 'george lucas'
		]
		for midichlorian in STAR_WARS:
			self.t.add(midichlorian)

		# Test case-sensitivity
		self.assertEqual(set(self.t.find_edits('George Lucas', 1)), set(['George Lucas']))
		self.assertEqual(set(self.t.find_edits('George Lucas', 2)), set(['George Lucas', 'george lucas']))

		# Assorted long find_edits
		self.assertEqual(set(self.t.find_edits('Looks Skywalker', 3)), set(['Luke Skywalker', 'Lucas Skywalker']))
		self.assertEqual(set(self.t.find_edits('Skywalker', 6)), set(['Luke Skywalker', 'Lucas Skywalker']))
		self.assertEqual(set(self.t.find_edits('force lightning', 6)), set(['force lift']))
		self.assertEqual(set(self.t.find_edits('farce lucas', 5)), set(['force push', 'force lift', 'George Lucas', 'force pull', 'george lucas']))
		self.assertEqual(set(self.t.find_edits('Jedi ! Knights', 2)), set(['Jedi Knights']))


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

if __name__ == '__main__':
	unittest.main()
