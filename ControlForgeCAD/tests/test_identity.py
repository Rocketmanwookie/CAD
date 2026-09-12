# SPDX-License-Identifier: MIT

import pytest

from controls_wb.identity import (
    CERoles,
    ensure_object_identity,
    imported_ce_identity,
    is_ce_identity,
    new_ce_identity,
)


class FakeObject:
    def __init__(self):
        self.PropertiesList = []
        self.editor_modes = {}

    def addProperty(self, property_type, name, group, description):
        self.PropertiesList.append(name)
        return self

    def setEditorMode(self, name, mode):
        self.editor_modes[name] = mode


def test_new_identities_are_valid_and_unique():
    first = new_ce_identity()
    second = new_ce_identity()

    assert is_ce_identity(first)
    assert is_ce_identity(second)
    assert first != second


def test_imported_identity_is_repeatable_for_source_identity():
    first = imported_ce_identity("ceproject", "PROJECT-100")

    assert first == imported_ce_identity("ceproject", "PROJECT-100")
    assert first != imported_ce_identity("ceproject", "PROJECT-101")


def test_identity_and_role_are_assigned_once_and_locked():
    obj = FakeObject()
    identity = ensure_object_identity(obj, CERoles.PLC_CONTROLLER)

    assert obj.CEIdentity == identity
    assert obj.CERole == CERoles.PLC_CONTROLLER
    assert obj.editor_modes == {"CEIdentity": 1, "CERole": 1}
    assert ensure_object_identity(obj, CERoles.PLC_CONTROLLER) == identity

    with pytest.raises(ValueError, match="cannot silently change"):
        ensure_object_identity(obj, CERoles.TERMINAL_STRIP)
