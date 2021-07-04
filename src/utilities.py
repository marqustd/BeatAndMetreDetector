def find_last_index_of_less_or_equal(list, value):
    return max(idx for idx, val in enumerate(list) if val <= value)
