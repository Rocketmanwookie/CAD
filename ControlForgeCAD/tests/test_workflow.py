# SPDX-License-Identifier: MIT
from types import SimpleNamespace

import pytest

from controls_wb.gui.workflow import save_io_counts, save_plant_questionnaire, sizing_targets


def test_sizing_rounds_each_type_up_without_turning_spares_into_points():
    assert sizing_targets(dict(DICount="1", DOCount="5", AICount="6", AOCount="0")) == {
        "DICount": (1, 2), "DOCount": (5, 6), "AICount": (6, 8), "AOCount": (0, 0),
    }


@pytest.mark.parametrize("count", ["-1", "1.5", "ten", "inf"])
def test_invalid_count_does_not_mutate_project(count):
    project = SimpleNamespace(ProjectId="P", Deliverables=[], DICount="2")
    document = SimpleNamespace(Objects=[project])
    with pytest.raises(ValueError):
        save_io_counts(document, dict(DICount=count))
    assert project.DICount == "2"


def test_count_step_preserves_hardware_and_defined_io():
    project = SimpleNamespace(ProjectId="P", Deliverables=[], PlcCPU="Selected CPU", IOSignals=["defined"])
    save_io_counts(SimpleNamespace(Objects=[project]), dict(DICount="3", AICount="2"))
    assert project.SensorCount == "5"
    assert project.DICount == "3"
    assert project.PlcCPU == "Selected CPU"
    assert project.IOSignals == ["defined"]


def test_plant_step_preserves_counts_hardware_and_defined_io():
    project = SimpleNamespace(ProjectId="P", Deliverables=[], PlcCPU="Selected CPU", DICount="7", IOSignals=["defined"])
    save_plant_questionnaire(SimpleNamespace(Objects=[project]), dict(ProjectName="Plant A", PowerConfiguration="1PH 120V"))
    assert project.ProjectName == "Plant A"
    assert project.NominalVoltage == "120"
    assert project.PlcCPU == "Selected CPU"
    assert project.DICount == "7"
    assert project.IOSignals == ["defined"]
