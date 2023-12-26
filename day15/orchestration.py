from dataclasses import dataclass, field

from .hashing import get_hash


@dataclass
class Lens:
    label: str
    focal_length: int


@dataclass
class Box:
    lenses: list[Lens] = field(default_factory=list)

    def find_index(self, label: str) -> int | None:
        matches = list(
            filter(lambda pair: pair[1].label == label, enumerate(self.lenses))
        )
        assert len(matches) <= 1
        if matches:
            return matches[0][0]

    def remove_lens(self, label: str):
        index = self.find_index(label)
        if index is not None:
            self.lenses.pop(index)

    def insert_lens(self, lens: Lens):
        index = self.find_index(lens.label)
        if index is None:
            self.lenses.append(lens)
        else:
            self.lenses[index] = lens


@dataclass
class BoxOrchestrator:
    boxes: dict[int, Box] = field(default_factory=dict)

    def __getitem__(self, key: int) -> Box:
        try:
            box = self.boxes[key]
        except KeyError:
            box = self.boxes[key] = Box()
        return box

    def handle_step(self, step: str):
        if step[-1] == "-":
            step = step.rstrip("-")
            self[get_hash(step)].remove_lens(step)
        else:
            label, _, focal_length = step.partition("=")
            self[get_hash(label)].insert_lens(Lens(label=label, focal_length=int(focal_length)))

    def get_focal_power(self) -> int:
        power = 0
        for box_number, box in self.boxes.items():
            for i, lens in enumerate(box.lenses, 1):
                power += (box_number + 1) * lens.focal_length * i
        return power
