#PA 4

import re

"Miscellaneous functions to practice Python"

class Failure(Exception):
    """Failure exception"""
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)

# Problem 1

# data type functions
# Return the element of the list l closest in value to v.  In the case of
# a tie, the first such element is returned.  If l is empty, None is returned.
def closest_to(l,v):
    if l == []:
        return None
    dist = max(l) - v
    result = 0
    for elem in l:
        if abs(elem - v) < dist:
            result = elem
            dist = abs(elem - v)
    return result

# Return a dictionary pairing corresponding keys to values.
def make_dict(keys,values):
    dictionary = {}
    for (k, v) in zip(keys, values):
        dictionary[k] = v
    return dictionary

# file IO functions
# Open the file fn and return a dictionary mapping words to the number
#    of times they occur in the file.  A word is defined as a sequence of
#    alphanumeric characters and _.  All spaces and punctuation are ignored.
#    Words are returned in lower case
def word_count(fn):
    dictionary = {}
    f = open(fn, 'r')
    lines = f.readlines()
    for line in lines:
        line = line.lower()
        line = line.replace('\t',' ')
        # line = re.sub(r'[^\w\s]','',line)
        for word in re.split('\W+', line):
            if word not in dictionary:
                dictionary[word] = 1
            else:
                dictionary[word] += 1
    return dictionary
