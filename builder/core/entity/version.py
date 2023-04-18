from dataclasses import dataclass


@dataclass
class Version:
    x: int
    y: int
    z: int
    date: int

    @classmethod
    def parse_str(cls, content: str) -> "Version":
        start = 0
        v = []
        for i in range(len(content)):
            if content[i] == ".":
                v.append(int(content[start:i]))
                start = i + 1

        v.append(int(content[start:]))
        assert len(v) == 4, v
        return Version(v[0], v[1], v[2], v[3])

    def get_full(self, split=".") -> str:
        return f"v{self.x}{split}{self.y}{split}{self.z}{split}{self.date}"
