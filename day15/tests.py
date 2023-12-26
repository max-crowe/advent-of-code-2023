from io import StringIO
from unittest import TestCase

from .hashing import get_hash
from .orchestration import Box, BoxOrchestrator, Lens
from .parser import get_values_from_input_data


class HashTestCase(TestCase):
    def test_hashing(self):
        self.assertEqual(get_hash("HASH"), 52)
        self.assertEqual(get_hash("rn=1"), 30)
        self.assertEqual(get_hash("cm-"), 253)


class ParserTestCase(TestCase):
    def test_parser(self):
        input_data = StringIO("""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
""")
        values = get_values_from_input_data(input_data)
        self.assertEqual(
            values,
            [
                "rn=1",
                "cm-",
                "qp=3",
                "cm=2",
                "qp-",
                "pc=4",
                "ot=9",
                "ab=5",
                "pc-",
                "pc=6",
                "ot=7"
            ]
        )
        self.assertEqual(sum(get_hash(value) for value in values), 1320)


class OrchestrationTestCase(TestCase):
    def test_orchestration(self):
        orchestrator = BoxOrchestrator()
        orchestrator.handle_step("rn=1")
        self.assertEqual(
            orchestrator.boxes,
            {
                0: Box(lenses=[Lens(label="rn", focal_length=1)])
            }
        )
        orchestrator.handle_step("cm-")
        self.assertEqual(
            orchestrator.boxes,
            {
                0: Box(lenses=[Lens(label="rn", focal_length=1)])
            }
        )
        orchestrator.handle_step("qp=3")
        self.assertEqual(
            orchestrator.boxes,
            {
                0: Box(lenses=[Lens(label="rn", focal_length=1)]),
                1: Box(lenses=[Lens(label="qp", focal_length=3)])
            }
        )
        orchestrator.handle_step("cm=2")
        self.assertEqual(
            orchestrator.boxes,
            {
                0: Box(lenses=[Lens(label="rn", focal_length=1), Lens(label="cm", focal_length=2)]),
                1: Box(lenses=[Lens(label="qp", focal_length=3)])
            }
        )
        orchestrator.handle_step("qp-")
        self.assertEqual(
            orchestrator.boxes,
            {
                0: Box(lenses=[Lens(label="rn", focal_length=1), Lens(label="cm", focal_length=2)]),
                1: Box(),
            }
        )
        orchestrator.handle_step("pc=4")
        self.assertEqual(
            orchestrator.boxes,
            {
                0: Box(lenses=[Lens(label="rn", focal_length=1), Lens(label="cm", focal_length=2)]),
                1: Box(),
                3: Box(lenses=[Lens(label="pc", focal_length=4)])
            }
        )
        orchestrator.handle_step("ot=9")
        self.assertEqual(
            orchestrator.boxes,
            {
                0: Box(lenses=[Lens(label="rn", focal_length=1), Lens(label="cm", focal_length=2)]),
                1: Box(),
                3: Box(lenses=[Lens(label="pc", focal_length=4), Lens(label="ot", focal_length=9)])
            }
        )
        orchestrator.handle_step("ab=5")
        self.assertEqual(
            orchestrator.boxes,
            {
                0: Box(lenses=[Lens(label="rn", focal_length=1), Lens(label="cm", focal_length=2)]),
                1: Box(),
                3: Box(lenses=[
                    Lens(label="pc", focal_length=4),
                    Lens(label="ot", focal_length=9),
                    Lens(label="ab", focal_length=5)
                ])
            }
        )
        orchestrator.handle_step("pc-")
        self.assertEqual(
            orchestrator.boxes,
            {
                0: Box(lenses=[Lens(label="rn", focal_length=1), Lens(label="cm", focal_length=2)]),
                1: Box(),
                3: Box(lenses=[Lens(label="ot", focal_length=9), Lens(label="ab", focal_length=5)])
            }
        )
        orchestrator.handle_step("pc=6")
        self.assertEqual(
            orchestrator.boxes,
            {
                0: Box(lenses=[Lens(label="rn", focal_length=1), Lens(label="cm", focal_length=2)]),
                1: Box(),
                3: Box(lenses=[
                    Lens(label="ot", focal_length=9),
                    Lens(label="ab", focal_length=5),
                    Lens(label="pc", focal_length=6)
                ])
            }
        )
        orchestrator.handle_step("ot=7")
        self.assertEqual(
            orchestrator.boxes,
            {
                0: Box(lenses=[Lens(label="rn", focal_length=1), Lens(label="cm", focal_length=2)]),
                1: Box(),
                3: Box(lenses=[
                    Lens(label="ot", focal_length=7),
                    Lens(label="ab", focal_length=5),
                    Lens(label="pc", focal_length=6)
                ])
            }
        )
        self.assertEqual(orchestrator.get_focal_power(), 145)
