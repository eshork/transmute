#!/usr/bin/env python
"""Usage: transmute [opts] [inputFile]

Generates transmutations of input words according to selected options.

If inputFile is - or not provided, and -w is not provided, stdin is used.

 -h,--help        Display this help
 -w <word>        Supply a single <word> as input, via command line argument
 -t               Perform some typical transmutations (-l -p 3 -P 2 -c -n -s)
 -l               Create leet transmutations
 -L               Create common leet transmutations
 -p <X>           Append up to X places
 -P <X>           Prepend up to X places
 -i <X>           Insert up to X places, permutated through each inside position
 -I <X>           Insert up to X places, permutated through each position, including ends
 -n               Added characters include numbers
 -s               Added characters include symbols
 -a               Added characters include lower alpha
 -A               Added characters include upper alpha
 --list=<chars>   Provide a custom list of characters to use for additions
 -c               Capitalize letters
 -d               Include debug output (to stderr)

Order of operations (unused operations are skipped):
	- InsertEnds Loop
	- Insert Loop
	- Prepend Loop
	- Append Loop
	- Caps
	- Perform leet mixes
"""
import sys
import getopt
import fileinput
from pprint import pprint
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8') # vary depending on your lang/locale

def RemoveStrDupes(s):
	import string
	n = ''
	for i in s:
		if i not in n:
			n += i
	return n

def cChg_AddSet_AddLowerAlpha():
	global CONF_AddSet
	CONF_AddSet = CONF_AddSet + "abcdefghijklmnopqrstuvwxyz"
	pass
def cChg_AddSet_AddUpperAlpha():
	global CONF_AddSet
	CONF_AddSet = CONF_AddSet + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	pass
def cChg_AddSet_AddNumbers():
	global CONF_AddSet
	CONF_AddSet = CONF_AddSet + "0123456789"
	pass
def cChg_AddSet_AddSymbols():
	global CONF_AddSet
	CONF_AddSet = CONF_AddSet + "!@#$%^&*()-+=_`~[]{}\\|;:'\",./<>?"
	pass

def main():
	global CONF_Debug
	global CONF_infile
	global CONF_commonleet
	global CONF_leet
	global CONF_capitalize
	global CONF_NumAppend
	global CONF_NumPrepend
	global CONF_NumInsert
	global CONF_NumEdgeInsert
	global CONF_AddSet
	CONF_Debug = False
	CONF_infile = "-"
	CONF_leet = False
	CONF_commonleet = False
	CONF_capitalize = False
	CONF_NumAppend = 0
	CONF_NumPrepend = 0
	CONF_NumInsert = 0
	CONF_NumEdgeInsert = 0
	CONF_AddSet = ""
	CONF_singleWord = None

	# parse command line options
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hdtlLcw:p:P:i:I:nsaA", ["help","list="])
		# pprint(opts)
		# pprint(args)
	except getopt.error, msg:
		print msg
		print "for help use --help"
		sys.exit(2)
	# process options
	for o, a in opts:
		if o in ("-h", "--help"):
			print __doc__
			sys.exit(0)
		if o in ("-d"):
			CONF_Debug = True
		if o in ("-t"):
			CONF_leet = True
			CONF_capitalize = True
			CONF_NumAppend = 3
			CONF_NumPrepend = 2
			cChg_AddSet_AddNumbers()
			cChg_AddSet_AddSymbols()
		if o in ("-l"):
			CONF_leet = True
		if o in ("-L"):
			CONF_commonleet = True
		if o in ("-p"):
			CONF_NumAppend = int(a)
		if o in ("-P"):
			CONF_NumPrepend = int(a)
		if o in ("-i"):
			CONF_NumInsert = int(a)
		if o in ("-I"):
			CONF_NumEdgeInsert = int(a)
		if o in ("-a"):
			cChg_AddSet_AddLowerAlpha()
		if o in ("-A"):
			cChg_AddSet_AddUpperAlpha()
		if o in ("-n"):
			cChg_AddSet_AddNumbers()
		if o in ("-s"):
			cChg_AddSet_AddSymbols()
		if o in ("--list"):
			CONF_AddSet = CONF_AddSet + str(a)
		if o in ("-c"):
			CONF_capitalize = True
		if o in ("-w"):
			CONF_singleWord = str(a)

	# process arguments
	if len(args) > 1:
		print __doc__
		sys.exit(0)
	elif len(args) == 1:
		CONF_infile = args[0]

	# sort the AddSet
	CONF_AddSet = ( ''.join(sorted(CONF_AddSet)) )
	# remove duplicates from AddSet
	CONF_AddSet = RemoveStrDupes(CONF_AddSet)


	# debug output
	if(CONF_Debug):
		sys.stderr.write("CONF_Debug = " + str(CONF_Debug) + "\n")
		sys.stderr.write("CONF_infile = " + CONF_infile + "\n")
		sys.stderr.write("CONF_singleWord = " + CONF_singleWord + "\n")
		sys.stderr.write("CONF_leet = " + str(CONF_leet) + "\n")
		sys.stderr.write("CONF_commonleet = " + str(CONF_commonleet) + "\n")
		sys.stderr.write("CONF_capitalize = " + str(CONF_capitalize) + "\n")
		sys.stderr.write("CONF_NumAppend = " + str(CONF_NumAppend) + "\n")
		sys.stderr.write("CONF_NumPrepend = " + str(CONF_NumPrepend) + "\n")
		sys.stderr.write("CONF_NumInsert = " + str(CONF_NumInsert) + "\n")
		sys.stderr.write("CONF_NumEdgeInsert = " + str(CONF_NumEdgeInsert) + "\n")
		sys.stderr.write("CONF_AddSet = [" + str(CONF_AddSet) + "]" + "\n")


	if CONF_singleWord != None:
		GoTransmute(CONF_singleWord)
		return

	if CONF_infile == '-':
		FILE = sys.stdin
	else:
		FILE = open(CONF_infile, 'r')

	for LINE in FILE:
		l = LINE.strip()
		GoTransmute(l)


