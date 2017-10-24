"""
Author: Floyd Kots ~ github.com/floydkots
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

codeskulptor.set_timeout(30)

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    clean = []
    dummy_ret = [clean.append(item) for item in list1 if item not in clean]
    return clean

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    both = []
    shorter = list1 if len(list1) < len(list2) else list2
    longer = list2 if len(list1) < len(list2) else list1
    for item in shorter:
        if item in longer:
            both.append(item)
    return both

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    #print "in_merge", "left", list1, "right", list2
    merged = []
    shorter = list(list1) if len(list1) < len(list2) else list(list2)
    longer = list(list2) if len(list1) < len(list2) else list(list1)
    
    while shorter and longer:
        if shorter[-1] > longer[-1]:
            merged.insert(0, shorter.pop())
        else:
            merged.insert(0, longer.pop())
        
    for item in (shorter or longer)[::-1]:
        merged.insert(0, item)
    return merged
        
          
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    else:
        left = merge_sort(list1[:len(list1)/2])
        right = merge_sort(list1[len(list1)/2:])
        return merge(left, right)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if not word:
        return [word]
    
    first = word[0]
    rest = word[1:]
    
    rest_strings = gen_all_strings(rest)
    
    new_strings = []
    for string in rest_strings:
        for idx in range(len(string) + 1):
            new_string = string[:idx] + first + string[idx:]
            new_strings.append(new_string)
    return rest_strings + new_strings
    

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    words = urllib2.urlopen(url)
    return [word[:-1] for word in words.readlines()]

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

run()
 
import poc_simpletest

def test_funcs():
    """
    Tests for the various helper functions.
    """
    ts = poc_simpletest.TestSuite()
    
    ts.run_test(remove_duplicates([1, 1, 2, 2, 3, 3]), [1, 2, 3], "remove_duplicates([1, 1, 2, 2, 3, 3])")
    ts.run_test(remove_duplicates([1, 2, 3]), [1, 2, 3], "remove_duplicates([1, 2, 3])")
    ts.run_test(remove_duplicates([]), [], "remove_duplicates([])")
    
    ts.run_test(intersect([1, 2, 3, 4], [1, 3]), [1, 3], "intersect([1, 2, 3, 4], [1, 3])")
    ts.run_test(intersect([1, 4, 6], [1, 3, 4, 5, 6]), [1, 4, 6], "intersect([1, 4, 6], [1, 3, 4, 5, 6])")
    ts.run_test(intersect([1, 4, 6], []), [], "intersect([])")
    ts.run_test(intersect([], []), [], "intersect([], [])")
    ts.run_test(intersect([1, 4, 6], [1, 4, 6]), [1, 4, 6], "intersect([1, 4, 6], [1, 4, 6])")
    
    ts.run_test(merge([1, 3, 5],[2, 4]), [1, 2, 3, 4, 5], "merge([1, 3, 5],[2, 4]")
    ts.run_test(merge([1, 3, 5],[1, 3, 5]), [1, 1, 3, 3, 5, 5], "merge([1, 3, 5],[1, 3, 5])")
    ts.run_test(merge([1, 4, 9, 10],[0, 1, 3, 5, 11]), [0, 1, 1, 3, 4, 5, 9, 10, 11], "merge([1, 4, 9, 10],[0, 1, 3, 5, 11])")
    ts.run_test(merge([], []), [], "merge([], [])")
    ts.run_test(merge([9], []), [9], "merge([9], [])")
    ts.run_test(merge([2], [1]), [1, 2], "merge([2], [1])")
    ts.run_test(merge([3], [1, 2]), [1, 2, 3], "merge([3], [1, 2])")
    
    ts.run_test(merge_sort([3, 2, 1]), [1, 2, 3], "merge_sort([3, 2, 1])")
    ts.run_test(merge_sort([3, 2, 4, 1]), [1, 2, 3, 4], "merge_sort([3, 2, 4, 1])")
    ts.run_test(merge_sort([1, 4, 2, 15, 8, 10]), [1, 2, 4, 8, 10, 15], "merge_sort([1, 4, 2, 15, 8, 10])")
    
    ts.run_test(gen_all_strings('a'), ['', 'a'], "gen_all_strings('a')")
    ts.run_test(sorted(gen_all_strings('ab')), sorted(['', 'a', 'b', 'ab', 'ba',]), "gen_all_strings('ab')")
    ts.run_test(sorted(gen_all_strings('aab')), sorted(["", "b", "a", "ab", "ba", "a", "ab", "ba", "aa", "aa", "aab", "aab", "aba", "aba", "baa", "baa"]), "gen_all_strings('aab')")

    
    ts.report_results()
    
test_funcs()
    