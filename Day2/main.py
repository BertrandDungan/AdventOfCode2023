from re import findall
from pyparsing import Path

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

MAX_CUBES = MAX_RED + MAX_GREEN + MAX_BLUE


def get_game_details(input: str) -> any:
    game_number = 
    return


def get_games(input: str) -> list[tuple[str, str]]:
    game_lines: list[str] = input.split('\n')
    game_details = map(get_game_details, game_lines)
    return game_details


data_path = Path(__file__).with_name("test.txt")
file_text = data_path.read_text()
games = get_games(file_text)

print(file_text)
