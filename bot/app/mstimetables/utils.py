import re


async def parse_classroom(input_str):
    match = re.match(r'(\d+)\s*\((\d+)к\)?', input_str)
    if match:
        classroom = int(match.group(1))
        building = int(match.group(2))
    else:
        classroom = int(input_str)
        building = 1
    return classroom, building
