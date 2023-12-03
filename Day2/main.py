from functools import reduce
from re import search
from typing import TypeAlias, TypedDict
from pathlib import Path

Hand = TypedDict("Hand", {"red": int, "green": int, "blue": int})
Game: TypeAlias = tuple[int, list[Hand]]


MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14


def get_hand_details(hand: str) -> Hand:
    red_search = search(r"([0-9]+) r", hand)
    green_search = search(r"([0-9]+) g", hand)
    blue_search = search(r"([0-9]+) b", hand)

    red = red_search.group(1) if red_search else 0
    green = green_search.group(1) if green_search else 0
    blue = blue_search.group(1) if blue_search else 0

    return {"red": int(red), "green": int(green), "blue": int(blue)}


def get_game_details(index: int, input: str) -> Game:
    game_result = search(r": (.*)", input)
    assert game_result is not None
    all_hands: str = game_result.group(1)
    individual_hands = all_hands.split(";")
    hand_details = [get_hand_details(hand) for hand in individual_hands]
    return (index + 1, hand_details)


def get_games(input: str) -> list[Game]:
    game_lines: list[str] = input.splitlines()
    return [get_game_details(index, line) for index, line in enumerate(game_lines)]


def hand_is_valid(hand: Hand) -> bool:
    if hand["red"] > MAX_RED:
        return False
    if hand["green"] > MAX_GREEN:
        return False
    if hand["blue"] > MAX_BLUE:
        return False
    return True


def is_game_valid(game: Game) -> bool:
    return all(hand_is_valid(hand) for hand in game[1])


def get_min_cubes(game: Game) -> Hand:
    hands = game[1]
    red_cubes = max(hand["red"] for hand in hands)
    green_cubes = max(hand["green"] for hand in hands)
    blue_cubes = max(hand["blue"] for hand in hands)
    return {"red": red_cubes, "green": green_cubes, "blue": blue_cubes}


def get_hand_power(hand: Hand) -> int:
    return hand["red"] * hand["green"] * hand["blue"]


data_path = Path(__file__).with_name("prompt.txt")
file_text = data_path.read_text()
games = get_games(file_text)
valid_game_ids = [game[0] for game in games if is_game_valid(game)]
sum_of__valid_ids = reduce(lambda acc, game_id: acc + game_id, valid_game_ids, 0)
print(f"Sum of valid ids {sum_of__valid_ids}")

min_cubes_hands = [get_min_cubes(game) for game in games]
powers_of_min_hands = [get_hand_power(hand) for hand in min_cubes_hands]
sum_of_powers = sum(powers_of_min_hands)
print(f"Sum of cube powers {sum_of_powers}")
