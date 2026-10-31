# SPDX-License-Identifier: MIT

import pytest

from controls_wb.intake_settings import (
    DELIVERY_METHODS,
    IntakeSystemSettings,
    load_intake_settings,
    save_intake_settings,
)


class FakeParameters:
    def __init__(self):
        self.values = {}

    def GetString(self, key, default):
        return self.values.get(key, default)

    def SetString(self, key, value):
        self.values[key] = value


class FakeApp:
    def __init__(self):
        self.parameters = {}

    def ParamGet(self, path):
        return self.parameters.setdefault(path, FakeParameters())


def test_load_intake_settings_uses_safe_local_defaults():
    settings = load_intake_settings(FakeApp())

    assert settings == IntakeSystemSettings(
        database_location="~/ControlForgeCAD/intake.sqlite",
        delivery_method="local_form",
        delivery_target="",
        form_template="",
    )


def test_save_intake_settings_round_trips_normalized_preferences():
    app = FakeApp()

    saved = save_intake_settings(
        IntakeSystemSettings(
            database_location="  ~/Jobs/intake.sqlite  ",
            delivery_method="email_draft",
            delivery_target="  intake@example.test ",
            form_template="  templates/forms/project-intake.schema.json ",
        ),
        app,
    )

    assert saved == IntakeSystemSettings(
        database_location="~/Jobs/intake.sqlite",
        delivery_method="email_draft",
        delivery_target="intake@example.test",
        form_template="templates/forms/project-intake.schema.json",
    )
    assert load_intake_settings(app) == saved


@pytest.mark.parametrize("settings", (
    IntakeSystemSettings("", "local_form", "", ""),
    IntakeSystemSettings("/tmp/intake.sqlite", "unknown", "", ""),
))
def test_save_intake_settings_rejects_invalid_local_preferences(settings):
    with pytest.raises(ValueError):
        save_intake_settings(settings, FakeApp())


def test_delivery_methods_are_user_selectable_values():
    assert DELIVERY_METHODS == ("local_form", "email_draft", "delivery_url")
