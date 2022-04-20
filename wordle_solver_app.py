# -*- coding: utf-8 -*-
from wordle_word_generator import WordGenerator, WordWithScores
import logging
import os


def read_corpus_file(filepath: str, negative_list_filepath: str = None) -> [WordWithScores]:
    if negative_list_filepath is not None and \
            not os.path.exists(negative_list_filepath) or not os.path.isfile(negative_list_filepath):
        ValueError(f"can't open {negative_list_filepath}")

    negative_list = []
    if negative_list_filepath is not None:
        with open(filepath, "r", encoding="UTF-8") as file:
            for line in file:
                negative_list.append(line.strip().lower())

    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        ValueError(f"can't open {filepath}")
    word_list = []
    with open(filepath, "r", encoding="UTF-8") as file:
        for line in file:
            line_split = line.split("\t")
            if len(line_split) != 2:
                continue
            word_str = line_split[0].strip().lower()
            if word_str in negative_list:
                continue
            score = float(line_split[1])
            word_list.append(WordWithScores(word_str, score))
    return word_list


if __name__ == "__main__":
    word_list = read_corpus_file("wordl_corpus.txt", negative_list_filepath="negative_list.txt")
    generator = WordGenerator(words=word_list)
    word_count_last = len(generator.words)
    new_word = generator.next_word()
    logging.info(f"next word: {new_word}), possibilities: "
                 f"{word_count_last}")
    while True:
        user_input = None
        while user_input is None or len(str(user_input)) != 5:
            print("enter mask")
            user_input = input()
            if str(user_input) == "!":
                new_word = generator.next_word()
                logging.info(f"next word: {new_word}), possibilities: {word_count_last}")

        word_hint = new_word.word
        word_mask = str(user_input).lower()
        generator.add_hint(word_hint, word_mask)
        new_word = generator.next_word()
        reduction = float(word_count_last - len(generator.words))
        percent = round(reduction / float(word_count_last) * 100.0, 1)
        word_count_last = len(generator.words)
        logging.info(f"next word: {new_word}), possibilities: {word_count_last}"
                     f" reduction: {reduction} ({percent}%)")
        if word_count_last <= 20:
            logging.info([(w.word, w.scores) for w in generator.words])
