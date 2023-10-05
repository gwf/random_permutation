"""
This module contains unit tests for the RandomPermutation class.
"""

import unittest
import random
from random_permutation import RandomPermutation

class TestPermutation(unittest.TestCase):
  """
  Unit Test class for testing the RandomPermutation class.
  """

  def setUp(self):
    """
    Setup function to initialize the test case.
    """
    self.n = random.randint(10, 100)
    self.p = RandomPermutation(self.n)

  def test_random_permutation_length(self):
    """
    Test case to check the length of the random permutation.
    """
    self.assertEqual(len(self.p), self.n)

  def test_random_permutation_content(self):
    """
    Test case to check the content of the random permutation.
    """
    self.assertEqual(set(range(self.n)), set(self.p))

  def test_random_permutation_uniqueness(self):
    """
    Test case to check the uniqueness of the elements in the random permutation.
    """
    self.assertEqual(len(set(self.p)), len(list(self.p)))

  def test_random_permutation_order(self):
    """
    Test case to check the order of the elements in the random permutation.
    """
    self.assertNotEqual(list(range(self.n)), list(self.p))

  def test_random_permutation_repr(self):
    """
    Test case to check the string representation of the random permutation.
    """
    self.assertEqual(repr(self.p),
                     f"RandomPermutation(max={self.n}, seed={self.p.seed})")

  def test_random_permutation_iter(self):
    """
    Test case to check the iterator of the random permutation.
    """
    self.assertEqual(sorted(list(self.p)), list(range(self.n)))

  def test_random_permutation_index(self):
    """
    Test case to check the index operator of the random permutation.
    """
    p = self.p
    for i in range(self.n):
      self.assertEqual(self.p[i], p[i])

  def test_random_permutation_index_out_of_range(self):
    """
    Test case to check the index operator of the random permutation for an
    out-of-range index.
    """
    with self.assertRaises(IndexError):
      self.p[self.n]

  def test_random_permutation_index_negative(self):
    """
    Test case to check the index operator of the random permutation for a
    negative index.
    """
    self.assertEqual(self.p[-1], self.p[self.n - 1])

  def test_random_permutation_index_slice(self):
    """
    Test case to check the index operator of the random permutation for a
    slice.
    """
    self.assertEqual(list(self.p[:]), list(self.p))

  def test_random_permutation_index_slice_negative(self):
    """
    Test case to check the index operator of the random permutation for a
    negative slice.
    """
    self.assertEqual(list(self.p[:-1]), list(self.p)[:self.n - 1])
