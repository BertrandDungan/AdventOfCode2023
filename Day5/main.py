from typing import NamedTuple
from itertools import batched, chain
from pathlib import Path
from re import search, Pattern, compile


class Mapping(NamedTuple):
    transformation: int
    start: int
    stop: int


class AlmanacRange(NamedTuple):
    start: int
    stop: int


MAPPING_REGEX = [
    r"soil map:\n([0-9 \n]+)",
    r"fertilizer map:\n([0-9 \n]+)",
    r"water map:\n([0-9 \n]+)",
    r"light map:\n([0-9 \n]+)",
    r"temperature map:\n([0-9 \n]+)",
    r"humidity map:\n([0-9 \n]+)",
    r"location map:\n([0-9 \n]+)",
]


def find_numbers(text: str, pattern: Pattern) -> list[int]:
    results = search(pattern, text)
    assert results is not None
    return [int(result) for result in results.group(1).split()]


def get_seeds(text: str) -> list[AlmanacRange]:
    all_seed_numbers = find_numbers(text, compile(r"seeds: ([0-9 ]+)\n"))
    seed_pairs = batched(all_seed_numbers, 2)
    return [AlmanacRange(pair[0], pair[0] + pair[1]) for pair in seed_pairs]


def get_mapping(text: str, pattern: Pattern) -> list[Mapping]:
    return [
        Mapping(group[0] - group[1], group[1], group[1] + group[2])
        for group in batched(find_numbers(text, pattern), 3)
    ]


def matching_range(source: AlmanacRange, transformation: Mapping) -> bool:
    return source.start >= transformation.start and source.stop <= transformation.stop


def overlapping_range(source: AlmanacRange, transformation: Mapping) -> bool:
    return source.start <= transformation.stop and transformation.start <= source.stop


def transform(
    source: AlmanacRange, transformations: list[Mapping]
) -> list[AlmanacRange]:
    for transformation in transformations:
        if matching_range(source, (matching_transformation := transformation)):
            return [
                AlmanacRange(
                    source.start + matching_transformation.transformation,
                    source.stop + matching_transformation.transformation,
                )
            ]
        if overlapping_range(source, (matching_transformation := transformation)):
            split_source = AlmanacRange(
                max(source.start, matching_transformation.start),
                min(source.stop, matching_transformation.stop),
            )

            transformed_range = [
                AlmanacRange(
                    split_source.start + matching_transformation.transformation,
                    split_source.stop + matching_transformation.transformation,
                )
            ]

            first_half = AlmanacRange(source.start, split_source.start - 1)
            if (
                first_half.start != split_source.start
                and first_half.stop != split_source.stop
                and first_half.start <= first_half.stop
            ):
                transformed_range.extend(transform(first_half, transformations))
            second_half = AlmanacRange(split_source.stop + 1, source.stop)
            if (
                split_source.start != second_half.start
                and second_half.stop != split_source.stop
                and second_half.start <= second_half.stop
            ):
                transformed_range.extend(transform(second_half, transformations))
            return transformed_range

    return [source]


def almanac_transform(
    input: list[AlmanacRange], mapping: list[Mapping]
) -> list[AlmanacRange]:
    return list(chain(*[transform(almanacNum, mapping) for almanacNum in input]))


data_path = Path(__file__).with_name("prompt.txt")
file_text = data_path.read_text()

transformation_mappings = [
    get_mapping(file_text, compile(regex)) for regex in MAPPING_REGEX
]

soil_for_seeds = almanac_transform(get_seeds(file_text), transformation_mappings[0])
fertiliser_for_soil = almanac_transform(soil_for_seeds, transformation_mappings[1])
water_for_fertiliser = almanac_transform(
    fertiliser_for_soil, transformation_mappings[2]
)
light_for_water = almanac_transform(water_for_fertiliser, transformation_mappings[3])
temperature_for_light = almanac_transform(light_for_water, transformation_mappings[4])
humidity_for_temperature = almanac_transform(
    temperature_for_light, transformation_mappings[5]
)
location_for_humidity = almanac_transform(
    humidity_for_temperature, transformation_mappings[6]
)

print(min(location_for_humidity).start)
