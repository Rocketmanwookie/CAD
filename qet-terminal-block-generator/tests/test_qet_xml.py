from qet_tb_generator.model import Terminal, TerminalBlock
from qet_tb_generator.qet_xml import block_from_xml, block_to_xml, read_block, write_block


def test_block_xml_round_trip_preserves_terminal_data():
    block = TerminalBlock(
        "TB1",
        [
            Terminal("X1:1", "24VDC", bridge="BR1", wire="1001"),
            Terminal("X1:2", "0VDC", side="right", terminal_type="ground", wire="1002"),
        ],
    )

    loaded = block_from_xml(block_to_xml(block))

    assert loaded.name == "TB1"
    assert loaded.terminals == block.terminals


def test_write_and_read_block(tmp_path):
    path = tmp_path / "tb1.xml"
    block = TerminalBlock("TB1", [Terminal("X1:1", "24VDC")])

    write_block(path, block)

    assert read_block(path).terminals[0].tag == "X1:1"
    assert "terminal_block_project" in path.read_text(encoding="utf-8")
