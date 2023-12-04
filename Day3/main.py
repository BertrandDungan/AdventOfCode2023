from pathlib import Path


def is_part(char: str) -> bool:
    return char != "." and not char.isdigit()


data_path = Path(__file__).with_name("prompt.txt")
file_text = data_path.read_text()
file_lines = file_text.splitlines()
max_lines = len(file_lines)
line_length = len(file_lines[0])

part_sum = 0
for line_index, line in enumerate(file_lines):
    current_number: list[str] = []
    is_part_number = False
    for character_index, character in enumerate(line):
        if character == ".":
            if is_part_number and len(current_number) > 0:
                full_number = "".join(current_number)
                part_sum += int(full_number)
            is_part_number = False
            current_number = []
        elif character.isdigit():
            current_number.append(character)
            if line_index > 0:
                char_n = file_lines[line_index - 1][character_index]
                if is_part(char_n):
                    is_part_number = True
                if character_index > 0:
                    char_nw = file_lines[line_index - 1][character_index - 1]
                    if is_part(char_nw):
                        is_part_number = True
                if character_index < line_length - 1:
                    char_ne = file_lines[line_index - 1][character_index + 1]
                    if is_part(char_ne):
                        is_part_number = True
            if line_index < max_lines - 1:
                char_s = file_lines[line_index + 1][character_index]
                if is_part(char_s):
                    is_part_number = True
                if character_index > 0:
                    char_sw = file_lines[line_index + 1][character_index - 1]
                    if is_part(char_sw):
                        is_part_number = True
                if character_index < line_length - 1:
                    char_se = file_lines[line_index + 1][character_index + 1]
                    if is_part(char_se):
                        is_part_number = True
        else:
            is_part_number = True

    if is_part_number and len(current_number) > 0:
        full_number = "".join(current_number)
        part_sum += int(full_number)

print(part_sum)
