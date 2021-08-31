"""
File: anagram.py
Name: 林柏廷 Kyle
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

import time                   # This file allows you to calculate the speed of your algorithm

# Constants
FILE = 'dictionary.txt'       # This is the filename of an English dictionary
EXIT = '-1'                   # Controls when to stop the loop

# Global variables
dictionary_list = []
# Counters for monitoring code performance
recursion_counter = []
word_search_counter = []
prefix_search_counter = []


def main():
    """
    Running anagram program.
    """
    global dictionary_list, recursion_counter, word_search_counter, prefix_search_counter
    print('Welcome to stanCode "Anagram Generator" (or -1 to quit)')
    dictionary_list = read_dictionary()     # read the dictionary .txt file and store in a global variable

    while True:
        str_input = input('Find anagrams for: ')
        # break while loop and end the program when user types '-1'
        if str_input == '-1':
            break
        start = time.time()         # timer for execution time
        find_anagrams(str_input)    # find anagrams of user's input
        end = time.time()           # timer for execution time
        print('----------------------------------')
        # code below prints execution time and the numbers of times different functions were called
        print(f'The speed of your anagram algorithm: {end-start} seconds.')
        print(f'Recursion ran {len(recursion_counter)} times.')
        print(f'Word search ran {len(word_search_counter)} times.')
        print(f'Prefix search ran {len(prefix_search_counter)} times.')
        print('----------------------------------')

        # reset counters for next anagram search
        recursion_counter.clear()
        word_search_counter.clear()
        prefix_search_counter.clear()


def read_dictionary():
    """
    Reads the dictionary .txt file, put all words into a list.
    :return: Dictionary(list)
    """
    dictionary_lst = []
    with open(FILE, 'r') as f:
        for word in f:
            dictionary_lst.append(word.strip())
    return dictionary_lst


def find_anagrams(s):
    """
    :param s: The string for searching anagrams
    :return: None
    """
    anagrams_lst = []
    print('Searching...')
    # calling the helper function
    helper(s, [], [], anagrams_lst)
    # print all anagrams found
    print(f'{len(anagrams_lst)} anagrams: ', anagrams_lst)


def helper(original_str, current_lst, used_lst, found_lst):
    """
    :param original_str: The original string for anagram search
    :param current_lst: A list that helps run permutation.
    :param used_lst: Stores the indexes of the characters used in current_lst.
    :param found_lst: Stores all anagrams found.
    :return: None
    """
    ############################
    recursion_counter.append(1)     # counter length +1 in each function call
    ############################

    # Base Case
    if len(current_lst) == len(original_str):
        anagram = ''.join(current_lst)      # join all characters in the current_lst into a string
        if search_dict(anagram) is True:    # search and check if the string is included in the dictionary
            if anagram in found_lst:        # avoid double counting same word. ex. a(0)p(1)p(2), a(0)p(2)p(1)
                return
            found_lst.append(anagram)       # a new anagram is found, append it to the found_lst
            print(f'Found: {anagram}')      # print the result
            print('Searching...')
    # Recursive Case
    else:
        for ind, alphabet in enumerate(original_str):
            if ind in used_lst:     # avoid using the same character twice
                pass
            else:
                # choose
                current_lst.append(alphabet)
                used_lst.append(ind)
                # check if the unfinished string matches any prefix in the dictionary
                if has_prefix(''.join(current_lst)) is True:
                    # explore (recursive call)
                    helper(original_str, current_lst, used_lst, found_lst)
                # un-choose
                current_lst.pop()
                used_lst.pop()


def has_prefix(sub_s):
    """
    :param sub_s: The sub-string (unfinished string) for prefix matching in the dictionary
    :param word_length: (int) The length of the original string
    :return: The return value of prefix search
    """
    global dictionary_list
    return prefix_search(sub_s, 0, len(dictionary_list)-1)     # calling new binary search for prefix


def prefix_search(sub_s, lower_bound, upper_bound):
    """
    :param sub_s: The sub-string (unfinished string) for prefix matching in the dictionary
    :param lower_bound: Lower bound for binary search
    :param upper_bound: Upper bound for binary search
    :return: True or False
    """
    ############################
    global prefix_search_counter
    prefix_search_counter.append(1)                 # counter length +1 in each function call
    ############################

    # binary search
    mid_index = (lower_bound + upper_bound) // 2    # get the index in the middle
    # worst case (find the target when there are two words left for search, or fail to find any match)
    if mid_index == lower_bound:                    # when upper_bound == lower_bound +1
        if dictionary_list[lower_bound][0:len(sub_s)] != sub_s and dictionary_list[upper_bound][0:len(sub_s)] != sub_s:
            return False
        else:
            return True
    # recursive call when the prefix does not match dictionary_list[mid_index]
    if dictionary_list[mid_index][0:len(sub_s)] > sub_s:
        return prefix_search(sub_s, lower_bound, mid_index)
    elif dictionary_list[mid_index][0:len(sub_s)] < sub_s:
        return prefix_search(sub_s, mid_index, upper_bound)
    else:
        return True


def word_search(target, lower_bound, upper_bound):
    """
    :param target: Target string for word matching in the dictionary
    :param lower_bound: Lower bound for binary search
    :param upper_bound: Upper bound for binary search
    :return: True or False
    """
    ############################
    global word_search_counter
    word_search_counter.append(1)                   # counter length +1 in each function call
    ############################

    # binary search
    mid_index = (lower_bound + upper_bound) // 2    # get the index in the middle
    # worst case (find the target when there are two words left for search, or fail to find any match)
    if mid_index == lower_bound:                    # when upper_bound == lower_bound +1
        if dictionary_list[lower_bound] == target or dictionary_list[upper_bound] == target:
            return True
        else:
            return False
    # recursive call when the target is not found
    if dictionary_list[mid_index] > target:
        return word_search(target, lower_bound, mid_index)
    elif dictionary_list[mid_index] < target:
        return word_search(target, mid_index, upper_bound)
    # return True when the target is found
    else:
        return True


def search_dict(target_str):
    """
    Search the dictionary and check if the target_str is in the dictionary.
    :param target_str: The string to search
    :return: True or False
    """
    global dictionary_list

    # linear search
    # for word in dictionary_list:
    #     if word == target_str:
    #         return True
    # return False

    # return target_str in dictionary_list                        # linear? search
    return word_search(target_str, 0, len(dictionary_list)-1)     # binary search


if __name__ == '__main__':
    main()
