import re
from collections import Counter

def load_word_list(file_path):
    with open(file_path, 'r') as file:
        words = re.findall(r'\b\w+\b', file.read().lower())
        return Counter(words)

def P(word, WORDS):
    return WORDS[word] / sum(WORDS.values()) if word in WORDS else 0

def correct_word(word, WORDS):
    return max(candidates(word, WORDS), key=lambda w: P(w, WORDS))

def candidates(word, WORDS):
    return (known([word], WORDS) or known(edits1(word), WORDS) or known(edits2(word), WORDS) or [word])

def known(words, WORDS):
    return set(w for w in words if w in WORDS)

def edits1(word):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in alphabet]
    inserts = [L + c + R for L, R in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
