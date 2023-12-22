from typing import NamedTuple
from itertools import batched
from pathlib import Path
from re import search, Pattern, compile


class Mapping(NamedTuple):
    transformation: int
    start: int
    stop: int


SEEDS_REGEX = compile(r"seeds: ([0-9 ]+)\n")
SOIL_REGEX = compile(r"soil map:\n([0-9 \n]+)")
FERTILISER_REGEX = compile(r"fertilizer map:\n([0-9 \n]+)")
WATER_REGEX = compile(r"water map:\n([0-9 \n]+)")
LIGHT_REGEX = compile(r"light map:\n([0-9 \n]+)")
TEMPERATURE_REGEX = compile(r"temperature map:\n([0-9 \n]+)")
HUMIDITY_REGEX = compile(r"humidity map:\n([0-9 \n]+)")
LOCATION_REGEX = compile(r"location map:\n([0-9 \n]+)")


def find_numbers(text: str, pattern: Pattern) -> list[int]:
    results = search(pattern, text)
    assert results is not None
    return [int(result) for result in results.group(1).split()]


def get_seeds(text: str) -> list[int]:
    return find_numbers(text, SEEDS_REGEX)


def get_mapping(text: str, pattern: Pattern) -> list[Mapping]:
    return [
        Mapping(group[0] - group[1], group[1], group[1] + group[2])
        for group in batched(find_numbers(text, pattern), 3)
    ]


def matching_range(source: int, transformation: Mapping) -> bool:
    return transformation.start <= source and transformation.stop >= source


def transform(source: int, transformations: list[Mapping]) -> int:
    if any(
        matching_range(source, (matching_transformation := transformation))
        for transformation in transformations
    ):
        return source + matching_transformation.transformation
    return source


data_path = Path(__file__).with_name("prompt.txt")
file_text = data_path.read_text()

seeds = get_seeds(file_text)
soil_map = get_mapping(file_text, SOIL_REGEX)
fertiliser_map = get_mapping(file_text, FERTILISER_REGEX)
water_map = get_mapping(file_text, WATER_REGEX)
light_map = get_mapping(file_text, LIGHT_REGEX)
temperature_map = get_mapping(file_text, TEMPERATURE_REGEX)
humidity_map = get_mapping(file_text, HUMIDITY_REGEX)
location_map = get_mapping(file_text, LOCATION_REGEX)

soil_for_seeds = [transform(seed, soil_map) for seed in seeds]
fertiliser_for_soil = [transform(seed, fertiliser_map) for seed in soil_for_seeds]
water_for_fertiliser = [transform(seed, water_map) for seed in fertiliser_for_soil]
light_for_water = [transform(seed, light_map) for seed in water_for_fertiliser]
temperature_for_light = [transform(seed, temperature_map) for seed in light_for_water]
humidity_for_temperature = [
    transform(seed, humidity_map) for seed in temperature_for_light
]
location_for_humidity = [
    transform(seed, location_map) for seed in humidity_for_temperature
]

print(min(location_for_humidity))
