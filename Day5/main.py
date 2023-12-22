from typing import NamedTuple
from itertools import batched
from pathlib import Path
from re import search, Pattern, compile


class Mapping(NamedTuple):
    transformation: int
    start: int
    stop: int


class SeedRange(NamedTuple):
    start: int
    stop: int


def find_numbers(text: str, pattern: Pattern) -> [int]:
    results = search(pattern, text)
    assert results is not None
    return [int(result) for result in results.group(1).split()]


def get_seeds(text: str) -> [SeedRange]:
    all_seed_numbers = find_numbers(text, compile(r"seeds: ([0-9 ]+)\n"))
    seed_pairs = batched(all_seed_numbers, 2)
    return [SeedRange(pair[0], pair[1]) for pair in seed_pairs]


def get_mapping(text: str, pattern: Pattern) -> [Mapping]:
    return [
        Mapping(group[0] - group[1], group[1], group[1] + group[2])
        for group in batched(find_numbers(text, pattern), 3)
    ]


def matching_range(source: int, transformation: Mapping) -> bool:
    return transformation.start <= source and transformation.stop >= source


def transform(source: SeedRange, transformations: list[Mapping]) -> [SeedRange]:
    if any(
        matching_range(source, (matching_transformation := transformation))
        for transformation in transformations
    ):
        return source + matching_transformation.transformation
    return source


data_path = Path(__file__).with_name("test.txt")
file_text = data_path.read_text()

seeds = get_seeds(file_text)
soil_map = get_mapping(file_text, compile(r"soil map:\n([0-9 \n]+)"))
fertiliser_map = get_mapping(file_text, compile(r"fertilizer map:\n([0-9 \n]+)"))
water_map = get_mapping(file_text, compile(r"water map:\n([0-9 \n]+)"))
light_map = get_mapping(file_text, compile(r"light map:\n([0-9 \n]+)"))
temperature_map = get_mapping(file_text, compile(r"temperature map:\n([0-9 \n]+)"))
humidity_map = get_mapping(file_text, compile(r"humidity map:\n([0-9 \n]+)"))
location_map = get_mapping(file_text, compile(r"location map:\n([0-9 \n]+)"))

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
