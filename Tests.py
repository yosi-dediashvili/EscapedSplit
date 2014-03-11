from EscapedSplit import escaped_split

TESTS = {
	r"a|b" 			: ["a", "b"],
	r"a|b^|c" 		: ["a", "b|c"],
	r"a|b^^|c"		: ["a", "b^", "c"],
	r"a|b^^^^|c"	: ["a", "b^^", "c"],
	r"a|b^^^^^|c"	: ["a", "b^^|c"],
	r"a|b|c|"		: ["a", "b", "c"]
}

for s, l in TESTS.iteritems():
	print "Testing: \"%s\", Expecting: %s" % (s, l)
	result_l = escaped_split(s, '|', '^')
	#result_l = remove_escape(result_l)
	print "Got: %s" % result_l
	if (result_l != l):
		print "Failed!"
	else:
		print "Succeeded!"
