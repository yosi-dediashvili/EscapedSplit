EscapedSplit
============

Implementation of an escapable split() function for python.

Usage exmples:
```python
# Import the function.
from EscapedSplit import escaped_split
# The following sentecnes will evaluate to true.
escaped_split("a|b", "|") == ["a", "b"]
escaped_split("a|b^|c", "|", "^") == ["a", "b|c"]
escaped_split("a|b^^|c", "|", "^") == ["a", "b^", "c"]
escaped_split("a|b^^^|c", "|", "^") == ["a", "b^|c"]
escaped_split("a|b|c|") == ["a", "b", "c"]
```


