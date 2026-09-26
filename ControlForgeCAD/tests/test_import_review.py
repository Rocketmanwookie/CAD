# SPDX-License-Identifier: MIT

import pytest

from controls_wb.import_review import (
    ImportReviewError,
    apply_approved_ceproject_io_import,
    apply_approved_project_import,
    remember_approved_ceproject_io_source,
    stage_ceproject_io_import,
    stage_project_import,
)
from controls_wb.ceproject_xml import ceproject_to_xml
from controls_wb.electrical_path import ElectricalConnectionPath, TerminalEndpoint, WireSegment
from controls_wb.identity import CERoles, new_ce_identity
from controls_wb.intake import default_project_intake
from controls_wb.model.project import create_or_update_project
from controls_wb.io_list import IOSignal, explicit_io_signals_from_project, serialize_io_signal


class FakeObject:
    def __init__(self, name):
        self.Name = name
        self.PropertiesList = []

    def addProperty(self, _type, name, _group, _description):
        self.PropertiesList.append(name)
        return self


class FakeDocument:
    def __init__(self):
        self.Objects = []

    def addObject(self, _type, name):
        obj = FakeObject(name)
        self.Objects.append(obj)
        return obj


def test_stage_yaml_is_read_only_and_lists_only_changed_review_candidates():
    document = FakeDocument()
    project = create_or_update_project(document)
    project.ProjectName = "Existing project"
    source = """project:\n  name: Imported project\nplc:\n  make: Siemens\n  line: S7-1200\n  cpu: CPU 1214C DC/DC/DC\n  di_count: 12\n"""

    staged = stage_project_import(source, "setup.yaml", project)

    assert project.ProjectName == "Existing project"
    assert staged.source_format == "yaml"
    assert {candidate.key for candidate in staged.candidates} >= {"ProjectName", "PlcCPU", "DICount"}


def test_apply_requires_explicit_approved_subset_and_leaves_other_candidates_unchanged():
    document = FakeDocument()
    project = create_or_update_project(document)
    project.ProjectName = "Existing project"
    project.DICount = "2"
    staged = stage_project_import("project_name: Imported project\ndi_count: 12\n", "setup.yml", project)

    with pytest.raises(ImportReviewError, match="Select at least one"):
        apply_approved_project_import(project, staged, set())
    with pytest.raises(ImportReviewError, match="not staged"):
        apply_approved_project_import(project, staged, {"NotAField"})

    apply_approved_project_import(project, staged, {"DICount"})

    assert project.DICount == "12"
    assert project.ProjectName == "Existing project"


def test_partial_plc_make_approval_rejects_unapproved_dependency_normalization():
    document = FakeDocument()
    project = create_or_update_project(document)
    project.PlcMake = "Siemens"
    project.PlcLine = "S7-1200"
    project.PlcCPU = "CPU 1212C DC/DC/DC"
    project.EthernetAdapter = "Integrated PROFINET interface"
    project.ExpansionPowerSupply = "External 24 VDC supply required"
    project.PlcPlatform = "Siemens S7-1200"
    staged = stage_project_import("plc:\n  make: Allen-Bradley\n", "setup.yml", project)

    with pytest.raises(ImportReviewError, match="unapproved PLC fields"):
        apply_approved_project_import(project, staged, {"PlcMake"})

    assert (
        project.PlcMake,
        project.PlcLine,
        project.PlcCPU,
        project.EthernetAdapter,
        project.ExpansionPowerSupply,
        project.PlcPlatform,
    ) == (
        "Siemens",
        "S7-1200",
        "CPU 1212C DC/DC/DC",
        "Integrated PROFINET interface",
        "External 24 VDC supply required",
        "Siemens S7-1200",
    )


def test_full_unsupported_plc_approval_rejects_catalog_rewrite_without_mutation():
    document = FakeDocument()
    project = create_or_update_project(document)
    project.PlcMake = "Siemens"
    project.PlcLine = "S7-1200"
    project.PlcCPU = "CPU 1212C DC/DC/DC"
    project.EthernetAdapter = "Integrated PROFINET interface"
    project.ExpansionPowerSupply = "External 24 VDC supply required"
    project.PlcPlatform = "Siemens S7-1200"
    staged = stage_project_import(
        """plc:
  make: Allen-Bradley
  line: CompactLogix 5380
  cpu: 5069-L306ER
  ethernet_adapter: EtherNet/IP
  expansion_power_supply: 24 VDC
""",
        "unsupported-plc.yml",
        project,
    )

    with pytest.raises(ImportReviewError, match="not compatible with the bundled catalog"):
        apply_approved_project_import(
            project, staged, {candidate.key for candidate in staged.candidates}
        )

    assert (
        project.PlcMake,
        project.PlcLine,
        project.PlcCPU,
        project.EthernetAdapter,
        project.ExpansionPowerSupply,
        project.PlcPlatform,
    ) == (
        "Siemens",
        "S7-1200",
        "CPU 1212C DC/DC/DC",
        "Integrated PROFINET interface",
        "External 24 VDC supply required",
        "Siemens S7-1200",
    )


