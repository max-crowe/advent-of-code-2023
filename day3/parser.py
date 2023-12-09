from io import TextIOBase

from .schematic import Element, Line, Schematic


def get_schematic_from_input(input_data: TextIOBase) -> Schematic:
    parsed_lines: list[Line] = []
    for line in input_data:
        parsed_elements: list[Element] = []
        current_value: str | None = None
        current_value_start: int = 0
        for pos, char in enumerate(line.strip()):
            if char == ".":
                if current_value:
                    parsed_elements.append(
                        Element(value=current_value, start=current_value_start)
                    )
                    current_value = None
            else:
                if not current_value or char.isdigit() != current_value[-1].isdigit():
                    if current_value:
                        parsed_elements.append(
                            Element(value=current_value, start=current_value_start)
                        )
                    current_value = ""
                    current_value_start = pos
                current_value += char
        if current_value:
            parsed_elements.append(
                Element(value=current_value, start=current_value_start)
            )
        parsed_lines.append(Line(elements=parsed_elements))
    return Schematic(lines=parsed_lines)
