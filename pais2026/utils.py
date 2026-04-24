def multiply_list(values, multiplier):
    values_copy = values.copy()
    for i in range(len(values)):
        values_copy[i] = values[i] * multiplier
    return values_copy


def multiply_list_by_list(list1, list2):
    return [a * b for a, b in zip(list1, list2)]


def multiply_list_by_scalar(list1, scalar):
    return [a * scalar for a in list1]


def sum_two_lists(list1, list2):
    return [a + b for a, b in zip(list1, list2)]


def complement(values):
    return [1 - i for i in values]
