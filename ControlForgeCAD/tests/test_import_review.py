# SPDX-License-Identifier: MIT

import pytest

from controls_wb.import_review import (
    ImportReviewError,
    apply_approved_project_import,
    stage_project_import,
)
from controls_wb.ceproject_xml import ceproject_to_xml
from controls_wb.electrical_path import ElectricalConnectionPath, TerminalEndpoint, WireSegment
from controls_wb.identity import CERoles, new_ce_identity
from controls_wb.intake import default_project_intake
from controls_wb.model.project import create_or_update_project


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
