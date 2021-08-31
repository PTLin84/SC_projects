"""
File: boggle.py
Name: 林柏廷 Kyle
----------------------------------------
TODO:
"""

import time

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'
dictionary_list = []
prefix_search_counter = []
word_search_counter = []
recursion_counter = []

# add a constant variable SIZE of the board
SIZE = 4


def main():

    global dictionary_list
    dictionary_list = read_dictionary()

    # user input
    alphabet_lst = []
    # for i in range(SIZE):
    # 	alphabet_lst += [(*(input(f'{i+1} row of letters: ').lower().split(' ')))]		# '*' for unpacking the split list

    # for testing
    alphabet_lst = [*('f,y,c,l,i,o,m,g,o,r,i,l,h,j,h,u'.split(','))]

    # print(alphabet_lst)
    boggle_lst = []
    start = time.time()
    # start playing boggle game
    for ind, ele in enumerate(alphabet_lst):
        explore_boggle(SIZE, '', alphabet_lst, [ind], boggle_lst)  # put current index in the used_lst
    end = time.time()
    print(f'There are {len(boggle_lst)} words in total.')
    print(boggle_lst)
    print('----------------------------------')
    print(f'The speed of your boggle algorithm: {end - start} seconds.')
    print(f'Recursion ran {len(recursion_counter)} times.')
    print(f'Word search ran {len(word_search_counter)} times.')
    print(f'Prefix search ran {len(prefix_search_counter)} times.')


def explore_boggle(n, cur_str, alphabet_lst, used_index, found_lst):
    """
	:param n: Size of the board.
	:param cur_str: Current string for word matching.
	:param alphabet_lst: A list containing all alphabets on the board.
	:param used_index: A list of used indexes.
	:param found_lst: A list storing found words.
	:return: None
	"""
    global recursion_counter
    recursion_counter.append(1)

    # base case
    # the below if statement will short circuit if cur_str length is not enough or already exists in the found_lst
    # short circuit ensures the absence of unnecessary word_search
    if len(cur_str) >= n and cur_str not in found_lst and word_search(cur_str, 0, len(dictionary_list) - 1):
        print(f'Found "{cur_str}"')
        found_lst.append(cur_str)

    # recursive case
    cur_position = used_index[-1]  # last index chosen (type: int)
    cur_row = cur_position // n
    cur_col = cur_position % n

    for i in range(cur_row - 1, cur_row + 2, 1):
        for j in range(cur_col - 1, cur_col + 2, 1):
            if i < 0 or i >= n or j < 0 or j >= n:  # out of bounds
                continue
            cur_index = i * n + j
            if cur_index in used_index:  # do not use the same element
                continue

            # choose
            cur_str += alphabet_lst[cur_index]
            used_index.append(cur_index)
            # explore
            if has_prefix(cur_str) is True:
                explore_boggle(n, cur_str, alphabet_lst, used_index, found_lst)
            # un-choose
            cur_str = cur_str[0:-1]
            used_index.pop()


# loop over every alphabet
# find words for every alphabet (start exploring)


def read_dictionary():
    """
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
	"""
    lst = []
    with open(FILE, 'r') as f:
        for word in f:
            lst.append(word.strip())
    return lst


def has_prefix(sub_s):
    """
    :param sub_s: The sub-string (unfinished string) for prefix matching in the dictionary
    :param word_length: (int) The length of the original string
    :return: The return value of prefix search
    """
    global dictionary_list
    return prefix_search(sub_s, 0, len(dictionary_list) - 1)  # calling new binary search for prefix


def prefix_search(sub_s, lower_bound, upper_bound):
    """
    :param sub_s: The sub-string (unfinished string) for prefix matching in the dictionary
    :param lower_bound: Lower bound for binary search
    :param upper_bound: Upper bound for binary search
    :return: True or False
    """
    ############################
    global prefix_search_counter
    prefix_search_counter.append(1)  # counter length +1 in each function call
    ############################

    # binary search
    mid_index = (lower_bound + upper_bound) // 2  # get the index in the middle
    # worst case (find the target when there are two words left for search, or fail to find any match)
    if mid_index == lower_bound:  # when upper_bound == lower_bound +1
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
    word_search_counter.append(1)  # counter length +1 in each function call
    ############################

    # binary search
    mid_index = (lower_bound + upper_bound) // 2  # get the index in the middle
    # worst case (find the target when there are two words left for search, or fail to find any match)
    if mid_index == lower_bound:  # when upper_bound == lower_bound +1
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
    return word_search(target_str, 0, len(dictionary_list) - 1)  # binary search


if __name__ == '__main__':
    main()
