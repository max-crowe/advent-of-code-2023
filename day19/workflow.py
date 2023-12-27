import operator
from dataclasses import dataclass
from enum import StrEnum

OPERATORS = {
    "<": operator.lt,
    ">": operator.gt,
}


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def __int__(self) -> int:
        return self.x + self.m + self.a + self.s


class Result(StrEnum):
    ACCEPTED = "A"
    REJECTED = "R"


class Rule:
    def __init__(
        self,
        orchestrator: "Orchestrator",
        parameter: str,
        operator_symbol: str,
        threshold: int,
        target: str
    ):
        self.orchestrator = orchestrator
        self.operator = OPERATORS[operator_symbol]
        self.parameter = parameter
        self.threshold = threshold
        self.target = target

    def __call__(self, part: Part) -> bool:
        return self.operator(getattr(part, self.parameter), self.threshold)

    @property
    def resolved_target(self) -> "Workflow | Result":
        try:
            return Result(self.target)
        except ValueError:
            return self.orchestrator[self.target]


@dataclass
class Workflow:
    orchestrator: "Orchestrator"
    rules: list[Rule]
    fallback: str

    def __call__(self, part: Part) -> Result:
        for rule in self.rules:
            if rule(part):
                result = rule.resolved_target
                if isinstance(result, Result):
                    return result
                return result(part)
        fallback = self.resolved_fallback
        if isinstance(fallback, Result):
            return fallback
        return fallback(part)

    @property
    def resolved_fallback(self) -> "Result | Workflow":
        try:
            return Result(self.fallback)
        except ValueError:
            return self.orchestrator[self.fallback]


class Orchestrator:
    def __init__(self):
        self.workflows: dict[str, Workflow] = {}

    def __getitem__(self, item: str) -> Workflow:
        return self.workflows[item]

    def __setitem__(self, key: str, value: Workflow):
        self.workflows[key] = value

    def add_workflow(self, name: str, fallback: str, *rule_args: tuple[str, str, int, str]):
        rules = [Rule(self, *args) for args in rule_args]
        self[name] = Workflow(self, rules, fallback)

    @property
    def entry_workflow(self) -> Workflow:
        return self["in"]
