import re
# We need the special chars of the re module in order to decide whether or not
# we should escape the escape_char and the separator in our re statements.
from sre_parse import SPECIAL_CHARS as RE_SPECIAL_CHARS
from string import Template

def _compile_re(template, separator, escape_char):
	"""
	Cosntructs the regex expression, and escapes the escape_char in the separ-
	ator before it places them in the template if they are contained in  the 
	RE_SPECIAL_CHARS string.
	"""

	# Escape the escape_char and the separator.
	if escape_char in RE_SPECIAL_CHARS:
		escape_char = "\\" + escape_char
	if separator in RE_SPECIAL_CHARS:
		separator = "\\" + separator

	return re.compile(template.substitute(
		escape_char=escape_char, separator=separator))

def _remove_escaping(s, separator, escape_char):
	"""
	Removes the escape_char from the string s in any place that it's considered
	to be an escape char. separator is the char that splits the string.

	The escape char will be considered as such in two cases. The first is if it 
	comes right before the separator char, in any place inside the string. The 
	second, is if it comes before another escape char, and it placed at the end 
	of the string. 

	Escape char at the middle of the string is not considered to be an escape
	char.
	"""
	def subber(match):
		""" 
		Replaces the matched substring with one that does not contains the 
		escape char.
		"""
		# If the separator was present, we need to remove the escape char that
		# came before him. And remove any escape char that comes right before 
		# it as many time as needed.
		if match.group(0).endswith(separator):
			return escape_char * ((len(match.group(0)) - 2) / 2) + separator
		# Otherwise, we just remove half of the escape chars.
		else:
			return escape_char * (len(match.group(0)) / 2)

	# The regex template for matching escape chars. Matches any zero or more
	# escape char couples that are followed by either End-Of-String, or and 
	# escaped separator.
	template = \
		Template("((?:(?:${escape_char}){2})*)(${escape_char}${separator}|$$)")
	r = _compile_re(template, separator, escape_char)
	return r.sub(subber, s)


def escaped_split(s, separator = "|", escape_char = "\\"):
	""" 
	Splits the string s at any occurence of separator that is not escaped 
	by the escape_char. The escape_char can be escaped as many times as 
	wanted.

	escape_char is not considered as such if it comes at the middle of the 
	string and its not followed by the separator.

	The escape_char is removed in every place that it was considered as escape.

	The function does not return empty list items.

	Examples:
		escaped_split("a|b") 		== ["a", "b"]
		escaped_split("a|b\|c") 	== ["a", "b|c"]
		escaped_split("a|b\\|c") 	== ["a", "b\", "c"]
		escaped_split("a|b\\\|c") 	== ["a", "b\|c"]
		escaped_split("a|b|c|") 	== ["a", "b", "c"]
		escaped_split("aaa\aa|bbbb) == ["aaa\aa", "bbbb"]
	"""
	template = Template("(?:${escape_char}.|[^${separator}])*")
	r = _compile_re(template, separator, escape_char)
	# Find all matching, i.e., split the string, and remove empty elements.
	l = filter(bool, r.findall(s))
	# Remove the escape char from every element.
	return map(lambda s: _remove_escaping(s, separator, escape_char), l)