#!/usr/bin/env python3
"""
This module provides a class for generating random permutations of a range
of numbers via a Feistel network over AES-128.  It operates in O(1) time
and space for each element of the permutation.
"""

# Random Permutation Package
# Copyright (c) 2022 Gary William Flake
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This package is inspired by https://github.com/dc0d32/RangePermute

import sys
import math
import random
from hashlib import sha512
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

###############################################################################

class RandomPermutation:
  """
  This class generates a random permutation of [0, N-1] using a Feistel
  network over AES-128.  It operates in O(1) time and space for each
  element and is designed to work for values of N that are too large for
  shuffle-based approaches.

  Usage:
    permute = RandomPermutation(N)
    x = permute[i]  # Get the i-th element of the permutation
    for x in permute:
      print(x)  # Print all elements of the permutation

  Methods:
    __getitem__(index): Returns the i-th element of the permutation.
    __iter__(): Returns an iterator over the permutation.
    __len__(): Returns the size of the permutation.
    __repr__(): Returns a string representation of the object.
  """

  ###########################################################################

  def __init__(self, length, seed=0, num_ciphers=3):
    """
    Initializes the RandomPermutation object.

    Parameters:
      length (int): The length / range of the permutation.
      seed (int, optional): A seed for varying permutations (default is 0).
      num_ciphers (int, optional): The number of ciphers to use (default is 3).
    """
    self.max = length
    self.seed = seed
    self.ciphers = _make_ciphers(seed, num_ciphers)
    self.a = self.b = math.ceil(math.sqrt(self.max))

  ###########################################################################

  def _feistel(self, num):
    """
    Implements a Feistel network, which is a symmetric structure used in
    the construction of block ciphers.  The Feistel structure ensures that
    decryption and encryption are very similar operations, even identical
    in some cases, and can be carried out in reverse order.

    Parameters:
      num (int): The input integer to be scrambled.

    Returns:
      int: The scrambled integer.
    """
    # Divide the input into two halves
    l, r = divmod(num, self.a)
    # Iterate over the ciphers
    for j, cipher in enumerate(self.ciphers):
      # If the index of the cipher is even
      if j % 2 == 0:
        # Scramble the right half and add it to the left half, then take
        # modulo a
        tmp = (l + self._scramble(cipher, r)) % self.a
      else:
        # If the index of the cipher is odd, do the same but take modulo b
        tmp = (l + self._scramble(cipher, r)) % self.b
      # Swap the halves
      l, r = r, tmp
    # If the number of ciphers is odd, return a*l + r, else return a*r + l
    if len(self.ciphers) % 2 == 1:
      return self.a * l + r
    return self.a * r + l

  ###########################################################################

  def _scramble(self, cipher, num):
    """
    Scrambles the input number using the provided cipher.

    Parameters:
      cipher (Cipher): The cipher to be used for scrambling.
      num (int): The number to be scrambled.

    Returns:
      int: The scrambled number.
    """
    encryptor = cipher.encryptor()
    raw = num.to_bytes(16, byteorder='little', signed=True)
    encoded = encryptor.update(raw) + encryptor.finalize()
    return int.from_bytes(encoded, byteorder='little', signed=True)

  ###########################################################################

  def __getitem__(self, index):
    """
    Generates the index'th integer in the permutation.

    Parameters:
      index (int): The index of the permutation element to get.

    Returns:
      int: The value of the permutation at the given index.

    Raises:
      IndexError: If the index is greater than or equal to the maximum value.
    """
    if isinstance(index, slice):
      start = index.start or 0
      stop = index.stop or self.max
      step = index.step or 1
      for index in range(start, stop, step):
        while True:
          index = self._feistel(index)
          if index < self.max:
            yield index
            break
      return

    elif index >= self.max:
      raise IndexError("Index out of range")
    while True:
      index = self._feistel(index)
      if index < self.max:
        return index

  ###########################################################################

  def __iter__(self):
    """
    Creates an iterator that generates each integer in the permutation.

    Yields:
      int: The next integer in the permutation.
    """
    for index in range(self.max):
      while True:
        index = self._feistel(index)
        if index < self.max:
          yield index
          break

  ###########################################################################

  def __len__(self):
    """
    Returns the length of the permutation.

    Returns:
      int: The maximum value of the permutation.
    """
    return self.max

  ###########################################################################

  def __repr__(self):
    """
    Returns a string representation of the RandomPermutation object.

    Returns:
      str: A string representation of the RandomPermutation object.
    """
    return f"RandomPermutation(max={self.max}, seed={self.seed})"

###############################################################################


###############################################################################

def _make_ciphers(seed, num_ciphers):
  """
  Private function to create a list of ciphers.

  Parameters:
    seed (int): The seed for the random number generator.
    num_ciphers (int): The number of ciphers to create.

  Returns:
    list: A list of Cipher objects.
  """
  n = 16  # the number of bytes for the key
  rng = random.Random(seed)  # a seeded random number generator
  ciphers = []
  for _ in range(num_ciphers):
    bits = rng.getrandbits(n * 8)  # 128 random bits
    raw = bits.to_bytes(n, byteorder='little')  # Convert to raw bytes
    # Hash raw bytes and take the first n bytes of the hash as the key
    key = sha512(raw).digest()[:n]
    alg = algorithms.AES(key)  # Use the key to create an AES cipher
    cipher = Cipher(alg, modes.ECB(), backend=default_backend())
    ciphers.append(cipher)
  return ciphers

###############################################################################

def _main():
  # Check if the number of arguments is less than 2
  if len(sys.argv) < 2:
    # If so, print the usage message and exit the program
    print("Usage: python3 random_permutation.py <maximum> [<seed>]")
    sys.exit(1)
  # Parse the maximum value from the command line arguments
  maximum = int(sys.argv[1])
  # If a seed is provided, parse it from the command line arguments
  # Otherwise, use 0 as the default seed
  seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
  # Create a RandomPermutation object with the provided maximum and seed
  permute = RandomPermutation(maximum, seed)
  # Iterate over the permutation and print each element
  for x in permute:
    print(x)
  sys.exit(0)

###############################################################################

if __name__ == "__main__":
  _main()

###############################################################################
