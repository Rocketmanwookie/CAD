# SPDX-License-Identifier: MIT

import json

from controls_wb.gui.project_intake import (
    COMMUNICATION_PROTOCOL_OPTIONS,
    ENCLOSURE_RATING_OPTIONS,
    IO_ACCESSORY_OPTIONS,
    PLC_LINES_BY_MAKE,
    POWER_CONFIGURATIONS,
    apply_form_values_to_project,
    create_or_update_project_from_form,
    form_values_from_project,
    io_expansion_suggestion,
    normalized_form_values,
    normalized_plc_line,
    parse_deliverables,
    parse_power_configuration,
    plc_platform_from_make_line,
    power_configuration_from_values,
    setup_source_record_from_form,
    source_type_value_from_label,
    total_input_count,
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
            "PowerConfiguration": "3PH 480V",
            "EnclosureRatings": ["UL Listed", "NEMA 12"],
            "PlcMake": "Siemens",
            "PlcLine": "S7-1200",
            "PlcCPU": "CPU 1212C DC/DC/DC",
            "DICount": "16",
            "DOCount": "8",
            "AICount": "2",
            "AOCount": "1",
            "IOAccessories": ["Remote / modular I/O bank"],
            "EthernetAdapter": "Integrated PROFINET interface",
            "ExpansionPowerSupply": "External 24 VDC supply required",
            "CommunicationProtocols": ["EtherNet/IP", "Modbus TCP"],
            "SourceRecords": [
                json.dumps(
                    {
                        "id": "SRC-PROJECT-SETUP-001",
                        "type": "meeting_note",
                        "title": "Kickoff meeting",
                        "stakeholder": "Controls lead",
                        "reference": "Minutes 2026-08-03",
                    }
                )
            ],
        },
    )()

    values = form_values_from_project(obj)

    assert values["ProjectName"] == "Line 7"
    assert values["Customer"] == "Acme"
    assert values["SiteLocation"] == "Cleveland"
    assert values["Deliverables"] == "ioList, panelLayout"
    assert values["PlcMake"] == "Siemens"
    assert values["PlcLine"] == "S7-1200"
    assert values["PowerConfiguration"] == "3PH 480V"
    assert values["EnclosureRatings"] == "NEMA 12, UL Listed"
    assert values["PlcCPU"] == "CPU 1212C DC/DC/DC"
    assert values["DICount"] == "16"
    assert values["IOAccessories"] == "Remote / modular I/O bank"
    assert values["CommunicationProtocols"] == "EtherNet/IP, Modbus TCP"
    assert values["SourceType"] == "Meeting note"
    assert values["SourceTitle"] == "Kickoff meeting"
    assert values["SourceStakeholder"] == "Controls lead"
    assert values["SourceReference"] == "Minutes 2026-08-03"


def test_normalized_form_values_strips_text_and_deliverables():
    values = normalized_form_values(
        {
            "ProjectName": " Line 7 ",
            "Customer": " Acme ",
            "SiteLocation": " Cleveland ",
            "Deliverables": " panelLayout,ioList ",
            "PowerConfiguration": "3PH 480V",
            "EnclosureRatings": " UL Listed, NEMA 12 ",
            "PlcMake": " Siemens ",
            "PlcLine": " S7-1200 ",
            "PlcCPU": "CPU 1214C DC/DC/DC",
            "DICount": " 16 ",
            "DOCount": " 8 ",
            "AICount": " 2 ",
            "AOCount": " 1 ",
            "IOAccessories": " Remote / modular I/O bank, Ethernet I/O adapter ",
            "CommunicationProtocols": " EtherNet/IP, Modbus TCP ",
        }
    )

    assert values["ProjectName"] == "Line 7"
    assert values["Deliverables"] == ["ioList", "panelLayout"]
    assert values["NominalVoltage"] == "480"
    assert values["PhaseCount"] == "3"
    assert values["PowerConfiguration"] == "3PH 480V"
    assert values["EnclosureRatings"] == ["NEMA 12", "UL Listed"]
    assert values["EnclosureRating"] == "NEMA 12, UL Listed"
    assert values["PlcMake"] == "Siemens"
    assert values["PlcLine"] == "S7-1200"
    assert values["PlcPlatform"] == "Siemens S7-1200"
    assert values["PlcCPU"] == "CPU 1214C DC/DC/DC"
    assert values["DICount"] == "16"
    assert values["SensorCount"] == "18"
    assert values["IOAccessories"] == ["Ethernet I/O adapter", "Remote / modular I/O bank"]
    assert values["CommunicationProtocols"] == ["EtherNet/IP", "Modbus TCP"]
    assert "DI:" in values["IOExpansionSuggestion"]


