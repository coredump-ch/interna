# -*- coding: utf-8 -*-


import os.path
import random


def generate_access_code(num_words=3):
    """
    Generate an XKCD style access code.
    """
    wordlist = 'wordlist_de.txt'
    thisdir = os.path.dirname(__file__)
    with open(os.path.join(thisdir, wordlist), 'r') as f:
        words = f.readlines()
    chosen = [random.choice(words).strip() for _ in range(num_words)]
    return ' '.join(chosen)
