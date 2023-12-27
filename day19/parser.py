import re
from io import TextIOBase

from .workflow import Orchestrator, Part


def get_orchestrator_and_part_list_from_input_data(input_data: TextIOBase) -> tuple[Orchestrator, list[Part]]:
    orchestrator = Orchestrator()
    parts: list[Part] = []
    process_parts = False
    for line in input_data:
        if not line.strip():
            process_parts = True
            continue
        if process_parts:
            part_args: dict[str, int] = {}
            for part_arg_str in line.strip().lstrip("{").rstrip("}").split(","):
                param, _, value = part_arg_str.partition("=")
                part_args[param] = int(value)
            parts.append(Part(**part_args))
        else:
            match = re.match("^([a-z]+){([^}]*)}", line.strip())
            assert match is not None
            workflow_name = match.group(1)
            rule_args: list[tuple[str, str, int, str]] = []
            rule_strs = match.group(2).split(",")
            fallback = rule_strs.pop(-1)
            for rule_str in rule_strs:
                match = re.match("^([xmas])(<|>)(\d+):([a-zA-Z]+)$", rule_str)
                assert match is not None
                rule_args.append((match.group(1), match.group(2), int(match.group(3)), match.group(4)))
            orchestrator.add_workflow(workflow_name, fallback, *rule_args)
    return orchestrator, parts
