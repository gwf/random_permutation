# Random Permutation

This module provides a class `RandomPermutation` that can be used to
generate a random permutation of a given length in O(1) time and space.

## Installation

To install the module, run:

```
pip install random_permutation
```

## Usage

To use the `RandomPermutation` class, import it from the `random_permutation` module:

```python
from random_permutation import RandomPermutation

n = 2**20
p = RandomPermutation(n)
for x in p:
  print(x)
# or
for i in range(n):
  print(p[i])
```

This will output the elements of the `RandomPermutation` object. You can
use the `seed` parameter to vary the permutations and the `num_ciphers`
parameter to control the number of ciphers used.

## Testing

To run the unit tests for the `RandomPermutation` class, run:

```
python -m unittest tests.test_permutation
```

## License

This module is licensed under the MIT License.
