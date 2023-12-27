from io import StringIO
from unittest import TestCase

from .parser import get_orchestrator_and_part_list_from_input_data
from .workflow import Orchestrator, Part, Result


class WorkflowTestCase(TestCase):
    def setUp(self):
        self.orchestrator = Orchestrator()
        self.orchestrator.add_workflow(
            "px", "rfg", ("a", "<", 2006, "qkq"), ("m", ">", 2090, "A")
        )
        self.orchestrator.add_workflow(
            "pv", "A", ("a", ">", 1716, "R")
        )
        self.orchestrator.add_workflow(
            "lnx", "A", ("m", ">", 1548, "A")
        )
        self.orchestrator.add_workflow(
            "rfg", "A", ("s", "<", 537, "gd"), ("x", ">", 2440, "R")
        )
        self.orchestrator.add_workflow(
            "qs", "lnx", ("s", ">", 3448, "A")
        )
        self.orchestrator.add_workflow(
            "qkq", "crn", ("x", "<", 1416, "A")
        )
        self.orchestrator.add_workflow(
            "crn", "R", ("x", ">", 2662, "A")
        )
        self.orchestrator.add_workflow(
            "in", "qqz", ("s", "<", 1351, "px")
        )
        self.orchestrator.add_workflow(
            "qqz", "R", ("s", ">", 2770, "qs"), ("m", "<", 1801, "hdj")
        )
        self.orchestrator.add_workflow(
            "gd", "R", ("a", ">", 3333, "R")
        )
        self.orchestrator.add_workflow(
            "hdj", "pv", ("m", ">", 838, "A")
        )

    def test_call_rule(self):
        part = Part(x=787, m=2655, a=1222, s=2876)
        self.assertFalse(self.orchestrator["gd"].rules[0](part))
        self.assertTrue(self.orchestrator["hdj"].rules[0](part))

    def test_rule_target_resolution(self):
        self.assertIs(self.orchestrator["gd"].rules[0].resolved_target, Result.REJECTED)
        self.assertIs(self.orchestrator["qqz"].rules[0].resolved_target, self.orchestrator["qs"])

    def test_workflow_target_resolution(self):
        self.assertIs(self.orchestrator["hdj"].resolved_fallback, self.orchestrator["pv"])
        self.assertIs(self.orchestrator["rfg"].resolved_fallback, Result.ACCEPTED)

    def test_workflow_orchestration(self):
        self.assertIs(
            self.orchestrator.entry_workflow(Part(x=787, m=2655, a=1222, s=2876)),
            Result.ACCEPTED
        )
        self.assertIs(
            self.orchestrator.entry_workflow(Part(x=1679, m=44, a=2067, s=496)),
            Result.REJECTED
        )
        self.assertIs(
            self.orchestrator.entry_workflow(Part(x=2036, m=264, a=79, s=2244)),
            Result.ACCEPTED
        )
        self.assertIs(
            self.orchestrator.entry_workflow(Part(x=2461, m=1339, a=466, s=291)),
            Result.REJECTED
        )
        self.assertIs(
            self.orchestrator.entry_workflow(Part(x=2127, m=1623, a=2188, s=1013)),
            Result.ACCEPTED
        )


class ParserTestCase(TestCase):
    def test_parser(self):
        input_data = StringIO("""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""")
        orchestrator, parts = get_orchestrator_and_part_list_from_input_data(input_data)
        self.assertEqual(len(parts), 5)
        self.assertEqual(len(orchestrator.workflows), 11)
        self.assertEqual(
            sum(int(part) for part in parts if orchestrator.entry_workflow(part) is Result.ACCEPTED),
            19114
        )
