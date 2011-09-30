import unittest

from friends import all_one_edits


class TestSingleEdit(unittest.TestCase):
	def test_empty_str(self):
		self.assertEqual(
			set(all_one_edits('')),
			# You don't get the empty string, since that would be 0 edits away
			set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
			'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
			'z'])
		)

	def test_one_char(self):
		self.assertEqual(
			set(all_one_edits('X')),
			set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
			'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
			'z', '', 'aX', 'bX', 'cX', 'dX', 'eX', 'fX', 'gX', 'hX', 'iX',
			'jX', 'kX', 'lX', 'mX', 'nX', 'oX', 'pX', 'qX', 'rX', 'sX', 'tX',
			'uX', 'vX', 'wX', 'xX', 'yX', 'zX', 'Xa', 'Xb', 'Xc', 'Xd', 'Xe',
			'Xf', 'Xg', 'Xh', 'Xi', 'Xj', 'Xk', 'Xl', 'Xm', 'Xn', 'Xo', 'Xp',
			'Xq', 'Xr', 'Xs', 'Xt', 'Xu', 'Xv', 'Xw', 'Xx', 'Xy', 'Xz'])
		)

	def test_multi_char(self):
		self.assertEqual(
			set(all_one_edits('XYZ')),
			set(['aYZ', 'bYZ', 'cYZ', 'dYZ', 'eYZ', 'fYZ', 'gYZ', 'hYZ', 'iYZ',
			'jYZ', 'kYZ', 'lYZ', 'mYZ', 'nYZ', 'oYZ', 'pYZ', 'qYZ', 'rYZ',
			'sYZ', 'tYZ', 'uYZ', 'vYZ', 'wYZ', 'xYZ', 'yYZ', 'zYZ', 'YZ',
			'XaZ', 'XbZ', 'XcZ', 'XdZ', 'XeZ', 'XfZ', 'XgZ', 'XhZ', 'XiZ',
			'XjZ', 'XkZ', 'XlZ', 'XmZ', 'XnZ', 'XoZ', 'XpZ', 'XqZ', 'XrZ',
			'XsZ', 'XtZ', 'XuZ', 'XvZ', 'XwZ', 'XxZ', 'XyZ', 'XzZ', 'XZ',
			'XYa', 'XYb', 'XYc', 'XYd', 'XYe', 'XYf', 'XYg', 'XYh', 'XYi',
			'XYj', 'XYk', 'XYl', 'XYm', 'XYn', 'XYo', 'XYp', 'XYq', 'XYr',
			'XYs', 'XYt', 'XYu', 'XYv', 'XYw', 'XYx', 'XYy', 'XYz', 'XY',
			'aXYZ', 'bXYZ', 'cXYZ', 'dXYZ', 'eXYZ', 'fXYZ', 'gXYZ', 'hXYZ',
			'iXYZ', 'jXYZ', 'kXYZ', 'lXYZ', 'mXYZ', 'nXYZ', 'oXYZ', 'pXYZ',
			'qXYZ', 'rXYZ', 'sXYZ', 'tXYZ', 'uXYZ', 'vXYZ', 'wXYZ', 'xXYZ',
			'yXYZ', 'zXYZ', 'XaYZ', 'XbYZ', 'XcYZ', 'XdYZ', 'XeYZ', 'XfYZ',
			'XgYZ', 'XhYZ', 'XiYZ', 'XjYZ', 'XkYZ', 'XlYZ', 'XmYZ', 'XnYZ',
			'XoYZ', 'XpYZ', 'XqYZ', 'XrYZ', 'XsYZ', 'XtYZ', 'XuYZ', 'XvYZ',
			'XwYZ', 'XxYZ', 'XyYZ', 'XzYZ', 'XYaZ', 'XYbZ', 'XYcZ', 'XYdZ',
			'XYeZ', 'XYfZ', 'XYgZ', 'XYhZ', 'XYiZ', 'XYjZ', 'XYkZ', 'XYlZ',
			'XYmZ', 'XYnZ', 'XYoZ', 'XYpZ', 'XYqZ', 'XYrZ', 'XYsZ', 'XYtZ',
			'XYuZ', 'XYvZ', 'XYwZ', 'XYxZ', 'XYyZ', 'XYzZ', 'XYZa', 'XYZb',
			'XYZc', 'XYZd', 'XYZe', 'XYZf', 'XYZg', 'XYZh', 'XYZi', 'XYZj',
			'XYZk', 'XYZl', 'XYZm', 'XYZn', 'XYZo', 'XYZp', 'XYZq', 'XYZr',
			'XYZs', 'XYZt', 'XYZu', 'XYZv', 'XYZw', 'XYZx', 'XYZy', 'XYZz'])
		)


if __name__ == '__main__':
	unittest.main()
