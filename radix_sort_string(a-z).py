def radix_sort_str(str_list):
    """
    Sorts a list of 'a' to 'z' strings
    :return: a list of string, sorted ascendingly
    Time Complexity: O(N + k) where n is the length of the list and k is the length of the longest string
    """
    if not str_list:
        return str_list
    max_place_value = len(max(str_list, key=len))-1
    place_value = max_place_value
    while place_value >= 0:
        str_list = counting_sort_str(str_list, place_value)
        place_value -= 1
    return str_list


def counting_sort_str(str_list, place_value_idx):
    """
    Note: It is essential that this counting sort is stable otherwise the radix sort will not return correctly
    Time Complexity: O(n + k) where n is the length of the list and k is the length of the longest string
    :return: the input list but instead now ordered ascendingly by the place value given by: place_value_idx
    corresponding to the said base
    """
    def get_number(word):
        if place_value_idx >= len(word):
            return 0
        else:
            return ord(word[place_value_idx]) - ASCII_REMOVAL
    ASCII_UPPER = ord("z")
    ASCII_REMOVAL = ord("a") - 1
    ASCII_RANGE = ASCII_UPPER - ASCII_REMOVAL + 1
    n = len(str_list)
    count_lst = [0] * ASCII_RANGE
    position_lst = [0] * ASCII_RANGE
    output_lst = [0] * n
    # for count list
    for j in range(n):
        count_lst[get_number(str_list[j])] += 1
    # for position list
    for idx in range(1, ASCII_RANGE):
        position_lst[idx] = position_lst[idx - 1] + count_lst[idx - 1]
    # for output list
    for i in range(n):
        number = get_number(str_list[i])
        output_lst[position_lst[number]] = str_list[i]
        position_lst[number] += 1
    return output_lst