def test_plc_make_line_helpers_keep_line_contingent_on_make():
    assert "3PH 480V" in POWER_CONFIGURATIONS
    assert "UL Listed" in ENCLOSURE_RATING_OPTIONS
    assert "PROFIBUS" in COMMUNICATION_PROTOCOL_OPTIONS
    assert PLC_LINES_BY_MAKE["Siemens"] == ("S7-1200",)
    assert normalized_plc_line("Siemens", "CompactLogix 5380") == "S7-1200"
    assert normalized_plc_line("Allen-Bradley", "CompactLogix 5380") == "Micro800"
    assert plc_platform_from_make_line("Siemens", "S7-1200") == "Siemens S7-1200"
    assert parse_power_configuration("3PH 480V") == ("480", "3")
    assert power_configuration_from_values("480", "3") == "3PH 480V"
    assert total_input_count("16", "2") == "18"
    assert "Remote / modular I/O bank" in IO_ACCESSORY_OPTIONS
    assert source_type_value_from_label("Customer email") == "email"


def test_io_expansion_suggestion_targets_twenty_percent_spare():
    suggestion = io_expansion_suggestion(
        "Siemens",
        "S7-1200",
        "CPU 1212C DC/DC/DC",
        "20",
        "12",
        "4",
        "2",
    )

    assert "DI: target 24, CPU 8, add 1 x SM 1221 DI 16x24 V DC" in suggestion
    assert "DO: target 15, CPU 6, add 1 x SM 1222 DQ 16x24 VDC" in suggestion
    assert "vendor-verified" in suggestion


def test_setup_source_record_from_form_attaches_filled_setup_fields():
    normalized = normalized_form_values(
        {
            "ProjectName": "Line 7",
            "Deliverables": "ioList,panelLayout",
            "NominalVoltage": "480",
            "PhaseCount": "3",
            "EnclosureRating": "NEMA 12",
            "PlcMake": "Siemens",
            "PlcLine": "S7-1200",
            "DICount": "16",
            "DOCount": "8",
            "AICount": "2",
            "AOCount": "0",
        }
    )

    record = json.loads(
        setup_source_record_from_form(
            {
                "SourceType": "Meeting note",
                "SourceTitle": "Kickoff review",
                "SourceStakeholder": "Controls lead",
                "SourceReference": "Meeting notes 2026-08-03",
            },
            normalized,
        )
    )

    assert record["id"] == "SRC-PROJECT-SETUP-001"
    assert record["type"] == "meeting_note"
    assert record["title"] == "Kickoff review"
    assert record["stakeholder"] == "Controls lead"
    assert record["reference"] == "Meeting notes 2026-08-03"
    assert record["fieldIds"] == [
        "project.name",
        "powerFeed.nominalVoltage",
        "powerFeed.phaseCount",
        "environment.enclosureRating",
        "controls.plcPlatform",
        "io.sensorCount",
    ]


def test_apply_form_values_to_project_updates_object():
    obj = FakeProjectObject()

    apply_form_values_to_project(
        obj,
        {
            "ProjectName": "Line 7",
            "Customer": "Acme",
            "SiteLocation": "Cleveland",
            "Deliverables": "ioList",
            "PowerConfiguration": "3PH 480V",
            "EnclosureRatings": "UL Listed, NEMA 12",
            "PlcMake": "Siemens",
            "PlcLine": "S7-1200",
            "PlcCPU": "CPU 1214C DC/DC/DC",
            "DICount": "16",
            "DOCount": "8",
            "AICount": "2",
            "AOCount": "1",
            "IOAccessories": "Remote / modular I/O bank",
            "EthernetAdapter": "Integrated PROFINET interface",
            "ExpansionPowerSupply": "External 24 VDC supply required",
            "CommunicationProtocols": "PROFINET, Modbus TCP",
            "SourceType": "Customer email",
            "SourceTitle": "Customer controls basis",
            "SourceStakeholder": "Customer engineering",
            "SourceReference": "email://line-7",
        },
    )

    assert obj.ProjectName == "Line 7"
    assert obj.Deliverables == ["ioList"]
    assert obj.PowerConfiguration == "3PH 480V"
    assert obj.NominalVoltage == "480"
    assert obj.PhaseCount == "3"
    assert obj.EnclosureRatings == ["NEMA 12", "UL Listed"]
    assert obj.PlcMake == "Siemens"
    assert obj.PlcLine == "S7-1200"
    assert obj.PlcCPU == "CPU 1214C DC/DC/DC"
    assert obj.PlcPlatform == "Siemens S7-1200"
    assert obj.DICount == "16"
    assert obj.SensorCount == "18"
    assert obj.IOAccessories == ["Remote / modular I/O bank"]
    assert obj.CommunicationProtocols == ["Modbus TCP", "PROFINET"]
    assert obj.EthernetAdapter == "Integrated PROFINET interface"
    assert obj.ExpansionPowerSupply == "External 24 VDC supply required"
    assert "DI:" in obj.IOExpansionSuggestion
    assert len(obj.SourceRecords) >= 1
    setup_source = json.loads(obj.SourceRecords[-1])
    assert setup_source["type"] == "email"
    assert "controls.plcPlatform" in setup_source["fieldIds"]


