# SPDX-License-Identifier: MIT

import pytest

from controls_wb.commands.edit_electrical_path import selected_electrical_path
from controls_wb.identity import CERoles


class Item:
    def __init__(self, role):
        self.CERole = role


def test_selection_requires_exactly_one_typed_path():
    path = Item(CERoles.CONNECTION_PATH)
    assert selected_electrical_path([Item(CERoles.WIRE), path]) is path
    with pytest.raises(ValueError, match="exactly one"):
        selected_electrical_path([])
    with pytest.raises(ValueError, match="exactly one"):
        selected_electrical_path([path, Item(CERoles.CONNECTION_PATH)])
