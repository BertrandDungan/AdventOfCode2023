from re import findall
from pathlib import Path

number_words = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]

regex_num = "|".join(number_words)


def get_calibration_values(file_contents: str) -> list[tuple[str, str, str]]:
    return findall(
        rf"([0-9]|{regex_num})[a-z0-9]*([0-9]|{regex_num})|([0-9]|{regex_num})",
        file_contents,
    )


def to_decimal(input: str) -> str:
    if input.isdigit():
        return input
    matching_index = number_words.index(input)
    return str(matching_index + 1)


def combine_or_double(input: tuple[str, str, str]) -> int:
    if input[2] == "":
        return int(to_decimal(input[0]) + to_decimal(input[1]))
    return int(to_decimal(input[2]) + to_decimal(input[2]))


data_path = Path(__file__).with_name("prompt.txt")
file_text = data_path.read_text()
found_values = get_calibration_values(file_text)
concatenated_numbers = map(combine_or_double, found_values)
calibration_result = sum(concatenated_numbers)
print(calibration_result)
