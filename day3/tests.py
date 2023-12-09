from io import StringIO
from unittest import TestCase

from .parser import get_schematic_from_input
from .schematic import DataType, Element, Line, Schematic


class ParserTestCase(TestCase):
    def test_get_schematic_from_input(self):
        input_data = StringIO("""467..114.
...*.....
..35..633
......#..
617*.....
.....+.58
..592....
......755
...$.*...
.664.598.""")
        expected = Schematic(
            lines=[
                Line(
                    elements=[
                        Element(start=0, value="467"),
                        Element(start=5, value="114"),
                    ]
                ),
                Line(
                    elements=[
                        Element(start=3, value="*"),
                    ]
                ),
                Line(
                    elements=[
                        Element(start=2, value="35"),
                        Element(start=6, value="633"),
                    ]
                ),
                Line(
                    elements=[
                        Element(start=6, value="#"),
                    ]
                ),
                Line(
                    elements=[
                        Element(start=0, value="617"),
                        Element(start=3, value="*"),
                    ]
                ),
                Line(
                    elements=[
                        Element(start=5, value="+"),
                        Element(start=7, value="58"),
                    ]
                ),
                Line(
                    elements=[
                        Element(start=2, value="592"),
                    ]
                ),
                Line(
                    elements=[
                        Element(start=6, value="755"),
                    ]
                ),
                Line(
                    elements=[
                        Element(start=3, value="$"),
                        Element(start=5, value="*"),
                    ]
                ),
                Line(
                    elements=[
                        Element(start=1, value="664"),
                        Element(start=5, value="598"),
                    ]
                )
            ]
        )
        actual = get_schematic_from_input(input_data)
        self.assertEqual(len(expected.lines), len(actual.lines))
        for line_number, line in enumerate(expected.lines):
            self.assertEqual(
                line, actual.lines[line_number], msg=f"Expectation failed at line {line_number + 1}"
            )


class ElementTestCase(TestCase):
    def test_data_type(self):
        self.assertIs(
            Element(start=0, value="123").data_type,
            DataType.NUMBER
        )
        self.assertIs(
            Element(start=0, value="$1").data_type,
            DataType.SYMBOL,
        )

    def test_range(self):
        element = Element(start=2, value="123")
        self.assertEqual(element.range.start, 2)
        self.assertEqual(element.range.stop, 5)


class LineTestCase(TestCase):
    def test_get_elements_in_range(self):
        line = Line(
            elements=[
                Element(start=2, value="123"),
                Element(start=6, value="90"),
                Element(start=10, value="$"),
            ]
        )
        self.assertEqual(
            line.get_elements_in_range(range(0, 1)),
            []
        )
        self.assertEqual(
            line.get_elements_in_range(range(1, 3)),
            [Element(start=2, value="123")]
        )
        self.assertEqual(
            line.get_elements_in_range(range(4, 7)),
            [
                Element(start=2, value="123"),
                Element(start=6, value="90"),
            ]
        )
        self.assertEqual(
            line.get_elements_in_range(range(6, 11)),
            [
                Element(start=6, value="90"),
                Element(start=10, value="$"),
            ]
        )
        self.assertEqual(
            line.get_elements_in_range(range(10, 11)),
            [Element(start=10, value="$")]
        )
        self.assertEqual(
            line.get_elements_in_range(range(10, 20)),
            [Element(start=10, value="$")]
        )
        self.assertEqual(
            line.get_elements_in_range(range(20, 100)),
            []
        )

    def test_get_elements_in_range_2(self):
        line = Line(
            elements=[
                Element(start=0, value="617"),
                Element(start=3, value="*"),
                Element(start=4, value="23")
            ]
        )
        self.assertEqual(
            line.get_elements_in_range(range(2, 4)),
            [
                Element(start=0, value="617"),
                Element(start=3, value="*")
            ]
        )

    def test_get_data_types_in_range(self):
        line = Line(
            elements=[
                Element(start=2, value="123"),
                Element(start=6, value="90"),
                Element(start=10, value="$"),
            ]
        )
        self.assertEqual(
            line.get_data_types_in_range(range(0, 1)),
            set()
        )
        self.assertEqual(
            line.get_data_types_in_range(range(1, 3)),
            {DataType.NUMBER}
        )
        self.assertEqual(
            line.get_data_types_in_range(range(4, 7)),
            {DataType.NUMBER}
        )
        self.assertEqual(
            line.get_data_types_in_range(range(6, 11)),
            {DataType.NUMBER, DataType.SYMBOL}
        ),
        self.assertEqual(
            line.get_data_types_in_range(range(10, 11)),
            {DataType.SYMBOL}
        )
        self.assertEqual(
            line.get_data_types_in_range(range(10, 20)),
            {DataType.SYMBOL}
        )
        self.assertEqual(
            line.get_data_types_in_range(range(20, 100)),
            set()
        )


class SchematicTestCase(TestCase):
    def setUp(self):
        self.schematic = get_schematic_from_input(StringIO("""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""))

    def test_get_part_numbers(self):
        self.assertEqual(
            list(self.schematic.get_part_numbers()),
            [
                467,
                35,
                633,
                617,
                592,
                755,
                664,
                598,
            ]
        )

    def test_get_gear_ratios(self):
        self.assertEqual(
            list(self.schematic.get_gear_ratios()),
            [
                16345,
                451490,
            ]
        )

    def test_get_gear_ratios_2(self):
        schematic = get_schematic_from_input(StringIO("""467..114..
...*......
..35..633.
......#...
617*23....
...*.+.58.
..592.....
......755.
...$.*....
.664.598.."""))
        self.assertEqual(
            list(schematic.get_gear_ratios()),
            [
                16345,
                617 * 23,
                451490,
            ]
        )
        schematic = get_schematic_from_input(StringIO("""467..114..
...*......
..35..633.
......#...
617*23....
..*..+.58.
..592.....
......755.
...$.*....
.664.598..
*123..11..
........*2
..........
.950.218.$...
.......*.328.
....254......"""))
        self.assertEqual(
            list(schematic.get_gear_ratios()),
            [
                16345,
                617 * 23,
                617 * 592,
                451490,
                664 * 123,
                11 * 2,
                218 * 254,
            ]
        )
