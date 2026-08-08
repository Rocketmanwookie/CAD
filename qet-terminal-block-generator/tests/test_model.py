import pytest

from qet_tb_generator.model import Terminal, TerminalBlock


def test_terminal_normalizes_values():
    terminal = Terminal(" X1:1 ", " 24VDC ", "LEFT", "FeedThrough", " BR1 ", " 1001 ")

    assert terminal.tag == "X1:1"
    assert terminal.label == "24VDC"
    assert terminal.side == "left"
    assert terminal.terminal_type == "feedthrough"
    assert terminal.bridge == "BR1"
    assert terminal.wire == "1001"


def test_terminal_requires_known_side_and_type():
    with pytest.raises(ValueError, match="terminal side"):
        Terminal("X1:1", "24VDC", side="top")

    with pytest.raises(ValueError, match="terminal type"):
        Terminal("X1:1", "24VDC", terminal_type="magic")


def test_terminal_block_next_tag_counts_existing_terminals():
    block = TerminalBlock(" TB1 ", [Terminal("X1:1", "24VDC")])

    assert block.name == "TB1"
    assert block.next_tag("X1") == "X1:2"
