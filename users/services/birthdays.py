import functools
from collections.abc import Callable
from typing import Protocol

__all__ = ('is_beautiful_number',)


class SupportsStrOrRepr(Protocol):

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...


def is_length_equals(item: SupportsStrOrRepr, *, to) -> bool:
    return len(str(item)) == to


def contains_same_digits(item: SupportsStrOrRepr) -> bool:
    return len(set(str(item))) == 1


def halves_contain_same_digits(item: SupportsStrOrRepr) -> bool:
    item = str(item)
    characters_count = len(item)
    if characters_count % 2 != 0:
        return False
    center = characters_count // 2
    first_half, second_half = item[:center], item[center:]
    return (
            contains_same_digits(first_half)
            and contains_same_digits(second_half)
    )


def is_even_odd_symmetric(item: SupportsStrOrRepr) -> bool:
    item_str = str(item)
    even_position_characters = item_str[::2]
    odd_position_characters = item_str[1::2]
    return (
            is_palindrome(even_position_characters)
            and is_palindrome(odd_position_characters)
    )


def is_palindrome(item: SupportsStrOrRepr) -> bool:
    item_str = str(item)
    return item_str == item_str[::-1]


def is_last_two_digits_zeros(number: SupportsStrOrRepr) -> bool:
    return str(number)[-2:] == '00'


def is_increasing_number(number: SupportsStrOrRepr, *, step) -> bool:
    number_str = str(number)
    for i in range(1, len(number_str)):
        if int(number_str[i]) - int(number_str[i - 1]) != step:
            return False
    return True


def is_decreasing_number(number: SupportsStrOrRepr, *, step) -> bool:
    return is_increasing_number(number, step=-step)


def all_digits_same_except_last_zero(number: SupportsStrOrRepr) -> bool:
    number_str = str(number)
    return contains_same_digits(number_str[:-1]) and number_str[-1] == '0'


predicates: tuple[Callable[[int | str], bool], ...] = (
    contains_same_digits,
    halves_contain_same_digits,
    is_even_odd_symmetric,
    is_palindrome,
    is_last_two_digits_zeros,
    all_digits_same_except_last_zero,
    functools.partial(is_increasing_number, step=1),
    functools.partial(is_decreasing_number, step=1),
)


def is_beautiful_number(number: int) -> bool:
    return any(predicate(number) for predicate in predicates)
