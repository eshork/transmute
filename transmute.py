#!/usr/bin/env python
"""transmute [opts] [inputFile]

Generates transmutations of input words according to selected options.

If inputFile is - or not provided, stdin is used.

 -h,--help        Display this help
 -t               Perform some typical transmutations (-l -p 3 -P 2 -c -n -s)
 -l               Create leet transmutations
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
	global CONF_infile
	global CONF_leet
	global CONF_capitalize
	global CONF_NumAppend
	global CONF_NumPrepend
	global CONF_NumInsert
	global CONF_NumEdgeInsert
	global CONF_AddSet
	CONF_infile = "-"
	CONF_leet = False
	CONF_capitalize = False
	CONF_NumAppend = 0
	CONF_NumPrepend = 0
	CONF_NumInsert = 0
	CONF_NumEdgeInsert = 0
	CONF_AddSet = ""

	# parse command line options
	try:
		opts, args = getopt.getopt(sys.argv[1:], "htlcp:P:i:I:nsaA", ["help","list="])
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
		if o in ("-t"):
			CONF_leet = True
			CONF_capitalize = True
			CONF_NumAppend = 3
			CONF_NumPrepend = 2
			cChg_AddSet_AddNumbers()
			cChg_AddSet_AddSymbols()
		if o in ("-l"):
			CONF_leet = True
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



	print ("CONF_infile = " + CONF_infile)
	print ("CONF_leet = " + str(CONF_leet))
	print ("CONF_capitalize = " + str(CONF_capitalize))
	print ("CONF_NumAppend = " + str(CONF_NumAppend))
	print ("CONF_NumPrepend = " + str(CONF_NumPrepend))
	print ("CONF_NumInsert = " + str(CONF_NumInsert))
	print ("CONF_NumEdgeInsert = " + str(CONF_NumEdgeInsert))
	print ("CONF_AddSet = [" + str(CONF_AddSet) + "]")



	if CONF_infile == '-':
		FILE = sys.stdin
	else:
		FILE = open(CONF_infile, 'r')

	for LINE in FILE:
		l = LINE.strip()
		GoTransmute(l)


def GoTransmute(origLine):
	global CONF_AddSet
	if(len(origLine)>0):
		if(len(CONF_AddSet)>0):
			GoTransmuteEdgeInsert(origLine)
		else:
			Print(origLine)
def GoTransmuteEdgeInsert(origLine):
	global CONF_NumEdgeInsert
	if(CONF_NumEdgeInsert>0):
		TransmuteEdgeInsert(origLine, GoTransmuteInsert)
	else:
		GoTransmuteInsert(origLine)
def GoTransmuteInsert(origLine):
	global CONF_NumInsert
	if(CONF_NumInsert>0):
		TransmuteInsert(origLine, GoTransmutePrepend)
	else:
		GoTransmutePrepend(origLine)
def GoTransmutePrepend(origLine):
	global CONF_NumPrepend
	if(CONF_NumPrepend>0):
		TransmutePrepend(origLine, GoTransmuteAppend)
	else:
		GoTransmuteAppend(origLine)
def GoTransmuteAppend(origLine):
	global CONF_NumAppend
	if(CONF_NumAppend>0):
		TransmuteAppend(origLine, GoTransmuteCaps)
	else:
		GoTransmuteCaps(origLine)
def GoTransmuteCaps(origLine):
	global CONF_capitalize
	if(True == CONF_capitalize):
		GoTransmuteLeet(origLine) # change to capitalization transmute
	else:
		GoTransmuteLeet(origLine)
def GoTransmuteLeet(origLine):
	global CONF_leet
	if(True == CONF_leet):
		Print(origLine) # change to leet transmute
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

# use a 2D array...

#original becomes ["o","r","i","g","i","n","a","l"]
#then ["o","r","i","g","i","n","a","l"] becomes...
# ["o","r","i","g","i","n","a","l"]
# ["0",   ,"1",   ,"1","|\|","a","1"]
# [   ,   ,"!",   ,"!",   ,   ,"!"]
# and then we just iterate through all the posibilities with a recursive function (and we can reuse this for the capitalizations as well)


# i ! | ;
# l 1 | ! |_
# e 3
# t 7
# a 4
# s $
# h #
# o 0 () [] {} *
# v \/
# n |\| |/|
# D |) |]
# b 8
# h |-|

def getNextSubstitute(curVal, valMatrix, curIndex):
	pass


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
