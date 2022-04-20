# -*- coding: utf-8 -*-
import random
from wordle_word_list_generator import calc_char_counts


class CharWithProperties:
    def __init__(self, c: str, excluded: bool, not_positions: [int],
                 positions: [int]):
        if len(c) != 1:
            raise ValueError("need single char")
        self.char = c
        self.excluded = excluded
        self.not_positions = not_positions
        self.positions = positions


class Word:
    def __init__(self, word: str):
        self.word = word
        if len(self.word) == 0:
            raise ValueError("word has no chars")
        self.char_counts = calc_char_counts(word)
        self.max_duplicated = max(self.char_counts.values())

    def validate_hint(self, hint: CharWithProperties):
        if hint.excluded:
            if hint.char in self.word:
                return False
        else:
            for pos in hint.positions:
                if self.word[pos] != hint.char:
                    return False
            for not_pos in hint.not_positions:
                if self.word[not_pos] == hint.char:
                    return False
            if hint.char not in self.word:
                return False
        return True

    def __str__(self):
        return self.word


class WordWithScores(Word):
    def __init__(self, word: str, char_prob_score: float):
        super().__init__(word)
        self.scores = [1, char_prob_score]

    def __str__(self):
        return f"{self.word} ({str(self.scores)})"


def word_distance(word1: Word, word2: Word) -> float:
    dist = 0
    for i, c in enumerate(word1.word):
        if c != word2.word[i]:
            dist += 1
    for c in word1.char_counts:
        if c not in word2.char_counts:
            dist += 1
        else:
            dist += abs(word1.char_counts[c] - word2.char_counts[c])
    return dist


class WordGenerator:
    def __init__(self, words: [WordWithScores]):
        self.words = words
        self.words.sort(key=lambda w: w.scores[1], reverse=True)
        self.hints: [CharWithProperties] = []
        self.counter = 0
        self.last_hint = None

    def resort_word_list(self):
        if self.counter < 3:

            for word in self.words:
                word.scores[0] += word_distance(word, Word(self.last_hint))
        else:
            for word in self.words:
                word.scores[0] = 1
        self.words.sort(key=lambda w: w.scores, reverse=True)

    def add_hint(self, word: str, mask: str):
        self.last_hint = word
        self.resort_word_list()
        for i, (c, m) in enumerate(zip(word, mask)):
            have_char = False
            for h in self.hints:
                if h.char == c:
                    if int(m) == 1 or int(m) == 0:
                        if i not in h.not_positions:
                            h.not_positions.append(i)
                        have_char = True
                        break
                    elif int(m) == 2:
                        h.excluded = False
                        if i not in h.positions:
                            h.positions.append(i)
                        have_char = True
                        break
                    else:
                        raise ValueError(f"Invalid mask value {int(m)}")
            if not have_char:
                excluded = False
                positions = []
                not_positions = []
                if int(m) == 0:
                    excluded = True
                elif int(m) == 1:
                    not_positions.append(i)
                elif int(m) == 2:
                    positions.append(i)
                else:
                    raise ValueError(f"Invalid mask value {int(m)}")
                self.hints.append(CharWithProperties(c=c, excluded=excluded, not_positions=not_positions,
                                                     positions=positions))

    def get_words(self) -> [WordWithScores]:
        lst = []
        for word_obj in self.words:
            valid = True
            for hint in self.hints:
                if not word_obj.validate_hint(hint):
                    valid = False
                    break
            if not valid:
                continue
            lst.append(word_obj)
        if len(lst) == 0:
            raise ValueError("no words")
        return lst

    def next_word(self) -> WordWithScores:
        lst = self.get_words()
        word = None
        for w in lst:
            word = w
            if word.max_duplicated <= max(self.counter, 1):
                if (self.counter == 0 and random.random() < 0.05) or self.counter > 0:
                    break
        self.counter += 1
        lst.remove(word)
        self.words = lst
        return word

    def remove_word(self, word: WordWithScores):
        self.words.remove(word)

    def save_words(self, filepath: str):
        with open(filepath, encoding="UTF-8", mode="w") as file:
            for w in self.words:
                file.write(f"{w.word}\t{w.prob_score}\n")