def GoTransmute(origLine):
	global CONF_AddSet
	global CONF_Debug
	if(CONF_Debug):
		sys.stderr.write("...GoTransmute\n")
	if(len(origLine)>0):
		if(len(CONF_AddSet)>0):
			GoTransmuteEdgeInsert(origLine)
		else:
			GoTransmuteCaps(origLine)
def GoTransmuteEdgeInsert(origLine):
	global CONF_NumEdgeInsert
	global CONF_Debug
	if(CONF_Debug):
		sys.stderr.write("...GoTransmuteEdgeInsert\n")
	if(CONF_NumEdgeInsert>0):
		TransmuteEdgeInsert(origLine, GoTransmuteInsert)
	else:
		GoTransmuteInsert(origLine)
def GoTransmuteInsert(origLine):
	global CONF_NumInsert
	global CONF_Debug
	if(CONF_Debug):
		sys.stderr.write("...GoTransmuteInsert\n")
	if(CONF_NumInsert>0):
		TransmuteInsert(origLine, GoTransmutePrepend)
	else:
		GoTransmutePrepend(origLine)
def GoTransmutePrepend(origLine):
	global CONF_NumPrepend
	global CONF_Debug
	if(CONF_Debug):
		sys.stderr.write("...GoTransmutePrepend\n")
	if(CONF_NumPrepend>0):
		TransmutePrepend(origLine, GoTransmuteAppend)
	else:
		GoTransmuteAppend(origLine)
def GoTransmuteAppend(origLine):
	global CONF_NumAppend
	global CONF_Debug
	if(CONF_Debug):
		sys.stderr.write("...GoTransmuteAppend\n")
	if(CONF_NumAppend>0):
		TransmuteAppend(origLine, GoTransmuteCaps)
	else:
		GoTransmuteCaps(origLine)
def GoTransmuteCaps(origLine):
	global CONF_capitalize
	global CONF_Debug
	if(CONF_Debug):
		sys.stderr.write("...GoTransmuteCaps\n")
	if(True == CONF_capitalize):
		TransmuteCaps(origLine, GoTransmuteCommonLeet) # change to common leet transmute
	else:
		GoTransmuteCommonLeet(origLine)

def GoTransmuteCommonLeet(origLine):
	global CONF_commonleet
	global CONF_Debug
	if(CONF_Debug):
		sys.stderr.write("...GoTransmuteCommonLeet\n")
	if(True == CONF_commonleet):
		TransmuteCommonLeet(origLine, GoTransmuteLeet) # change to leet transmute
	else:
		GoTransmuteLeet(origLine)
def GoTransmuteLeet(origLine):
	global CONF_leet
	global CONF_Debug
	if(CONF_Debug):
		sys.stderr.write("...GoTransmuteLeet\n")
	if(True == CONF_leet):
		TransmuteLeet(origLine, Print) # change to leet transmute
	else:
		Print(origLine)


def Print(output):
	print output

def TransmutePrepend(baseWord, nextFunc):
	global CONF_AddSet
	global CONF_NumPrepend
	prepend_Str = ""
	while(len(prepend_Str) <= CONF_NumPrepend):
		newline = prepend_Str + baseWord
		prepend_Str = getNextIncrement(prepend_Str, CONF_AddSet)
		nextFunc(newline)
def TransmuteAppend(baseWord, nextFunc):
	global CONF_AddSet
	global CONF_NumAppend
	append_Str = ""
	while(len(append_Str) <= CONF_NumAppend):
		newline = baseWord + append_Str
		append_Str = getNextIncrement(append_Str, CONF_AddSet)
		nextFunc(newline)
def TransmuteInsert(baseWord, nextFunc):
	global CONF_AddSet
	global CONF_NumInsert
	insert_Str = ""
	nextFunc(baseWord)
	insert_Str = getNextIncrement(insert_Str, CONF_AddSet)
	while(len(insert_Str) <= CONF_NumInsert):
		pos = 1
		while(pos < len(baseWord)):
			f,b = baseWord[:pos],baseWord[pos:]
			nextFunc(f+insert_Str+b)
			pos += 1
		insert_Str = getNextIncrement(insert_Str, CONF_AddSet)
