# SPDX-License-Identifier: MIT

import pytest

from controls_wb.setup_import import ProjectSetupImportError, parse_project_setup


def test_project_setup_yaml_import_maps_nested_sections():
    result = parse_project_setup(
        """
project:
  name: Line 9 Controls
  customer: Acme
  site_location: Building 4
deliverables:
  - ioList
  - panelLayout
power:
  configuration: 3PH 480V
controlled_loads:
  - motor, Conveyor, 2, 1hp
  - heat_strip, Cabinet heater, 1, 500W
enclosure_ratings:
  - UL Listed
  - NEMA 12
plc:
  make: Siemens
  line: S7-1200
  cpu: CPU 1214C DC/DC/DC
io:
  di_count: 16
  do_count: 8
  ai_count: 2
  ao_count: 1
source:
  type: Meeting note
  title: Kickoff setup import
  stakeholder: Controls lead
  reference: meeting://line-9
"""
    )

    assert result.warnings == ()
    assert result.values["ProjectName"] == "Line 9 Controls"
    assert result.values["Customer"] == "Acme"
    assert result.values["SiteLocation"] == "Building 4"
    assert result.values["Deliverables"] == ["ioList", "panelLayout"]
    assert result.values["PowerConfiguration"] == "3PH 480V"
    assert result.values["ControlledLoads"] == [
        "motor, Conveyor, 2, 1hp",
        "heat_strip, Cabinet heater, 1, 500W",
    ]
    assert result.values["EnclosureRatings"] == ["UL Listed", "NEMA 12"]
    assert result.values["PlcMake"] == "Siemens"
    assert result.values["PlcLine"] == "S7-1200"
    assert result.values["DICount"] == "16"
    assert result.values["SourceType"] == "Meeting note"


def test_project_setup_yaml_import_combines_voltage_and_phase():
    result = parse_project_setup(
        """
name: Pump Skid
nominal_voltage: 480
phase_count: 3
"""
    )

    assert result.values["ProjectName"] == "Pump Skid"
    assert result.values["PowerConfiguration"] == "3PH 480V"


def test_project_setup_yaml_import_preserves_comma_delimited_load_lines():
    result = parse_project_setup(
        """
project_name: Conveyor Controls
controlled_loads: motor, Conveyor, 2, 1hp
"""
    )

    assert result.values["ControlledLoads"] == ["motor, Conveyor, 2, 1hp"]


def test_project_setup_uml_import_maps_fact_lines():
    result = parse_project_setup(
        """
@startuml
title Line 10
class CE_Project {
  ProjectName = Line 10
  Customer = Acme
  SiteLocation = Packaging
  PowerConfiguration = 3PH 480V
  PlcMake = Siemens
  PlcLine = S7-1200
  DICount = 12
  DOCount = 6
}
note right of CE_Project
Deliverables: ioList, panelLayout
CommunicationProtocols: PROFINET, Modbus TCP
EnclosureRatings: UL Listed, NEMA 12
end note
@enduml
""",
        "plantuml",
    )

    assert result.values["ProjectName"] == "Line 10"
    assert result.values["Deliverables"] == ["ioList", "panelLayout"]
    assert result.values["CommunicationProtocols"] == ["PROFINET", "Modbus TCP"]
    assert result.values["EnclosureRatings"] == ["UL Listed", "NEMA 12"]
    assert result.values["DICount"] == "12"


def test_project_setup_import_reports_unsupported_text():
    with pytest.raises(ProjectSetupImportError, match="No supported"):
        parse_project_setup("this is only prose")
