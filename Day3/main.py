from pathlib import Path


def is_part(char: str) -> bool:
    return char != "." and not char.isdigit()


def get_number(number_buffer: list[str]) -> int:
    return int("".join(number_buffer))


def check_for_parts(file_lines, line_index, character_index) -> bool:
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


data_path = Path(__file__).with_name("prompt.txt")
file_text = data_path.read_text()
file_lines = file_text.splitlines()
max_lines = len(file_lines)
line_length = len(file_lines[0])

part_sum = 0
for line_index, line in enumerate(file_lines):
    number_buffer: list[str] = []
    is_part_number = False
    for character_index, character in enumerate(line):
        if character == ".":
            if is_part_number and len(number_buffer) > 0:
                part_sum += get_number(number_buffer)
            is_part_number = False
            number_buffer = []
        elif character.isdigit():
            number_buffer.append(character)
            if is_part_number is not True:
                is_part_number = check_for_parts(
                    file_lines, line_index, character_index
                )

        else:
            is_part_number = True
            if len(number_buffer) > 0:
                part_sum += get_number(number_buffer)
                number_buffer = []

    if is_part_number and len(number_buffer) > 0:
        part_sum += get_number(number_buffer)

print(part_sum)
