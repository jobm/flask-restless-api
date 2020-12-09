from collections import defaultdict

# cost per day in usd
MIN_FICTION_COST = 3
MIN_NOVEL_COST = 4.5
MIN_REGULAR_COST = 2


def regular_book_costs(num_days):
    dict_ = defaultdict(lambda: 1.5 * num_days)
    dict_[1] = MIN_REGULAR_COST
    return dict_[num_days]


def novel_book_costs(num_days):
    dict_ = defaultdict(lambda: 1.5 * num_days)
    dict_[1] = MIN_NOVEL_COST
    dict_[2] = MIN_NOVEL_COST
    return dict_[num_days]


def fiction_book_costs(num_days):
    return MIN_FICTION_COST * num_days
