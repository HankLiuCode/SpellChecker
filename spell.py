import re
from collections import Counter
import timeit

#from functools import filter

def words(text): 
    return re.findall(r'\w+', text.lower())

word_count = Counter(words(open('big.txt').read()))
N = sum(word_count.values())
letters    = 'abcdefghijklmnopqrstuvwxyz'

def P(word): 
    return word_count[word] / N # float

def edits1(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def correction(word): 
    return max(candidates(word), key=P)

def candidates(word): 
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    return set(w for w in words if w in word_count)

def edits2(word): 
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def unit_tests():
    # test correction
    assert correction('speling') == 'spelling'              # insert
    assert correction('korrectud') == 'corrected'           # replace 2
    assert correction('bycycle') == 'bicycle'               # replace
    assert correction('inconvient') == 'inconvenient'       # insert 2
    assert correction('arrainged') == 'arranged'            # delete
    assert correction('peotry') =='poetry'                  # transpose
    assert correction('peotryy') =='poetry'                 # transpose + delete
    assert correction('word') == 'word'                     # known
    assert correction('quintessential') == 'quintessential' # unknown


    assert words('This is a TEST.') == ['this', 'is', 'a', 'test']
    assert Counter(words('This is a test. 123; A TEST this is.')) == (
           Counter({'123': 1, 'a': 2, 'is': 2, 'test': 2, 'this': 2}))
    assert len(word_count) == 32198
    assert sum(word_count.values()) == 1115585
    assert word_count.most_common(10) == [
     ('the', 79809),
     ('of', 40024),
     ('and', 38312),
     ('to', 28765),
     ('in', 22023),
     ('a', 21124),
     ('that', 12512),
     ('he', 12401),
     ('was', 11410),
     ('it', 10681)]
    assert word_count['the'] == 79809
    assert P('quintessential') == 0
    assert 0.07 < P('the') < 0.08

    return 'unit_tests pass'

def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    start = timeit.default_timer()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in word_count)
            if verbose:
                print(f'correction({wrong}) => {w} ({word_count[w]}); expected {right} ({word_count[right]})')
    dt = timeit.default_timer() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '.format(good / n, n, unknown / n, n / dt))


def TestSet(file):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in file)
            for wrong in wrongs.split()]



if __name__ == "__main__":
    print(unit_tests())
    spelltest(TestSet(open("development_set.txt")))
    spelltest(TestSet(open("test_set.txt")))