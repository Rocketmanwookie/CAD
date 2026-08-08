from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree

from qet_tb_generator.model import Terminal, TerminalBlock


SCHEMA_VERSION = "0.1"


def block_to_element(block: TerminalBlock) -> ElementTree.Element:
    root = ElementTree.Element(
        "terminal_block_project",
        {
            "generator": "qet_tb_generator",
            "schema_version": SCHEMA_VERSION,
        },
    )
    block_element = ElementTree.SubElement(root, "terminal_block", {"name": block.name})
    for index, terminal in enumerate(block.terminals, start=1):
        ElementTree.SubElement(
            block_element,
            "terminal",
            {
                "index": str(index),
                "tag": terminal.tag,
                "label": terminal.label,
                "side": terminal.side,
                "type": terminal.terminal_type,
                "bridge": terminal.bridge,
                "wire": terminal.wire,
            },
        )
    return root


def block_to_xml(block: TerminalBlock) -> str:
    root = block_to_element(block)
    ElementTree.indent(root, space="  ")
    return ElementTree.tostring(root, encoding="unicode", xml_declaration=True)


def block_from_xml(xml_text: str | bytes) -> TerminalBlock:
    root = ElementTree.fromstring(xml_text)
    if root.tag != "terminal_block_project":
        raise ValueError("expected terminal_block_project XML root")

    block_element = root.find("terminal_block")
    if block_element is None:
        raise ValueError("terminal_block element is required")

    block = TerminalBlock(name=block_element.get("name", "TB1"))
    for terminal_element in block_element.findall("terminal"):
        block.add_terminal(
            Terminal(
                tag=terminal_element.get("tag", ""),
                label=terminal_element.get("label", ""),
                side=terminal_element.get("side", "left"),
                terminal_type=terminal_element.get("type", "feedthrough"),
                bridge=terminal_element.get("bridge", ""),
                wire=terminal_element.get("wire", ""),
            )
        )
    return block


def write_block(path: str | Path, block: TerminalBlock) -> Path:
    output_path = Path(path)
    output_path.write_text(block_to_xml(block), encoding="utf-8")
    return output_path


def read_block(path: str | Path) -> TerminalBlock:
    return block_from_xml(Path(path).read_text(encoding="utf-8"))
