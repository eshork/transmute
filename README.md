# transmute.py

A command-line program to generate transmutations of input words, for the purpose of adding controlled complexity to password cracking dictionaries.

Sometimes your password cracking dictionary lacks originality. Your word list may contain every word in the english language, but what if your target was clever enough to append a symbol or number to the end of a common word? Or worse, they replaced a letter with a symbol! Your dictionary doesn't contain that variant, and thus it will never find the user's password.

Enter transmute. With this tool, you can add salt to password dictionaries in a controlled manner. 

## getting started

Help is embedded. All you need to do is simply run transmute with the -h argument for the full list.

Under most Unix-like environments, you can either:

	python transmute.py -h

OR

	chmod +x transmute.py
	./transmute.py -h

The choice is yours.

*Transmute was originally developed using Python 2.7.5, running on Mac OSX 10.9.3 Mavericks. I blame any and all weirdness on the idiosyncrasies of that platform.*


## examples

Transmute a single word "hello" into all possible capitalization combinations

	./transmute.py -c -w hello

Transmute a single word "hello" into all possible leet combinations

	./transmute.py -l -w hello

Transmute a single word "hello" into all possible combined capitalization and leet combinations

	./transmute.py -cl -w hello

Transmute an entire dictionary list of words into all possible combined capitalization and leet combinations

	cat your_dictionary | ./transmute.py -cl
