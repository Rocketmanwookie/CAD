# SPDX-License-Identifier: MIT

import json
from types import SimpleNamespace

from controls_wb.commands.export_io_list import io_list_csv_for_objects
from controls_wb.gui.io_signal import add_io_signal_from_form, normalized_io_signal_form_values
from controls_wb.io_list import (
    IO_LIST_HEADERS,
    IOSignal,
    append_io_signal_to_project,
    create_labeled_io_signal,
    explicit_io_signals_from_project,
    io_list_csv,
    io_mapping_summary,
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


def _typed_project(di="2", do="1", ai="1", ao="1"):
    project = _project("")
    project.PlcMake = "Siemens"
    project.PlcLine = "S7-1500"
    project.PlcPlatform = "Siemens S7-1500"
    project.DICount = di
    project.DOCount = do
    project.AICount = ai
    project.AOCount = ao
    project.IOAccessories = ["Remote / modular I/O bank"]
    return project


def test_io_signal_csv_row_uses_stable_headers():
    signal = IOSignal(
        tag="DI-0001",
        address="%I0.0",
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
    assert signal.to_csv_row()["Address"] == "%I0.0"
    assert signal.to_csv_row()["SourceRecordIds"] == "SRC-1;SRC-2"


def test_starter_io_signals_from_project_sensor_count():
    signals = starter_io_signals_from_project(_project("2"))

    assert signals == [
        IOSignal(
            tag="DI-0001",
            address="%I0.0",
            description="Starter digital input 1",
            signal_type="digital_input",
            device="Digital Input 1",
            source_record_ids=("SRC-IO",),
            mapping_status="addressed",
        ),
        IOSignal(
            tag="DI-0002",
            address="%I0.1",
            description="Starter digital input 2",
            signal_type="digital_input",
            device="Digital Input 2",
            source_record_ids=("SRC-IO",),
            mapping_status="addressed",
        ),
    ]


def test_starter_io_signals_from_typed_project_counts():
    signals = starter_io_signals_from_project(_typed_project(di="2", do="1", ai="1", ao="1"))

    assert [(signal.tag, signal.address, signal.signal_type) for signal in signals] == [
        ("DI-0001", "%I0.0", "digital_input"),
        ("DI-0002", "%I0.1", "digital_input"),
        ("DO-0001", "%Q0.0", "digital_output"),
        ("AI-0001", "%IW0", "analog_input"),
        ("AO-0001", "%QW0", "analog_output"),
    ]
    assert {signal.mapping_status for signal in signals} == {"addressed"}


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
        "Tag,Address,Description,SignalType,Device,Rack,Slot,Channel,Terminal,SourceRecordIds,MappingStatus\n"
        "DI-0001,%I0.0,Starter digital input 1,digital_input,Digital Input 1,,,,,SRC-IO,addressed\n"
        "DI-0002,%I0.1,Starter digital input 2,digital_input,Digital Input 2,,,,,SRC-IO,addressed\n"
    )


def test_unmapped_io_findings_are_clear():
    findings = unmapped_io_findings(starter_io_signals_from_project(_project("")))

    assert findings == ["ERROR: IO-UNASSIGNED-001 has no usable I/O source data."]


def test_io_mapping_summary_collapses_unmapped_warning_noise():
    summary = io_mapping_summary(
        [
            IOSignal(
                tag=f"DI-{index:04d}",
                description=f"Starter digital input {index}",
                signal_type="digital_input",
                mapping_status="unmapped",
            )
            for index in range(1, 31)
        ]
    )

    assert summary == (
        "WARNING: I/O list has 30 signals not mapped to PLC rack/slot/channel. "
        "See integracab_io_list.csv for details."
    )


def test_io_mapping_summary_reports_missing_source_data_as_error():
    summary = io_mapping_summary(starter_io_signals_from_project(_project("")))

    assert summary == (
        "ERROR: I/O list has 1 signal with missing source data. "
        "See integracab_io_list.csv for details."
    )


def test_create_labeled_io_signal_assigns_type_tag_and_address():
    first = create_labeled_io_signal("digital_input", "Photoeye PE-101")
    second = create_labeled_io_signal("digital_input", "Limit switch LS-102", [first])
    relay = create_labeled_io_signal("relay", "Motor starter relay")
    analog = create_labeled_io_signal("analog_input", "Tank level")

    assert first.tag == "DI-0001"
    assert first.address == "%I0.0"
    assert first.description == "Photoeye PE-101"
    assert second.tag == "DI-0002"
    assert second.address == "%I0.1"
    assert relay.tag == "RLY-0001"
    assert relay.address == "RLY-0001"
    assert analog.tag == "AI-0001"
    assert analog.address == "%IW0"


def test_append_io_signal_to_project_stores_json_records():
    project = _project("2")

    signal = append_io_signal_to_project(project, "digital_output", "Stack light green")

    assert signal.tag == "DO-0001"
    assert signal.address == "%Q0.0"
    assert explicit_io_signals_from_project(project) == [signal]


def test_explicit_io_signals_reduce_remaining_starter_inputs():
    project = _project("2")
    explicit = append_io_signal_to_project(project, "digital_input", "Photoeye PE-101")

    signals = io_signals_from_objects([project])

    assert signals[0] == explicit
    assert [signal.tag for signal in signals] == ["DI-0001", "DI-0002"]
    assert signals[1].description == "Starter digital input 2"


def test_io_signal_form_mapping_appends_to_existing_project():
    document = SimpleNamespace(Objects=[_project("1")])

    signal = add_io_signal_from_form(
        document,
        {"SignalType": "Analog Output", "Label": "VFD speed command"},
    )

    assert signal.tag == "AO-0001"
    assert signal.address == "%QW0"
    assert explicit_io_signals_from_project(document.Objects[0]) == [signal]
    assert normalized_io_signal_form_values(
        {"SignalType": "Relay", "Label": "  Pump enable  "}
    ) == {"SignalType": "relay", "Label": "Pump enable"}


def test_io_signals_and_command_helper_read_project_objects_only():
    objects = [SimpleNamespace(Tag="M101"), _project("1")]

    assert [signal.tag for signal in io_signals_from_objects(objects)] == ["DI-0001"]
    assert "DI-0001,%I0.0,Starter digital input 1" in io_list_csv_for_objects(objects)
