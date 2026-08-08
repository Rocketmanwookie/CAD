# SPDX-License-Identifier: MIT

import json

from controls_wb.intake import default_project_intake
from controls_wb.model.project import (
    PROJECT_PROPERTY_SPECS,
    ControlsProject,
    _project_payloads,
    create_or_update_project,
    initialize_project_object,
    intake_to_project_properties,
)


class FakeProjectObject:
    def __init__(self):
        self.PropertiesList = []
        self.added_properties = []

    def addProperty(self, property_type, name, group, description):
        self.PropertiesList.append(name)
        self.added_properties.append((property_type, name, group, description))
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


def test_project_payloads_include_contacts_sources_and_questions():
    contacts, sources, questions = _project_payloads(default_project_intake())

    contact_records = [json.loads(contact) for contact in contacts]
    source_records = [json.loads(source) for source in sources]
    question_records = [json.loads(question) for question in questions]

    assert any(record["role"] == "Controls lead" for record in contact_records)
    assert any(record["type"] == "manual_entry" and "project.name" in record["fieldIds"] for record in source_records)
    assert any(record["fieldId"] == "controls.plcPlatform" and record["ask"] == "Controls lead" for record in question_records)


def test_project_property_specs_expose_editable_intake_fields():
    specs = {spec.name: spec for spec in PROJECT_PROPERTY_SPECS}

    assert specs["ProjectName"].property_type == "App::PropertyString"
    assert specs["Customer"].group == "CEProject"
    assert specs["SiteLocation"].description == "Site or installation location"
    assert specs["CEProjectImports"].property_type == "App::PropertyStringList"
    assert specs["CEProjectImports"].group == "CEProject"
    assert specs["Deliverables"].property_type == "App::PropertyStringList"
    assert specs["IOSignals"].property_type == "App::PropertyStringList"
    assert specs["IOSignals"].group == "I/O"
    assert specs["NominalVoltage"].group == "Intake"
    assert specs["PhaseCount"].group == "Intake"
    assert specs["PowerConfiguration"].group == "Power"
    assert specs["ControlledLoads"].property_type == "App::PropertyStringList"
    assert specs["EstimatedLoadAmps"].group == "Power"
    assert specs["EnclosureRatings"].property_type == "App::PropertyStringList"
    assert specs["EnclosureRating"].group == "Intake"
    assert specs["PlcPlatform"].group == "Intake"
    assert specs["PlcMake"].group == "PLC / I/O"
    assert specs["PlcLine"].group == "PLC / I/O"
    assert specs["PlcCPU"].group == "PLC / I/O"
    assert specs["SensorCount"].group == "Intake"
    assert specs["DICount"].group == "PLC / I/O"
    assert specs["DOCount"].group == "PLC / I/O"
    assert specs["AICount"].group == "PLC / I/O"
    assert specs["AOCount"].group == "PLC / I/O"
    assert specs["IOAccessories"].property_type == "App::PropertyStringList"
    assert specs["EthernetAdapter"].group == "PLC / I/O"
    assert specs["ExpansionPowerSupply"].group == "PLC / I/O"
    assert specs["IOExpansionSuggestion"].group == "PLC / I/O"
    assert specs["CommunicationProtocols"].property_type == "App::PropertyStringList"


def test_intake_to_project_properties_maps_starter_payload():
    properties = intake_to_project_properties(default_project_intake(name="Line 7 Upgrade"))

    assert properties["ProjectName"] == "Line 7 Upgrade"
    assert properties["SchemaVersion"] == "0.1.0"
    assert properties["Deliverables"] == ["ioList", "panelLayout"]
    assert properties["Customer"] == ""
    assert properties["SiteLocation"] == ""
    assert properties["CEProjectImports"] == []
    assert properties["IOSignals"] == []
    assert properties["IOAccessories"] == []
    assert properties["EnclosureRatings"] == []
    assert properties["CommunicationProtocols"] == []
    assert properties["ControlledLoads"] == []
    assert properties["EstimatedLoadAmps"] == ""
    assert properties["PowerFeedStatus"] == "Requested"


def test_initialize_project_object_adds_properties_and_proxy():
    obj = initialize_project_object(FakeProjectObject(), default_project_intake())

    assert isinstance(obj.Proxy, ControlsProject)
    assert obj.Proxy.Type == "ControlsProject"
    assert obj.ProjectId == "CE-PROJECT-001"
    assert obj.ProjectName == "Controls Project"
    assert obj.Deliverables == ["ioList", "panelLayout"]
    assert "ProjectName" in obj.PropertiesList
    assert "Customer" in obj.PropertiesList
    assert "SiteLocation" in obj.PropertiesList
    assert "CEProjectImports" in obj.PropertiesList
    assert "IOSignals" in obj.PropertiesList
    assert "PowerConfiguration" in obj.PropertiesList
    assert "ControlledLoads" in obj.PropertiesList
    assert "EstimatedLoadAmps" in obj.PropertiesList
    assert "EnclosureRatings" in obj.PropertiesList
    assert "DICount" in obj.PropertiesList
    assert "IOAccessories" in obj.PropertiesList
    assert "CommunicationProtocols" in obj.PropertiesList
    assert "PlcPlatform" in obj.PropertiesList


def test_project_proxy_round_trips_persistent_state():
    obj = initialize_project_object(FakeProjectObject(), default_project_intake())

    state = obj.Proxy.__getstate__()
    restored = ControlsProject.__new__(ControlsProject)
    restored.__setstate__(state)

    assert restored.Type == "ControlsProject"


def test_create_or_update_project_reuses_existing_project_object():
    document = FakeDocument()
    first = create_or_update_project(document, name="Original")
    first.Customer = "Acme"

    second = create_or_update_project(document, name="Updated")

    assert first is second
    assert document.Objects == [first]
    assert second.ProjectName == "Updated"
    assert second.ObjectType == "App::FeaturePython"
    assert second.Name == "CE_Project"
