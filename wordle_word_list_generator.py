# -*- coding: utf-8 -*-
import os.path
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)


def calc_score(char_counts: dict, relative_frequency: dict):
    score = 0.0
    decrease = 1.0
    for c, count in char_counts.items():
        score += relative_frequency[c] * count
        if count > 1:
            decrease *= 0.8
    return score * decrease


def calc_char_counts(word: str):
    count_dict = {}
    for c in word:
        if c in count_dict:
            count_dict[c] += 1
        else:
            count_dict[c] = 1
    return {k: v for k, v in reversed(sorted(count_dict.items(), key=lambda item: item[1]))}


class WordStatistics:
    def __init__(self):
        self.char_counts = {}

    def add_to_statistics(self, word):
        counts = {}
        for c in word:
            if c not in counts:
                counts[c] = 1
            else:
                counts[c] += 1

        for c in counts:
            if c not in self.char_counts:
                self.char_counts[c] = counts[c]
            else:
                self.char_counts[c] += counts[c]
        return True

    def save(self, filepath: str):
        with open(filepath, encoding="UTF-8", mode="w") as file:
            for c in self.char_counts:
                file.write(f"{c}: {self.char_counts[c]}\n")

    def load(self, filepath: str):
        with open(filepath, encoding="UTF-8", mode="r") as file:
            self.char_counts = {}
            for line in file:
                split_line = line.split(": ")
                self.char_counts[split_line[0]] = int(split_line[1])

    def total_count(self):
        return np.sum([count for count in self.char_counts.values()])

    def relative_frequency(self):
        total_count = self.total_count()
        freq_dict = {item[0]: item[1] / total_count for item in self.char_counts.items()}
        return {k: v for k, v in reversed(sorted(freq_dict.items(), key=lambda item: item[1]))}


class WordListGenerator:
    def __init__(self):
        self.word_length = 5
        self.VALIDCHARS = "abcdefghijklmnopqrstuvwxyzüöä"
        self.word_list = []

    def validate_word(self, word: str) -> bool:
        if len(word) != self.word_length:
            return False
        for c in word:
            if c not in self.VALIDCHARS:
                logging.info(f"invalid char {c} in word {word}")
                return False
        return True

    def export_words(self, filepath: str = "wordl_corpus.txt"):
        if len(self.word_list) == 0:
            return
        stats = WordStatistics()
        for word in self.word_list:
            stats.add_to_statistics(word)

        frequency_dict = stats.relative_frequency()
        with open(filepath, "w", encoding="UTF-8") as file:
            for word in self.word_list:
                score = calc_score(calc_char_counts(word), frequency_dict)
                file.write(f"{word}\t{score}\n")

    def import_words(self, raw_wordlist_filepath: str, negativelist_filepath: str = ""):
        if not os.path.exists(raw_wordlist_filepath):
            raise ValueError(f"{raw_wordlist_filepath} does not exist")

        negative_lst = []
        if len(negativelist_filepath) > 0:
            if not os.path.exists(negativelist_filepath):
                raise ValueError(f"{raw_wordlist_filepath} does not exist")
            with open(negativelist_filepath, encoding="UTF-8", mode="r") as file:
                for line in file:
                    negative_lst.append(line.lower().strip())

        filtered_words = []
        with open(raw_wordlist_filepath, encoding="UTF-8", mode="r") as file:
            for line in file:
                line_split = line.split("\t")
                if len(line_split) != 3:
                    # logging.info(f"{line} has unexpected length after split")
                    continue
                word = line_split[1].lower()
                if word in negative_lst:
                    continue
                if word in filtered_words:
                    continue
                if not self.validate_word(word):
                    continue
                filtered_words.append(word)

        self.word_list = filtered_words


if __name__ == "__main__":
    corpus_file = r"deu_mixed-typical_2011_1M-words.txt"
    negative_file = "negative_list.txt"
    wlg = WordListGenerator()
    wlg.import_words(corpus_file, negative_file)
    wlg.export_words()