def test_approved_unsupported_plc_line_rejects_even_when_default_matches_current_project():
    document = FakeDocument()
    project = create_or_update_project(document)
    project.PlcMake = "Allen-Bradley"
    project.PlcLine = "Micro800"
    project.PlcCPU = "Micro820 2080-LC20-20QWB"
    project.EthernetAdapter = "Embedded EtherNet/IP"
    project.ExpansionPowerSupply = "24 VDC expansion supply"
    project.PlcPlatform = "Allen-Bradley Micro800"
    staged = stage_project_import(
        "plc:\n  line: Unsupported line\n", "unsupported-line.yml", project
    )

    with pytest.raises(ImportReviewError, match="not compatible with the bundled catalog"):
        apply_approved_project_import(project, staged, {"PlcLine"})

    assert project.PlcLine == "Micro800"
    assert project.PlcCPU == "Micro820 2080-LC20-20QWB"


def test_stage_ceproject_xml_preserves_source_only_after_explicit_apply():
    document = FakeDocument()
    project = create_or_update_project(document)
    xml = """<?xml version=\"1.0\"?><CEProject xmlns=\"https://whrsdaparty.github.io/ceproject/0.1\" schemaVersion=\"0.1.0\" projectId=\"CE-IMPORT-001\"><Metadata><Name>Imported XML project</Name></Metadata><Intake /></CEProject>"""

    staged = stage_project_import(xml, "incoming.ceproject.xml", project)

    assert staged.source_format == "ceproject-xml"
    assert project.CEProjectImports == []
    apply_approved_project_import(project, staged, {"ProjectName"})
    assert project.ProjectName == "Imported XML project"
    assert len(project.CEProjectImports) == 1


def test_stage_ceproject_xml_warns_that_paths_are_not_part_of_phase_one_apply():
    document = FakeDocument()
    project = create_or_update_project(document)
    plc = TerminalEndpoint(new_ce_identity(), CERoles.PLC_CHANNEL_TERMINAL, new_ce_identity(), "X1.0")
    device = TerminalEndpoint(new_ce_identity(), CERoles.DEVICE_TERMINAL, new_ce_identity(), "1")
    wire = WireSegment(new_ce_identity(), plc.identity, device.identity, "W-001")
    path = ElectricalConnectionPath(new_ce_identity(), new_ce_identity(), "DI-0001", (plc, device), (wire,))
    xml = ceproject_to_xml(default_project_intake("Imported XML project"), (path,))

    staged = stage_project_import(xml, "incoming.xml", project)

    assert staged.warnings == ("1 typed connection path(s) were detected but are not applied in phase 1.",)


def _ceproject_with_signals(signals: str) -> str:
    return f'''<?xml version="1.0"?>
<CEProject xmlns="https://whrsdaparty.github.io/ceproject/0.1" schemaVersion="0.1.0" projectId="CE-IMPORT-IO">
  <Metadata><Name>I/O import</Name></Metadata>
  <Signals>{signals}</Signals>
</CEProject>'''


def test_stage_ceproject_io_rows_is_read_only_and_rejects_imported_coordinates():
    current = [IOSignal("DI-0001", "Existing", "digital_input", address="%I0.0", rack="0", slot="1", channel="0", mapping_status="allocated")]
    staged = stage_ceproject_io_import(
        _ceproject_with_signals('<Signal signalId="SIG-1" tag="DI-0001" type="DI" description="Photoeye" plcAddress="Local:2:I.Data.1" terminal="X1:02"/>'),
        "incoming.ceproject.xml", current,
    )

    assert current[0].description == "Existing"
    assert len(staged.candidates) == 1
    candidate = staged.candidates[0]
    assert (candidate.candidate_id, candidate.action) == ("io:SIG-1", "update")
    assert (candidate.proposed.address, candidate.proposed.rack, candidate.proposed.slot, candidate.proposed.channel) == ("%I0.0", "0", "1", "0")
    assert [item.code for item in staged.diagnostics] == ["imported_coordinate_ignored", "imported_coordinate_ignored"]


