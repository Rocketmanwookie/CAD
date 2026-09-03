# SPDX-License-Identifier: MIT

import json

from controls_wb.gui.project_intake import (
    COMMUNICATION_PROTOCOL_OPTIONS,
    ENCLOSURE_RATING_OPTIONS,
    IO_ACCESSORY_OPTIONS,
    PLC_LINES_BY_MAKE,
    POWER_CONFIGURATIONS,
    apply_form_values_to_project,
    ceproject_import_record,
    ceproject_import_records_from_project,
    create_or_update_project_from_form,
    form_values_from_project,
    form_values_from_ceproject_xml,
    form_values_from_project_setup_text,
    io_expansion_suggestion,
    merge_ceproject_import_records,
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
from controls_wb.ceproject_xml import ceproject_to_xml
from controls_wb.intake import (
    Contact,
    FieldStatus,
    IntakeField,
    IntakeQuestionResponse,
    ProjectIntake,
    SourceRecord,
    SourceRecordType,
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


def _ceproject_xml_for_import():
    intake = ProjectIntake(
        project_id="CE-XML-001",
        name="XML Setup",
        deliverables={"ioList", "panelLayout"},
        contacts={
            "pm": Contact("pm", "Project manager", "Pat", "pat@example.test", "Customer"),
        },
        source_records={
            "SRC-XML": SourceRecord(
                "SRC-XML",
                SourceRecordType.UPLOADED_FILE,
                "Customer CEProject",
                "Project manager",
                field_ids=("controls.plcPlatform", "io.sensorCount"),
                reference="customer.ceproject.xml",
            ),
        },
        fields={
            "powerFeed.nominalVoltage": IntakeField(
                "powerFeed.nominalVoltage",
                "Nominal voltage",
                "Electrical engineering",
                value="480",
                status=FieldStatus.RECEIVED,
            ),
            "powerFeed.phaseCount": IntakeField(
                "powerFeed.phaseCount",
                "Phase count",
                "Electrical engineering",
                value="3",
                status=FieldStatus.RECEIVED,
            ),
            "environment.enclosureRating": IntakeField(
                "environment.enclosureRating",
                "Enclosure rating",
                "Operations / maintenance",
                value="UL Listed",
                status=FieldStatus.RECEIVED,
            ),
            "controls.plcPlatform": IntakeField(
                "controls.plcPlatform",
                "PLC platform",
                "Controls lead",
                value="Siemens S7-1200",
                status=FieldStatus.RECEIVED,
            ),
            "io.sensorCount": IntakeField(
                "io.sensorCount",
                "Sensor count or estimate",
                "Mechanical / materials handling",
                value="30",
                status=FieldStatus.ESTIMATED,
            ),
        },
        questions={
            "Q-XML-PLC": IntakeQuestionResponse(
                "Q-XML-PLC",
                "controls.plcPlatform",
                "Confirm PLC platform.",
                "Controls lead",
                status=FieldStatus.RECEIVED,
                response="Siemens S7-1200",
                source_ids=("SRC-XML",),
            ),
        },
    )
    return ceproject_to_xml(intake)


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
            "ControlledLoads": ["motor, Conveyor, 2, 1hp"],
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
    assert values["ControlledLoads"] == "motor, Conveyor, 2, 1hp"
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
            "ControlledLoads": " motor, Conveyor, 2, 1hp\nheat_strip, Cabinet heater, 1, 500W ",
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
    assert values["ControlledLoads"] == [
        "motor, Conveyor, 2, 1hp",
        "heat_strip, Cabinet heater, 1, 500W",
    ]
    assert values["EstimatedLoadAmps"] == "3.54"
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
            "ControlledLoads": "motor, Conveyor, 2, 1hp",
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
    assert obj.ControlledLoads == ["motor, Conveyor, 2, 1hp"]
    assert obj.EstimatedLoadAmps == "2.82"
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


def test_ceproject_xml_import_record_maps_to_project_setup_form_values():
    xml_text = _ceproject_xml_for_import()
    values = form_values_from_ceproject_xml(xml_text)

    assert values["ProjectName"] == "XML Setup"
    assert values["Deliverables"] == "ioList, panelLayout"
    assert values["PowerConfiguration"] == "3PH 480V"
    assert values["EnclosureRatings"] == "UL Listed"
    assert values["PlcMake"] == "Siemens"
    assert values["PlcLine"] == "S7-1200"
    assert values["DICount"] == "30"
    assert values["SourceType"] == "Uploaded file / reference"


def test_project_setup_text_import_maps_to_normalized_form_values():
    values = form_values_from_project_setup_text(
        """
project:
  name: Line 11
  customer: Acme
deliverables:
  - ioList
power:
  configuration: 3PH 480V
plc:
  make: Siemens
  line: S7-1200
io:
  di_count: 8
  ai_count: 2
"""
    )
    normalized = normalized_form_values(values)

    assert normalized["ProjectName"] == "Line 11"
    assert normalized["Customer"] == "Acme"
    assert normalized["Deliverables"] == ["ioList"]
    assert normalized["PowerConfiguration"] == "3PH 480V"
    assert normalized["PlcPlatform"] == "Siemens S7-1200"
    assert normalized["SensorCount"] == "10"
    assert values["ImportWarnings"] == []


def test_ceproject_xml_import_records_are_deduplicated_and_selectable():
    xml_text = _ceproject_xml_for_import()
    record = ceproject_import_record(xml_text, "/tmp/customer.ceproject.xml")

    merged = merge_ceproject_import_records([], record)
    merged = merge_ceproject_import_records(merged, record)
    obj = type("Obj", (), {"CEProjectImports": merged})()
    records = ceproject_import_records_from_project(obj)

    assert len(merged) == 1
    assert len(records) == 1
    assert records[0]["projectId"] == "CE-XML-001"
    assert records[0]["projectName"] == "XML Setup"
    assert records[0]["xmlText"] == xml_text


def test_create_or_update_project_from_form_remembers_and_applies_ceproject_xml_import():
    document = FakeDocument()
    xml_text = _ceproject_xml_for_import()
    record = ceproject_import_record(xml_text, "/tmp/customer.ceproject.xml")
    record_id = json.loads(record)["id"]

    project = create_or_update_project_from_form(
        document,
        {
            **form_values_from_ceproject_xml(xml_text),
            "CEProjectImportRecord": record,
            "SelectedCEProjectImportId": record_id,
        },
    )

    assert project.ProjectId == "CE-XML-001"
    assert project.ProjectName == "XML Setup"
    assert project.PlcMake == "Siemens"
    assert project.PlcLine == "S7-1200"
    assert project.DICount == "30"
    assert len(project.CEProjectImports) == 1
    import_records = ceproject_import_records_from_project(project)
    assert import_records[0]["id"] == record_id
    assert any(json.loads(record)["id"] == "SRC-XML" for record in project.SourceRecords)
    assert any(json.loads(record)["id"].startswith("SRC-CEPROJECT-IMPORT-") for record in project.SourceRecords)
    assert any(json.loads(contact)["id"] == "pm" for contact in project.Contacts)
    assert any(json.loads(question)["id"] == "Q-XML-PLC" for question in project.IntakeQuestions)
