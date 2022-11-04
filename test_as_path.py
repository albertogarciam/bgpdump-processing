#!/usr/bin/env python3

'''Tests for as_path utilities.'''

import pytest
from as_path import as_path_remove_prepending, is_as_path, as_path_length, as_path_length_no_prepending, origin_as, closest_as, is_as_in_aspath, maximum_common_path, count_ases

# test vectors: (input, expected_value)
IS_AS_PATH = [
    ('', True),
    ('12983', True),
    ('1 2', True),
    ('    24455          222276677   ', True),
    ('24555 {2222 9822} 44', True),
    ('{222 44444 333}', True),
    ('{}', True),
    ('222{ 222}', True), # This may not be a valid as_path, but it is reported as true

    ('1a44', False),
    ('222 {', False),
    ('222 }', False),
    ('222 { 4} 33 { 4}', False)
]


REMOVE_PREPENDING = [
    ("", ""),
    ("1 2 3",    "1 2 3" ),
    ("1 2    3",    "1 2 3" ),
    ("1 2 2 2 3",    "1 2 3" ),
    ("1 1 1 1 2 3",    "1 2 3" ),
    ("1 2 3 3 3    3",    "1 2 3" ),
    ("1 1 1 2 2 2 3 3 3  3",    "1 2 3" ),

    ("1 {5} 3",    "1 {5} 3" ),
    ("1 {3 5}  3",    "1 {3 5} 3" ),

    ("1  1 1 1",    "1" ),
    ("10  10 10 10",    "10" ),
    ("13 13 13 13 27 27 398",    "13 27 398" ),
    ("1  2 2 1 2",    "1 2 1 2" ), 

    # Does not remove properly prepending inside an AS_SET
    # Note that there should not be repeated ASes inside an AS_SET.
    ("1 {3 5 5 5}  3",    "1 {3 5 5} 3" ),

    # Next it is NOT prepending (this is a loop!)
    (" 87 222 87", "87 222 87")
]


AS_PATH_LENGTH = [
    ("", 0),
    (" 22222 ", 1),
    ("1 2 3", 3),

    ("{22 22 2}", 1),
    ("{22}", 1),
    ("2     {22 22 2}", 2),
    ("34 {22 22 2}   67", 3),
    ("{22}     4", 2),
]


COUNT_ASES = [
    ("", 0),
    (" 22222 ", 1),
    ("1 2 3", 3),

    ("{22 22 2}", 3),   # difference with as_path length
    ("{22}", 1),        
    ("2     {22 22 2}", 4), # difference with as_path length
    ("34 {22 22 2}   67", 5), # difference with as_path length
    ("{22}     4", 2), 
]

AS_PATH_LENGTH_NO_PREPENDING = [
    ("", 0),
    (" 3333 ", 1),
    (" 3333 3333", 1),
    ("1 2 2 3", 3),
    ("1 1 1 2 2 3 3 3 3", 3),
    (" 1 2 1", 3),

    ("{22 22 2}", 1),
    ("{22}", 1),
    ("2     {22 22 2}", 2),
    ("34 {22 22 2}   67", 3),
    ("{22}     4", 2),
]


ORIGIN_AS = [
    ("", ""),
    ("1 2  345 ", "345"),
    ("1 {3  4} 345", "345"),
]


ORIGIN_AS_RAISE = [
    ("{1}"),
    ("1 2 3 {1}"),
    ("1 2 3 {1 2}"),
    ("1 2 3 {1 2    }  "),
]


CLOSEST_AS = [
    ("", ""),
    (" 1 2  345 ", "1"),
    ("123 {3  4} 345", "123"),
]


CLOSEST_AS_RAISE = [
    ("{1}"),
    (" {1 } 2 3 34"),
    ("{1 2} 3 4 5"),
    (" {   1 2}  3 4 56 "),
]


AS_IN_AS_PATH = [
    ("1", "1 2 3",  True),
    (" 1 ", "  1 2 3 ",  True),
    (" 2 ", "  1 2 3 ",  True),
    (" 3 ", "  1 2 3 ",  True),
    ("1", "1 2 3",  True),
    ("2", "1 2 3",  True),
    ("3", "1 2 3",  True),

    ("22", "1 {22 44 77} 3",  True),
    ("44", "1 {22 44 77} 3",  True),
    ("77", "1 {22 44 77} 3",  True),
    ("44", "1 {44} 3",  True),

    (" 3 ", "  1 22 33 ",  False),
    ("1", "  11 22 33 ",  False),
    ("2", "  11 22 33 ",  False),
    ("67", "  11 22 33 ",  False),
    ("a", "  11 22 33 ",  False), # Not checking asn, this may change

]

MAX_COMMON = [
    ("3 2 1", "3 2 1", "3 2 1"),
    ("33 22 11", "33 22 11", "33 22 11"),
    (" 44 33 22 11", "33 22 11 ", "33 22 11"),
    (" 44 33 22 11", " 11 ", "11"),

    ("2 1", "1 ", " 1"),
    (" 1 ", "1", "1"),


    ("33 22 11", "33 22", ""),
    ("", "", ""),
    ("3 2 1", "", ""),
    ("5 6 7", "1 2 3", ""),
]


@pytest.mark.parametrize("input,expected", IS_AS_PATH)
def test_is_as_path(input, expected):
    assert is_as_path(input) == expected


@pytest.mark.parametrize("input,expected", REMOVE_PREPENDING)
def test_remove_prepending(input, expected):
    assert as_path_remove_prepending(input) == expected


@pytest.mark.parametrize("input,expected", AS_PATH_LENGTH)
def test_as_path_length(input, expected):
    assert as_path_length(input) == expected

@pytest.mark.parametrize("input,expected", COUNT_ASES)
def test_count_ases(input, expected):
    assert count_ases(input) == expected




@pytest.mark.parametrize("input,expected", AS_PATH_LENGTH_NO_PREPENDING)
def test_as_path_length_no_prepending(input, expected):
    assert as_path_length_no_prepending(input) == expected


@pytest.mark.parametrize("input,expected", ORIGIN_AS)
def test_origin_as(input, expected):
    assert origin_as(input) == expected


@pytest.mark.parametrize("input", ORIGIN_AS_RAISE)
def test_origin_as_raise(input ):

    with pytest.raises(Exception):
        result = origin_as(input)


@pytest.mark.parametrize("input,expected", CLOSEST_AS)
def test_closest_as(input, expected):
    assert closest_as(input) == expected


@pytest.mark.parametrize("input", CLOSEST_AS_RAISE)
def test_closest_as_raise(input ):

    with pytest.raises(Exception):
        result = closest_as(input)

@pytest.mark.parametrize("input1,input2,expected", AS_IN_AS_PATH)
def test_as_in_as_path(input1, input2, expected):
    assert is_as_in_aspath(input1, input2) == expected


# test common origin (from right to left)
@pytest.mark.parametrize("as1,as2,common", MAX_COMMON)
def test_is_common_path(as1, as2, common):
    assert maximum_common_path(as1, as2) == common.strip()
    assert maximum_common_path(as2, as1) == common.strip()