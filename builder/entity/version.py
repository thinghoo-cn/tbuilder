from dataclasses import dataclass


@dataclass
class Version:
    x: int
    y: int
    z: int

    def get_full(self, split=".") -> str:
        return f"v{self.x}{split}{self.y}{split}{self.z}"
