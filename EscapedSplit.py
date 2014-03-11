def _count_rstripped(s, escape_char):
	"""
		Counts how many escape_chars was stripped from the end of the string s.
	"""
	before = len(s)
	after = len(s.rstrip(escape_char))
	return before - after

def _rstrip_escape(s, escape_char):
	"""
		Removes the escape_char occurences from the end of the string s. Such 
		that the escaped char will be kept. The function returns a tuple of the 
		number of occurences of the escape_char and the stripped string:

		_remove_escape("test$$", "$") == (2, "test$")
		_remove_escape("test^^^^^) == (5, "test^^^")
	"""
	# First, count occurences of escape_char at the end of s.
	num_stripped = _count_rstripped(s, escape_char)
	even_or_none = not (num_stripped % 2)
	# Take the substring first (without the escape at the end)
	correct_form = s[0:len(s) - num_stripped]
	# Repeat escape_char as many times as needed (i.e., (n / 2) + (n % 2))
	correct_form += (escape_char * (num_stripped / 2))
	if not even_or_none:
		correct_form += escape_char
	return num_stripped, correct_form


def escaped_split(s, separator = "|", escape_char = "\\"):
	"""
		Splits the string s at any occurence of separator that is not escaped 
		by the escape_char. The escape_char can be escaped as many times as 
		wanted.

		The function does not return empty list items.

		Examples:
			escaped_split("a|b") == ["a", "b"]
			escaped_split("a|b\|c") == ["a", "b|c"]
			escaped_split("a|b\\|c") == ["a", "b\", "c"]
			escaped_split("a|b\\\|c") == ["a", "b\|c"]
			escaped_split("a|b|c|") == ["a", "b", "c"]
	"""
	init_list = s.split(separator)
	# Array with the same length for start.
	final_list = [''] * len(init_list)
	init_i = final_i = 0
	
	while init_i < len(init_list):
		# Strip first.
		num_stripped, correct_form = \
			_rstrip_escape(init_list[init_i], escape_char)

		# If the separator was escaped (odd number of escape char casts to 
		# true):
		if num_stripped % 2:
			# In case of odd number, on escape_char is escaping the separator,
			# so we need to remove it from the final string.
			correct_form = correct_form[0:-1]

			final_list[final_i] += correct_form
			# If that's not the last element, add the separator char too. Notice
			# that because of the implementation of split(), when the last char
			# in the string s is the separator, we'll get an additional empty 
			# element in the init_list.
			if init_i < len(init_list): 
				final_list[final_i] += separator
		else:
			final_list[final_i] += correct_form
			# We increase the new_i only when the seperator was escaped...
			final_i += 1
		# In any case, increase the init_i index.
		init_i += 1

	# Return the new list, but remove the empty elements.
	return filter(bool, final_list)