def test_create_or_update_project_from_form_creates_ce_project():
    document = FakeDocument()

    project = create_or_update_project_from_form(
        document,
        {
            "ProjectName": "Line 7",
            "Customer": "Acme",
            "SiteLocation": "Cleveland",
            "Deliverables": "ioList",
            "PowerConfiguration": "3PH 480V",
            "EnclosureRatings": "UL Listed, NEMA 12",
            "PlcMake": "Allen-Bradley",
            "PlcLine": "Micro800",
            "PlcCPU": "Micro800 starter placeholder",
            "DICount": "10",
            "DOCount": "4",
            "AICount": "1",
            "AOCount": "1",
            "IOAccessories": "Remote / modular I/O bank",
            "CommunicationProtocols": "EtherNet/IP",
            "SourceType": "Meeting note",
            "SourceTitle": "Project kickoff",
            "SourceStakeholder": "Project manager",
            "SourceReference": "",
        },
    )

    assert document.Objects == [project]
    assert project.Name == "CE_Project"
    assert project.ProjectName == "Line 7"
    assert project.Customer == "Acme"
    assert project.Deliverables == ["ioList"]
    assert project.PlcPlatform == "Allen-Bradley Micro800"
    assert project.SensorCount == "11"
    assert project.DICount == "10"
    assert project.IOAccessories == ["Remote / modular I/O bank"]
    assert project.CommunicationProtocols == ["EtherNet/IP"]
    assert any("SRC-PROJECT-SETUP-001" in record for record in project.SourceRecords)


def test_create_or_update_project_from_form_preserves_existing_io_signals():
    document = FakeDocument()
    existing = document.addObject("App::FeaturePython", "CE_Project")
    existing.ProjectId = "CE-PROJECT-001"
    existing.Deliverables = ["ioList"]
    existing.IOSignals = ['{"tag": "DI-0001"}']
    existing.SourceRecords = [
        json.dumps(
            {
                "id": "SRC-PROJECT-SETUP-001",
                "type": "manual_entry",
                "title": "Old setup",
                "stakeholder": "Project manager",
                "fieldIds": ["project.name"],
            }
        ),
        json.dumps(
            {
                "id": "SRC-OTHER",
                "type": "email",
                "title": "Other source",
                "stakeholder": "Controls lead",
                "fieldIds": ["controls.plcPlatform"],
            }
        ),
    ]

    project = create_or_update_project_from_form(
        document,
        {
            "ProjectName": "Line 8",
            "Customer": "Acme",
            "SiteLocation": "Cleveland",
            "Deliverables": "ioList",
            "PowerConfiguration": "3PH 480V",
            "EnclosureRatings": "NEMA 12",
            "PlcMake": "Siemens",
            "PlcLine": "S7-1200",
            "PlcCPU": "CPU 1212C DC/DC/DC",
            "DICount": "4",
            "DOCount": "2",
            "AICount": "0",
            "AOCount": "0",
            "IOAccessories": "",
            "SourceType": "Meeting note",
            "SourceTitle": "Updated setup",
            "SourceStakeholder": "Project manager",
            "SourceReference": "",
        },
    )

    assert project is existing
    assert project.ProjectName == "Line 8"
    assert project.IOSignals == ['{"tag": "DI-0001"}']
    source_records = [json.loads(record) for record in project.SourceRecords]
    assert [record["id"] for record in source_records] == ["SRC-OTHER", "SRC-PROJECT-SETUP-001"]
    assert source_records[-1]["title"] == "Updated setup"
