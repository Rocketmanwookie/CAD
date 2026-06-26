# SPDX-License-Identifier: MIT

import json
from types import SimpleNamespace

from controls_wb.commands.export_io_list import io_list_csv_for_objects
from controls_wb.io_list import (
    IO_LIST_HEADERS,
    IOSignal,
    io_list_csv,
    io_signals_from_objects,
    starter_io_signals_from_project,
    unmapped_io_findings,
)


def _project(sensor_count="2"):
    return SimpleNamespace(
        ProjectId="CE-PROJECT-001",
        ProjectName="Controls Project",
        SchemaVersion="0.1.0",
        Deliverables=["ioList"],
        SensorCount=sensor_count,
        SensorCountStatus="Received",
        SourceRecords=[
            json.dumps(
                {
                    "id": "SRC-IO",
                    "type": "meeting_note",
                    "title": "Sensor count review",
                    "stakeholder": "Mechanical / materials handling",
                    "fieldIds": ["io.sensorCount"],
                }
            )
        ],
    )


def test_io_signal_csv_row_uses_stable_headers():
    signal = IOSignal(
        tag="DI-0001",
        description="Photoeye",
        signal_type="digital_input",
        device="PE-001",
        rack="0",
        slot="1",
        channel="0",
        terminal="TB1-1",
        source_record_ids=("SRC-1", "SRC-2"),
        mapping_status="mapped",
    )

    assert tuple(signal.to_csv_row()) == IO_LIST_HEADERS
    assert signal.to_csv_row()["SourceRecordIds"] == "SRC-1;SRC-2"


def test_starter_io_signals_from_project_sensor_count():
    signals = starter_io_signals_from_project(_project("2"))

    assert signals == [
        IOSignal(
            tag="DI-0001",
            description="Starter discrete input 1",
            signal_type="digital_input",
            device="Sensor 1",
            source_record_ids=("SRC-IO",),
            mapping_status="unmapped",
        ),
        IOSignal(
            tag="DI-0002",
            description="Starter discrete input 2",
            signal_type="digital_input",
            device="Sensor 2",
            source_record_ids=("SRC-IO",),
            mapping_status="unmapped",
        ),
    ]


def test_starter_io_signals_reports_missing_or_invalid_sensor_count():
    signals = starter_io_signals_from_project(_project(""))

    assert signals == [
        IOSignal(
            tag="IO-UNASSIGNED-001",
            description="Sensor count is missing or not numeric",
            signal_type="unknown",
            source_record_ids=("SRC-IO",),
            mapping_status="missing",
        )
    ]


def test_io_list_csv_is_deterministic():
    csv_text = io_list_csv(starter_io_signals_from_project(_project("2")))

    assert csv_text == (
        "Tag,Description,SignalType,Device,Rack,Slot,Channel,Terminal,SourceRecordIds,MappingStatus\n"
        "DI-0001,Starter discrete input 1,digital_input,Sensor 1,,,,,SRC-IO,unmapped\n"
        "DI-0002,Starter discrete input 2,digital_input,Sensor 2,,,,,SRC-IO,unmapped\n"
    )


def test_unmapped_io_findings_are_clear():
    findings = unmapped_io_findings(starter_io_signals_from_project(_project("")))

    assert findings == ["ERROR: IO-UNASSIGNED-001 has no usable I/O source data."]


def test_io_signals_and_command_helper_read_project_objects_only():
    objects = [SimpleNamespace(Tag="M101"), _project("1")]

    assert [signal.tag for signal in io_signals_from_objects(objects)] == ["DI-0001"]
    assert "DI-0001,Starter discrete input 1" in io_list_csv_for_objects(objects)
