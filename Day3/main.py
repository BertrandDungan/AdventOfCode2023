from pathlib import Path


def is_part(char: str) -> bool:
    return char != "." and not char.isdigit()


def is_gear(char: str) -> bool:
    return char == "*"


def get_number(number_buffer: list[str]) -> int:
    return int("".join(number_buffer))


def check_for_parts(
    file_lines: list[str], line_index: int, character_index: int
) -> bool:
    if line_index > 0:
        char_n = file_lines[line_index - 1][character_index]
        if is_part(char_n):
            return True
        if character_index > 0:
            char_nw = file_lines[line_index - 1][character_index - 1]
            if is_part(char_nw):
                return True
        if character_index < line_length - 1:
            char_ne = file_lines[line_index - 1][character_index + 1]
            if is_part(char_ne):
                return True
    if line_index < max_lines - 1:
        char_s = file_lines[line_index + 1][character_index]
        if is_part(char_s):
            return True
        if character_index > 0:
            char_sw = file_lines[line_index + 1][character_index - 1]
            if is_part(char_sw):
                return True
        if character_index < line_length - 1:
            char_se = file_lines[line_index + 1][character_index + 1]
            if is_part(char_se):
                return True
    return False


def get_gear_identifier(line_index: int, character_index: int) -> str:
    return f"{line_index},{character_index}"


def check_for_gear_parts(
    file_lines: list[str], line_index: int, character_index: int
) -> tuple[bool, str]:
    if line_index > 0:
        char_n = file_lines[line_index - 1][character_index]
        if is_gear(char_n):
            return (True, get_gear_identifier(line_index, character_index - 1))
        if character_index > 0:
            char_nw = file_lines[line_index - 1][character_index - 1]
            if is_gear(char_nw):
                return (True, get_gear_identifier(line_index - 1, character_index - 1))
        if character_index < line_length - 1:
            char_ne = file_lines[line_index - 1][character_index + 1]
            if is_gear(char_ne):
                return (True, get_gear_identifier(line_index - 1, character_index + 1))
    if line_index < max_lines - 1:
        char_s = file_lines[line_index + 1][character_index]
        if is_gear(char_s):
            return (True, get_gear_identifier(line_index + 1, character_index))
        if character_index > 0:
            char_sw = file_lines[line_index + 1][character_index - 1]
            if is_gear(char_sw):
                return (True, get_gear_identifier(line_index + 1, character_index - 1))
        if character_index < line_length - 1:
            char_se = file_lines[line_index + 1][character_index + 1]
            if is_gear(char_se):
                return (True, get_gear_identifier(line_index + 1, character_index + 1))
    return (False, "")


data_path = Path(__file__).with_name("test.txt")
file_text = data_path.read_text()
file_lines = file_text.splitlines()
max_lines = len(file_lines)
line_length = len(file_lines[0])

part_sum = 0
gear_tracker: dict[str, list[int]] = {}
for line_index, line in enumerate(file_lines):
    number_buffer: list[str] = []
    is_part_number = False
    is_gear_part = False
    gear_position = ""

    for character_index, character in enumerate(line):
        if character == ".":
            if is_part_number and len(number_buffer) > 0:
                part_number = get_number(number_buffer)
                part_sum += part_number
                if is_gear_part:
                    current_value = gear_tracker.get(gear_position)
                    if current_value is None:
                        gear_tracker[gear_position] = [part_number]
                    else:
                        gear_tracker[gear_position].append(part_number)
            is_part_number = False
            is_gear_part = False
            number_buffer = []
        elif character.isdigit():
            number_buffer.append(character)
            if is_part_number is not True:
                is_part_number = check_for_parts(
                    file_lines, line_index, character_index
                )
                is_gear_part, gear_position = check_for_gear_parts(
                    file_lines, line_index, character_index
                )

        else:
            is_part_number = True
            if character == "*":
                is_gear_part = True
                gear_position = get_gear_identifier(line_index, character_index)
            if len(number_buffer) > 0:
                part_number = get_number(number_buffer)
                part_sum += part_number
                if is_gear_part:
                    current_value = gear_tracker.get(gear_position)
                    if current_value is None:
                        gear_tracker[gear_position] = [part_number]
                    else:
                        gear_tracker[gear_position].append(part_number)
                number_buffer = []

    if is_part_number and len(number_buffer) > 0:
        part_number = get_number(number_buffer)
        part_sum += part_number
        if is_gear_part:
            current_value = gear_tracker.get(gear_position)
            if current_value is None:
                gear_tracker[gear_position] = [part_number]
            else:
                gear_tracker[gear_position].append(part_number)

print(part_sum)

gear_ratios = [gear[0] * gear[1] for gear in gear_tracker.values() if len(gear) == 2]
gear_ratio_sum = sum(gear_ratios)

print(gear_ratio_sum)
