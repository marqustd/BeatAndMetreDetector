def findLastIndexOfLessOrEqual(list, value):
    return max(idx for idx, val in enumerate(list) if val <= value)
