from functools import reduce
import re
from typing import Iterable, TypeAlias, TypedDict
from pathlib import Path

Hand = TypedDict("Hand", {"red": int, "green": int, "blue": int})
Game: TypeAlias = tuple[int, list[Hand]]


MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

MAX_CUBES = MAX_RED + MAX_GREEN + MAX_BLUE


def get_hand_details(hand: str) -> Hand:
    red_search = re.search(r"([0-9]+) r", hand)
    green_search = re.search(r"([0-9]+) g", hand)
    blue_search = re.search(r"([0-9]+) b", hand)

    red = red_search.group(1) if red_search else 0
    green = green_search.group(1) if green_search else 0
    blue = blue_search.group(1) if blue_search else 0

    return {"red": int(red), "green": int(green), "blue": int(blue)}


def get_game_details(input: str) -> Game:
    game_number = re.search(r"([0-9]+):", input)
    assert game_number is not None
    game_result = re.search(r": (.*)", input)
    assert game_result is not None
    all_hands: str = game_result.group(1)
    individual_hands = all_hands.split(";")
    hand_details = map(get_hand_details, individual_hands)
    return (int(game_number.group(1)), list(hand_details))


def get_games(input: str) -> Iterable[Game]:
    game_lines: list[str] = input.splitlines()
    game_details = map(get_game_details, game_lines)
    return game_details


def hand_is_valid(hand: Hand) -> bool:
    if hand["red"] > MAX_RED:
        return False
    if hand["green"] > MAX_RED:
        return False
    if hand["blue"] > MAX_BLUE:
        return False
    if (hand["red"] + hand["green"] + hand["blue"]) > MAX_CUBES:
        return False
    return True


def is_game_valid(game: Game) -> bool:
    return all(hand_is_valid(hand) for hand in game[1])


data_path = Path(__file__).with_name("test.txt")
file_text = data_path.read_text()
games = get_games(file_text)
valid_games = filter(is_game_valid, games)
sum_of_ids = reduce(lambda acc, next_game: acc + next_game[0], valid_games, 0)

print(sum_of_ids)
