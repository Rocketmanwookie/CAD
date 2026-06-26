# SPDX-License-Identifier: MIT

from types import SimpleNamespace

from controls_wb.commands.export_bom import collect_bom_rows


def test_collect_bom_rows_uses_controls_metadata():
    objects = [
        SimpleNamespace(
            Tag="CP-001",
            Description="Control panel",
            Manufacturer="Generic",
            PartNumber="PN-1",
        ),
        SimpleNamespace(Label="No controls metadata"),
    ]

    assert collect_bom_rows(objects) == [
        {
            "Tag": "CP-001",
            "Description": "Control panel",
            "Manufacturer": "Generic",
            "PartNumber": "PN-1",
            "Quantity": 1,
        }
    ]
