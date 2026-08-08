from __future__ import annotations

from dataclasses import dataclass, field


VALID_SIDES = frozenset({"left", "right", "both"})
VALID_TERMINAL_TYPES = frozenset({"feedthrough", "ground", "fused", "disconnect", "shield"})


@dataclass(frozen=True)
class Terminal:
    tag: str
    label: str
    side: str = "left"
    terminal_type: str = "feedthrough"
    bridge: str = ""
    wire: str = ""

    def __post_init__(self) -> None:
        tag = self.tag.strip()
        label = self.label.strip()
        side = self.side.strip().lower()
        terminal_type = self.terminal_type.strip().lower()

        if not tag:
            raise ValueError("terminal tag is required")
        if not label:
            raise ValueError("terminal label is required")
        if side not in VALID_SIDES:
            raise ValueError(f"terminal side must be one of: {', '.join(sorted(VALID_SIDES))}")
        if terminal_type not in VALID_TERMINAL_TYPES:
            raise ValueError(
                f"terminal type must be one of: {', '.join(sorted(VALID_TERMINAL_TYPES))}"
            )

        object.__setattr__(self, "tag", tag)
        object.__setattr__(self, "label", label)
        object.__setattr__(self, "side", side)
        object.__setattr__(self, "terminal_type", terminal_type)
        object.__setattr__(self, "bridge", self.bridge.strip())
        object.__setattr__(self, "wire", self.wire.strip())


@dataclass
class TerminalBlock:
    name: str
    terminals: list[Terminal] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("terminal block name is required")

    def add_terminal(self, terminal: Terminal) -> None:
        self.terminals.append(terminal)

    def next_tag(self, prefix: str = "X1") -> str:
        return f"{prefix}:{len(self.terminals) + 1}"

    @classmethod
    def from_rows(cls, name: str, rows: list[dict[str, str]]) -> "TerminalBlock":
        block = cls(name=name)
        for row in rows:
            block.add_terminal(
                Terminal(
                    tag=row.get("tag", ""),
                    label=row.get("label", ""),
                    side=row.get("side", "left"),
                    terminal_type=row.get("terminal_type", row.get("type", "feedthrough")),
                    bridge=row.get("bridge", ""),
                    wire=row.get("wire", ""),
                )
            )
        return block