def TransmuteEdgeInsert(baseWord, nextFunc):
	global CONF_AddSet
	global CONF_NumEdgeInsert
	insert_Str = ""
	nextFunc(baseWord)
	insert_Str = getNextIncrement(insert_Str, CONF_AddSet)
	while(len(insert_Str) <= CONF_NumEdgeInsert):
		pos = 0
		while(pos <= len(baseWord)):
			f,b = baseWord[:pos],baseWord[pos:]
			nextFunc(f+insert_Str+b)
			pos += 1
		insert_Str = getNextIncrement(insert_Str, CONF_AddSet)

def TransmuteCaps(baseWord, nextFunc):
	nextFunc(baseWord) # first passed call is clean

	matrix = buildCapitalizationSubstitutesMatrix(baseWord)
	curVal = []
	for c in baseWord:
		curVal += [c]
	curVal = getNextSubstitute(curVal, matrix)
	
	while( len(curVal)>0 ):
		nextFunc("".join(curVal))
		curVal = getNextSubstitute(curVal, matrix)

def TransmuteLeet(baseWord, nextFunc):
	nextFunc(baseWord) # first passed call is clean

	matrix = buildLeetSubstitutesMatrix(baseWord)
	curVal = []
	for c in baseWord:
		curVal += [c]
	curVal = getNextSubstitute(curVal, matrix)
	
	while( len(curVal)>0 ):
		nextFunc("".join(curVal))
		curVal = getNextSubstitute(curVal, matrix)

def TransmuteCommonLeet(baseWord, nextFunc):
	nextFunc(baseWord) # first passed call is clean

	matrix = buildCommonLeetSubstitutesMatrix(baseWord)
	curVal = []
	for c in baseWord:
		curVal += [c]
	curVal = getNextSubstitute(curVal, matrix)
	
	while( len(curVal)>0 ):
		nextFunc("".join(curVal))
		curVal = getNextSubstitute(curVal, matrix)

def buildCommonLeetSubstitutesMatrix(origLine):
	out = []
	capMap = {
		"i" : ["i","!","1"],
		"l" : ["l", "1"],
		"e" : ["e", "3"],
		"t" : ["t", "7"],
		"a" : ["a", "4", "@"],
		"s" : ["s", "5", "$"],
		"o" : ["o", "0"],
		"b" : ["b", "8"],
	}
	for c in origLine:
		if capMap.has_key(c):
			out += [capMap[c]]
		else:
			out += [c]
	return out
	pass
	
	
def buildLeetSubstitutesMatrix(origLine):
	out = []
	capMap = {
		"i" : ["i","!","|",";"],
		"l" : ["l", "1","|","!", "|_"],
		"e" : ["e", "3"],
		"t" : ["t", "7"],
		"a" : ["a", "4", "@"],
		"s" : ["s", "5", "$"],
		"h" : ["h", "#", "|-|"],
		"o" : ["o", "0", "*", "()", "[]", "{}"],
		"b" : ["b", "8"],
		"v" : ["v", "\/"],
		"n" : ["n", "|\|", "|/|"],
		"d" : ["d", "|)", "|]"],
	}
	for c in origLine:
		if capMap.has_key(c):
			out += [capMap[c]]
		else:
			out += [c]
	return out
	pass

def buildCapitalizationSubstitutesMatrix(origLine):
	out = []
	capMap = {}
	for c in "abcdefghijklmnopqrstuvwxyz":
		capMap[c] = [c, c.upper()]
	for c in origLine:
		if capMap.has_key(c):
			out += [capMap[c]]
		else:
			out += [c]
	return out
	pass

def getNextSubstitute(curVal, valMatrix, curIndex = 0):
	if( curIndex >= len(curVal) ):
		return "" # out of bounds returns empty string
	# find matrixIndex at curIndex 
	matrixIndex = valMatrix[curIndex].index(curVal[curIndex])
	next = matrixIndex + 1
	if( next >= len(valMatrix[curIndex]) ):
		# need to roll to next significant place
		return getNextSubstitute( curVal[:curIndex] + [ valMatrix[curIndex][0] ] + curVal[curIndex+1:], valMatrix, curIndex+1)
	else:
		# increment this place only
		return curVal[:curIndex] + [ valMatrix[curIndex][next] ] + curVal[curIndex+1:]


def getNextIncrement(curVal, AddSet):
	if curVal == "":
		return AddSet[0]
	#pop last char
	f, b = curVal[:-1],curVal[-1]
	#find position in AddSet
	pos = AddSet.find(b)

	#if last position, recurse and start over
	if len(AddSet)-1 == pos:
		f = getNextIncrement(f,AddSet)
		b = AddSet[0]
		pass
	else:
		#otherwise, just increment 
		b = AddSet[pos+1]
	# and stuff it back onto the end
	return f+b
	pass

if __name__ == "__main__":
	main()
