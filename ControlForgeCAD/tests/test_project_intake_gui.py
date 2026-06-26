# SPDX-License-Identifier: MIT

from controls_wb.gui.project_intake import (
    apply_form_values_to_project,
    create_or_update_project_from_form,
    form_values_from_project,
    normalized_form_values,
    parse_deliverables,
)


class FakeProjectObject:
    def __init__(self):
        self.PropertiesList = []

    def addProperty(self, property_type, name, group, description):
        self.PropertiesList.append(name)
        return self


class FakeDocument:
    def __init__(self):
        self.Objects = []

    def addObject(self, object_type, name):
        obj = FakeProjectObject()
        obj.ObjectType = object_type
        obj.Name = name
        self.Objects.append(obj)
        return obj


def test_parse_deliverables_normalizes_comma_text():
    assert parse_deliverables("panelLayout, ioList, panelLayout, ") == ["ioList", "panelLayout"]


def test_form_values_from_project_uses_defaults_without_object():
    values = form_values_from_project(None)

    assert values["ProjectName"] == "Controls Project"
    assert values["Deliverables"] == "ioList, panelLayout"


def test_form_values_from_project_reads_existing_object():
    obj = type(
        "Obj",
        (),
        {
            "ProjectName": "Line 7",
            "Customer": "Acme",
            "SiteLocation": "Cleveland",
            "Deliverables": ["panelLayout", "ioList"],
            "NominalVoltage": "480",
            "PhaseCount": "3",
            "EnclosureRating": "NEMA 12",
            "PlcPlatform": "Generic PLC",
            "SensorCount": "18",
        },
    )()

    values = form_values_from_project(obj)

    assert values["ProjectName"] == "Line 7"
    assert values["Customer"] == "Acme"
    assert values["SiteLocation"] == "Cleveland"
    assert values["Deliverables"] == "ioList, panelLayout"
    assert values["PlcPlatform"] == "Generic PLC"


def test_normalized_form_values_strips_text_and_deliverables():
    values = normalized_form_values(
        {
            "ProjectName": " Line 7 ",
            "Customer": " Acme ",
            "SiteLocation": " Cleveland ",
            "Deliverables": " panelLayout,ioList ",
            "NominalVoltage": " 480 ",
            "PhaseCount": " 3 ",
            "EnclosureRating": " NEMA 12 ",
            "PlcPlatform": " Generic PLC ",
            "SensorCount": " 18 ",
        }
    )

    assert values["ProjectName"] == "Line 7"
    assert values["Deliverables"] == ["ioList", "panelLayout"]
    assert values["NominalVoltage"] == "480"
    assert values["SensorCount"] == "18"


def test_apply_form_values_to_project_updates_object():
    obj = FakeProjectObject()

    apply_form_values_to_project(
        obj,
        {
            "ProjectName": "Line 7",
            "Customer": "Acme",
            "SiteLocation": "Cleveland",
            "Deliverables": "ioList",
            "NominalVoltage": "480",
            "PhaseCount": "3",
            "EnclosureRating": "NEMA 12",
            "PlcPlatform": "Generic PLC",
            "SensorCount": "18",
        },
    )

    assert obj.ProjectName == "Line 7"
    assert obj.Deliverables == ["ioList"]
    assert obj.PlcPlatform == "Generic PLC"


def test_create_or_update_project_from_form_creates_ce_project():
    document = FakeDocument()

    project = create_or_update_project_from_form(
        document,
        {
            "ProjectName": "Line 7",
            "Customer": "Acme",
            "SiteLocation": "Cleveland",
            "Deliverables": "ioList",
            "NominalVoltage": "480",
            "PhaseCount": "3",
            "EnclosureRating": "NEMA 12",
            "PlcPlatform": "Generic PLC",
            "SensorCount": "18",
        },
    )

    assert document.Objects == [project]
    assert project.Name == "CE_Project"
    assert project.ProjectName == "Line 7"
    assert project.Customer == "Acme"
    assert project.Deliverables == ["ioList"]
    assert project.SensorCount == "18"
