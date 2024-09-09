"""
Script to generate a new class for similar words.

This script receives a text file with a list of words and generates a new
class for similar words. The script uses the WordNet corpus to find the
synonyms of the words and then generates a new class for the words that
have similar synonyms.

Example:
    python similar.py words.txt
"""

import argparse

from nltk.corpus import wordnet


def create_parser() -> argparse.ArgumentParser:
    """
    Create a parser for the command line arguments.

    :return parser: The parser object.
    """
    parser = argparse.ArgumentParser(
        description="Generate a new dataset with similar words."
    )
    parser.add_argument(
        "text_path",
        type=str,
        help="The path to the text file with the words.",
    )
    return parser


def get_synonyms(word: str) -> set:
    """
    Get the synonyms for a word

    :param word: The word
    :return synonyms: The set of synonyms
    """
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms


def find_similar_words(word_list: list) -> dict:
    """
    Find similar words for a list of words

    :param word_list: The list of words
    :return similar_words: A dictionary with the similar words
    """
    similar_words = {}
    for word in word_list:
        similar_words[word] = get_synonyms(word)
    return similar_words


def get_words_list(text_path: str) -> list:
    """
    Get the list of words from the text file

    :param text_path: The path to the text file with the words
    :return words: The list of words
    """
    with open(text_path, "r") as f:
        text_file = f.readlines()

    words = []
    for word in text_file:
        words_in_line = word.split("/")
        for word_aux in words_in_line:
            word_aux = word_aux.replace(" ", "_")
            word_aux = word_aux.replace("\n", "").strip()
            words.append(word_aux)
    return words


def get_new_classifications(words: str, similar_words: dict) -> dict:
    """
    Get the new classification for the words

    :param words: The list of words
    :param similar_words: The dictionary with the similar words
    :return new_words: A dictionary with the new words
    """
    new_words = {}
    for word in words:
        found = False
        for similar_word in similar_words[word]:
            if similar_word in new_words:
                new_words[word] = similar_word
                found = True
                break
        if not found:
            new_words[word] = word
    return new_words


def get_new_classes(text_path: str) -> dict:
    """
    Transform similar words into a unique class

    :param text_path: The path to the text file with the words
    :return new_classes: A dictionary with the new classes
    """
    words = get_words_list(text_path)
    similar_words = find_similar_words(words)
    new_words = get_new_classifications(words, similar_words)
    return new_words


def main():
    parser = create_parser()
    text_path = parser.text_path
    new_words = get_new_classes(text_path)
    print(new_words)


if __name__ == "__main__":
    main()
