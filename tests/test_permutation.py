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
    self.permutation = RandomPermutation(self.n)

  def test_random_permutation_length(self):
    """
    Test case to check the length of the random permutation.
    """
    self.assertEqual(len(self.permutation), self.n)

  def test_random_permutation_content(self):
    """
    Test case to check the content of the random permutation.
    """
    self.assertEqual(set(range(self.n)), set(self.permutation))

  def test_random_permutation_uniqueness(self):
    """
    Test case to check the uniqueness of the elements in the random permutation.
    """
    self.assertEqual(len(set(self.permutation)), len(self.permutation))

  def test_random_permutation_order(self):
    """
    Test case to check the order of the elements in the random permutation.
    """
    self.assertNotEqual(list(range(self.n)), list(self.permutation))
