from itertools import batched
from pathlib import Path
from re import search, Pattern, compile

SEEDS_REGEX = compile(r"seeds: ([0-9 ]+)\n")
SOIL_REGEX = compile(r"soil map:\n([0-9 \n]+)")
FERTILISER_REGEX = compile(r"fertilizer map:\n([0-9 \n]+)")
WATER_REGEX = compile(r"water map:\n([0-9 \n]+)")
LIGHT_REGEX = compile(r"light map:\n([0-9 \n]+)")
TEMPERATURE_REGEX = compile(r"temperature map:\n([0-9 \n]+)")
HUMIDITY_REGEX = compile(r"humidity map:\n([0-9 \n]+)")
LOCATION_REGEX = compile(r"location map:\n([0-9 \n]+)")


def group_by_three(input: list[int]):
    return list(batched(input, 3))


def find_numbers(text: str, pattern: Pattern) -> list[int]:
    results = search(pattern, text)
    assert results is not None
    return [int(result) for result in results.group(1).split()]


def get_seeds(text: str) -> list[int]:
    return find_numbers(text, SEEDS_REGEX)


def get_mapping(text: str, pattern: Pattern) -> list[tuple[int, int, int]]:
    return group_by_three(find_numbers(text, pattern))


data_path = Path(__file__).with_name("test.txt")
file_text = data_path.read_text()

seeds = get_seeds(file_text)
soil_map = get_mapping(file_text, SOIL_REGEX)
fertiliser_map = get_mapping(file_text, FERTILISER_REGEX)
water_map = get_mapping(file_text, WATER_REGEX)
light_map = get_mapping(file_text, LIGHT_REGEX)
temperature_map = get_mapping(file_text, TEMPERATURE_REGEX)
humidity_map = get_mapping(file_text, HUMIDITY_REGEX)
location_map = get_mapping(file_text, LOCATION_REGEX)


print(soil_map)
