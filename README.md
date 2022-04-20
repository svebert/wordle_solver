# wordle_solver
simple program to solve wordle game

wordle_word_list_generator.py will generate a new file named "wordl_corpus.txt" which contains a filtered list of the 1 million german mixed-typical word corpus from the university of Leipzig (https://wortschatz.uni-leipzig.de/de/download/German). All filtered words get a score. The score is based on the frequency of characters in the german alphabet (including umlauts)

wordle_solver_app.py

generates a new word candidate. Enter the feedback from wordle as "mask" in the next step. Enter a 5 digit number. A 0-digit means, that the character at this position is not occur in the solution word. A 1-digit means, that the character occurs in the solution word but at a different position. A 2-digit means, that the character occurs in the solution word at the given position. This mask relates to the last given word candidate.
To skip entering the mask and receive the next candidate, enter !.

The word corpus is very weak and contains many useless/wrong words. Add these words to the negative_list.txt. When you restart wordle_solver_app.py the words in the negative_list.txt will be ignored.
