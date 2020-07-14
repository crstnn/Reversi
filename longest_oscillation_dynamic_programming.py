
def longest_oscillation(L: list) -> tuple:
    """
	Dynamic Programming of the longest non-contiguous oscilation in a list (i.e. longest subsequence that is a wiggle sequence)
    :param L: A list of integers (could contain duplicates or be empty)
    :return: a 2-tuple with the first element containing the longest oscillating sequence and the second element as a
    list of the indices (from the parameter L) that make up a solution.
    Time Complexity: Runs in O(n) time. Uses O(n) auxiliary space. n being the length of the list L
    """

    size = len(L)
    if not size: return 0, []
    # Add index of first element because we can never find a longer solution by removing the first element.
    best_indexes = [0]

    if size == 1: return 1, [0]
    curr_val = L[0]

    j = 1
    while j < size and L[j] == curr_val:
        j += 1
    if j >= size:
        return 1, [0]
    best_indexes.append(j)
    new_val = L[j]
    last_delta_is_positive = (new_val - curr_val) > 0
    curr_val = new_val

    while True:
        while j < size and L[j] == curr_val:
            j += 1
        if j >= size:
            break
        new_val = L[j]
        new_delta_is_positive = (new_val - curr_val) > 0
        if last_delta_is_positive is new_delta_is_positive:
            best_indexes.pop()
        best_indexes.append(j)
        curr_val = new_val
        last_delta_is_positive = new_delta_is_positive
        j += 1

    return len(best_indexes), best_indexes




