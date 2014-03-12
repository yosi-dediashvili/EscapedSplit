from EscapedSplit import escaped_split

TESTS = {
	r"a|b" 			: ["a", "b"],
	r"a|b^|c" 		: ["a", "b|c"],
	r"a|b^^|c"		: ["a", "b^", "c"],
	r"a|b^^^^|c"	: ["a", "b^^", "c"],
	r"a|b^^^^^|c"	: ["a", "b^^|c"],
	r"a|b|c|"		: ["a", "b", "c"],
	r"some^long|list|with^^^^^escaping^|of|the^|sep^|arator" : ["some^long", "list", "with^^^^^escaping|of", "the|sep|arator"],
	r""				: [],
	r"^||"			: ["|"]
}

for s, l in TESTS.iteritems():
	print "Testing: \"%s\", Expecting: %s" % (s, l)
	result_l = escaped_split(s, '|', '^')
	print "Got: %s" % result_l
	if (result_l != l):
		print "Failed!"
	else:
		print "Succeeded!"
	print "-----------------------------------------------------"
