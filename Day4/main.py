from functools import reduce
from pathlib import Path


def get_card_numbers(line: str) -> tuple[list[str], list[str]]:
    split_card = line.split("|")

    winning_side = split_card[0].split(":")[1]
    our_side = split_card[1]

    winning_numbers = winning_side.split()
    our_numbers = our_side.split()
    return (winning_numbers, our_numbers)


def card_score(current_score: int) -> int:
    if current_score == 0:
        return 1
    return current_score * 2


def get_card_value(card: tuple[list[str], list[str]]) -> int:
    card_value = reduce(
        lambda acc, current_number: card_score(acc)
        if current_number in card[0]
        else acc,
        card[1],
        0,
    )
    return card_value


data_path = Path(__file__).with_name("prompt.txt")
file_text = data_path.read_text()
file_lines = file_text.splitlines()

card_numbers = [get_card_numbers(line) for line in file_lines]
card_values = [get_card_value(card) for card in card_numbers]
all_values = sum(card_values)

print(all_values)
