# SPDX-License-Identifier: MIT
"""Live FreeCAD regression for the PLC allocation dependency graph."""

import pytest

App = pytest.importorskip("FreeCAD", reason="FreeCAD Python module is required for the live recompute regression")

from controls_wb.model.layout import materialize_plc_allocation
from controls_wb.model.project import create_or_update_project


def test_materialized_allocation_recomputes_without_a_dependency_cycle():
    document = App.newDocument("ControlForgeCADAllocationRecompute")
    try:
        project = create_or_update_project(document)
        project.ProjectId = "CE-RECOMPUTE-001"
        project.PlcMake = "Siemens"
        project.PlcLine = "S7-1200"
        project.PlcCPU = "CPU 1212C DC/DC/DC"
        project.DICount = "1"

        materialize_plc_allocation(document, project)

        assert document.recompute() == 0
    finally:
        App.closeDocument(document.Name)
