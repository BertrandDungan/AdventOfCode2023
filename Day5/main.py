from typing import NamedTuple
from itertools import batched, chain
from pathlib import Path
from re import search, Pattern, compile


class Mapping(NamedTuple):
    transformation: int
    start: int
    stop: int


class SeedRange(NamedTuple):
    start: int
    stop: int


def find_numbers(text: str, pattern: Pattern) -> list[int]:
    results = search(pattern, text)
    assert results is not None
    return [int(result) for result in results.group(1).split()]


def get_seeds(text: str) -> list[SeedRange]:
    all_seed_numbers = find_numbers(text, compile(r"seeds: ([0-9 ]+)\n"))
    seed_pairs = batched(all_seed_numbers, 2)
    return [SeedRange(pair[0], pair[0] + pair[1]) for pair in seed_pairs]


def get_mapping(text: str, pattern: Pattern) -> list[Mapping]:
    return [
        Mapping(group[0] - group[1], group[1], group[1] + group[2])
        for group in batched(find_numbers(text, pattern), 3)
    ]


def matching_range(source: SeedRange, transformation: Mapping) -> bool:
    return transformation.start <= source.stop and transformation.stop >= source.start


def overlapping_range(source: SeedRange, transformation: Mapping) -> bool:
    return (
        transformation.start <= source.stop and transformation.stop >= source.stop
    ) or (transformation.stop >= source.start and transformation.start <= source.start)


def transform(source: SeedRange, transformations: list[Mapping]) -> list[SeedRange]:
    for transformation in transformations:
        if matching_range(source, (matching_transformation := transformation)):
            return [
                SeedRange(
                    source.start + matching_transformation.transformation,
                    source.stop + matching_transformation.transformation,
                )
            ]
        if overlapping_range(source, (matching_transformation := transformation)):
            split_source = SeedRange(
                max(source.start, matching_transformation.start),
                min(source.stop, matching_transformation.stop),
            )

            transformed_range = [split_source]

            first_half = SeedRange(source.start, split_source.start)
            if first_half.start != split_source.start:
                transformed_range.extend(transform(first_half, transformations))
            second_half = SeedRange(split_source.stop, source.stop)
            if second_half.stop != split_source.stop:
                transformed_range.extend(transform(second_half, transformations))
            return transformed_range

    return [source]


data_path = Path(__file__).with_name("prompt.txt")
file_text = data_path.read_text()

seeds = get_seeds(file_text)
soil_map = get_mapping(file_text, compile(r"soil map:\n([0-9 \n]+)"))
fertiliser_map = get_mapping(file_text, compile(r"fertilizer map:\n([0-9 \n]+)"))
water_map = get_mapping(file_text, compile(r"water map:\n([0-9 \n]+)"))
light_map = get_mapping(file_text, compile(r"light map:\n([0-9 \n]+)"))
temperature_map = get_mapping(file_text, compile(r"temperature map:\n([0-9 \n]+)"))
humidity_map = get_mapping(file_text, compile(r"humidity map:\n([0-9 \n]+)"))
location_map = get_mapping(file_text, compile(r"location map:\n([0-9 \n]+)"))

soil_for_seeds = list(chain(*[transform(seed, soil_map) for seed in seeds]))
fertiliser_for_soil = list(
    chain(*[transform(seed, fertiliser_map) for seed in soil_for_seeds])
)
water_for_fertiliser = list(
    chain(*[transform(seed, water_map) for seed in fertiliser_for_soil])
)
light_for_water = list(
    chain(*[transform(seed, light_map) for seed in water_for_fertiliser])
)
temperature_for_light = list(
    chain(*[transform(seed, temperature_map) for seed in light_for_water])
)
humidity_for_temperature = list(
    chain(*[transform(seed, humidity_map) for seed in temperature_for_light])
)
location_for_humidity = list(
    chain(*[transform(seed, location_map) for seed in humidity_for_temperature])
)


print(min(location_for_humidity).start)
# 71100042 too low
