from functools import reduce
import re
from typing import Iterable, TypeAlias
from pyparsing import Path


Game: TypeAlias = tuple[int, dict[str, int]]


MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

MAX_CUBES = MAX_RED + MAX_GREEN + MAX_BLUE


def get_game_details(input: str) -> Game:
    game_number = re.search(r"([0-9]+):", input)
    assert game_number is not None
    game_result = re.search(r": (.*)", input)
    assert game_result is not None
    all_hands: str = game_result.group(1)
    individual_hands = all_hands.split(";")
    return  # todo


def get_games(input: str) -> Iterable[Game]:
    game_lines: list[str] = input.splitlines()
    game_details = map(get_game_details, game_lines)
    return game_details


def is_game_valid(input: Game) -> bool:
    return True


data_path = Path(__file__).with_name("test.txt")
file_text = data_path.read_text()
games = get_games(file_text)
valid_games = filter(is_game_valid, games)
sum_of_ids = reduce(lambda acc, next_game: acc + next_game[0], valid_games, 0)

print(sum_of_ids)