def test_stage_ceproject_io_reports_source_identity_and_type_conflicts():
    staged = stage_ceproject_io_import(
        _ceproject_with_signals(
            '<Signal signalId="SIG-1" tag="DI-0001" type="DI"/>'
            '<Signal signalId="SIG-1" tag="DI-0002" type="DI"/>'
            '<Signal signalId="SIG-3" tag="DI-0001" type="SDI"/>'
        ),
    )

    assert [(item.candidate_id, item.action) for item in staged.candidates] == [("io:SIG-1", "add")]
    assert {item.code for item in staged.diagnostics} == {"duplicate_signal_id", "duplicate_import_tag"}


def test_apply_ceproject_io_import_requires_exact_approval_and_writes_complete_payload_once():
    project = FakeObject("Project")
    original = IOSignal("DI-0001", "Existing", "digital_input", address="%I0.0", rack="0", slot="1", channel="0", mapping_status="allocated")
    project.IOSignals = [serialize_io_signal(original)]
    staged = stage_ceproject_io_import(
        _ceproject_with_signals(
            '<Signal signalId="SIG-1" tag="DI-0001" type="DI" description="Photoeye"/>'
            '<Signal signalId="SIG-2" tag="DO-0001" type="DO" description="Run light"/>'
        ), current_signals=explicit_io_signals_from_project(project),
    )

    with pytest.raises(ImportReviewError, match="Select at least one"):
        apply_approved_ceproject_io_import(project, staged, set())
    with pytest.raises(ImportReviewError, match="were not staged"):
        apply_approved_ceproject_io_import(project, staged, {"io:missing"})

    result = apply_approved_ceproject_io_import(project, staged, {"io:SIG-1", "io:SIG-2"})

    assert [(signal.tag, signal.description, signal.rack, signal.slot, signal.channel, signal.mapping_status) for signal in result] == [
        ("DI-0001", "Photoeye", "0", "1", "0", "allocated"),
        ("DO-0001", "Run light", "", "", "", "unmapped"),
    ]
    assert explicit_io_signals_from_project(project) == list(result)


def test_i_o_only_import_source_is_remembered_after_approved_apply():
    project = FakeObject("Project")
    project.IOSignals = []
    project.CEProjectImports = []
    staged = stage_ceproject_io_import(
        _ceproject_with_signals('<Signal signalId="SIG-1" tag="DI-0001" type="DI" description="Photoeye"/>'),
        "incoming.ceproject.xml",
    )

    apply_approved_ceproject_io_import(project, staged, {"io:SIG-1"})
    remember_approved_ceproject_io_source(project, staged)

    assert len(project.CEProjectImports) == 1


def test_apply_ceproject_io_import_rejects_stale_review_before_mutation():
    project = FakeObject("Project")
    project.IOSignals = [serialize_io_signal(IOSignal("DI-0001", "Existing", "digital_input"))]
    staged = stage_ceproject_io_import(
        _ceproject_with_signals('<Signal signalId="SIG-1" tag="DI-0001" type="DI" description="Changed"/>'),
        current_signals=explicit_io_signals_from_project(project),
    )
    project.IOSignals = [serialize_io_signal(IOSignal("DI-0001", "Someone else changed it", "digital_input"))]

    with pytest.raises(ImportReviewError, match="stale"):
        apply_approved_ceproject_io_import(project, staged, {"io:SIG-1"})

    assert explicit_io_signals_from_project(project)[0].description == "Someone else changed it"


def test_apply_ceproject_io_import_rejects_malformed_current_record_without_overwrite():
    project = FakeObject("Project")
    project.IOSignals = ["not-json"]
    staged = stage_ceproject_io_import(
        _ceproject_with_signals('<Signal signalId="SIG-1" tag="DI-0001" type="DI" description="Photoeye"/>'),
    )

    with pytest.raises(ImportReviewError, match="malformed"):
        apply_approved_ceproject_io_import(project, staged, {"io:SIG-1"})

    assert project.IOSignals == ["not-json"]


def test_apply_ceproject_io_import_blocks_unsupported_or_type_conflicted_rows_before_mutation():
    project = FakeObject("Project")
    existing = IOSignal("DI-0001", "Existing", "digital_input")
    project.IOSignals = [serialize_io_signal(existing)]
    staged = stage_ceproject_io_import(
        _ceproject_with_signals('<Signal signalId="SIG-1" tag="DI-0001" type="DO" description="Wrong type"/>'),
        current_signals=[existing],
    )

    with pytest.raises(ImportReviewError, match="conflicts"):
        apply_approved_ceproject_io_import(project, staged, {"io:SIG-1"})

    assert explicit_io_signals_from_project(project) == [existing]
