# SPDX-License-Identifier: MIT

from controls_wb.hardware_catalog import load_hardware_catalog
from controls_wb.io_allocation import allocate_io_signals, validate_io_allocations
from controls_wb.io_list import IOSignal
from controls_wb.io_list import io_signals_from_objects, persist_io_allocation_to_project, explicit_io_signals_from_project
from types import SimpleNamespace


def _signals(signal_type: str, count: int) -> list[IOSignal]:
    return [
        IOSignal(f"{signal_type}-{index:04d}", f"{signal_type} {index}", signal_type)
        for index in range(1, count + 1)
    ]


def test_cpu_channels_are_allocated_before_catalog_expansion_modules():
    result = allocate_io_signals(
        _signals("digital_input", 10),
        load_hardware_catalog(),
        "Siemens",
        "S7-1200",
        "CPU 1212C DC/DC/DC",
    )

    assert [(signal.tag, signal.rack, signal.slot, signal.channel) for signal in result.signals] == [
        ("digital_input-0001", "0", "1", "0"),
        ("digital_input-0002", "0", "1", "1"),
        ("digital_input-0003", "0", "1", "2"),
        ("digital_input-0004", "0", "1", "3"),
        ("digital_input-0005", "0", "1", "4"),
        ("digital_input-0006", "0", "1", "5"),
        ("digital_input-0007", "0", "1", "6"),
        ("digital_input-0008", "0", "1", "7"),
        ("digital_input-0009", "0", "2", "0"),
        ("digital_input-0010", "0", "2", "1"),
    ]
    assert [(module.slot, module.part_number) for module in result.modules] == [
        ("1", "6ES7212-1AE40-0XB0"),
        ("2", "6ES7221-1BH32-0XB0"),
    ]
    assert result.findings == ()


def test_allocator_uses_distinct_expansion_slots_by_io_type():
    result = allocate_io_signals(
        _signals("digital_output", 7) + _signals("analog_input", 3),
        load_hardware_catalog(),
        "Siemens",
        "S7-1200",
        "CPU 1212C DC/DC/DC",
    )

    assert [(signal.slot, signal.channel) for signal in result.signals] == [
        ("1", "0"), ("1", "1"), ("1", "2"), ("1", "3"), ("1", "4"), ("1", "5"), ("2", "0"),
        ("1", "0"), ("1", "1"), ("3", "0"),
    ]
    assert [module.part_number for module in result.modules] == [
        "6ES7212-1AE40-0XB0", "6ES7222-1BH32-0XB0", "6ES7231-4HF32-0XB0",
    ]


def test_allocator_reports_catalog_and_signal_type_gaps_without_inventing_assignments():
    result = allocate_io_signals(
        [IOSignal("RLY-0001", "relay", "relay")],
        load_hardware_catalog(),
        "Allen-Bradley",
        "Micro800",
        "Micro800 starter placeholder",
    )

    assert result.signals[0].slot == ""
    assert [(finding.code, finding.signal_tag) for finding in result.findings] == [
        ("unsupported_io_signal_type", "RLY-0001"),
    ]


def test_allocator_reports_insufficient_capacity_when_no_compatible_module_exists():
    result = allocate_io_signals(
        _signals("digital_input", 1),
        load_hardware_catalog(),
        "Allen-Bradley",
        "Micro800",
        "Micro800 starter placeholder",
    )

    assert result.signals[0].mapping_status == "unmapped"
    assert result.findings[0].code == "insufficient_io_capacity"


def test_validation_reports_collision_in_imported_or_manually_edited_assignments():
    findings = validate_io_allocations(
        [
            IOSignal("DI-0001", "first", "digital_input", rack="0", slot="1", channel="0"),
            IOSignal("DI-0002", "second", "digital_input", rack="0", slot="1", channel="0"),
            IOSignal("DO-0001", "separate namespace", "digital_output", rack="0", slot="1", channel="0"),
        ]
    )

    assert [(finding.code, finding.signal_tag) for finding in findings] == [
        ("io_channel_collision", "DI-0002"),
    ]


def test_project_io_projection_uses_the_selected_catalog_allocation():
    project = SimpleNamespace(
        ProjectId="CE-001",
        ProjectName="Allocation test",
        SchemaVersion="0.1.0",
        Deliverables=["ioList"],
        SensorCount="",
        SensorCountStatus="Received",
        PlcMake="Siemens",
        PlcLine="S7-1200",
        PlcCPU="CPU 1212C DC/DC/DC",
        DICount="9",
        DOCount="",
        AICount="",
        AOCount="",
        IOSignals=[],
        SourceRecords=[],
    )

    signals = io_signals_from_objects([project])

    assert [(signal.slot, signal.channel) for signal in signals] == [
        *(('1', str(index)) for index in range(8)),
        ('2', '0'),
    ]
    assert {signal.mapping_status for signal in signals} == {"allocated"}


def test_persisted_allocation_survives_project_signal_round_trip():
    project = SimpleNamespace(
        ProjectId="CE-002", ProjectName="Persist", SchemaVersion="0.1.0", Deliverables=["ioList"],
        SensorCount="", SensorCountStatus="Received", PlcMake="Siemens", PlcLine="S7-1200",
        PlcCPU="CPU 1212C DC/DC/DC", DICount="2", DOCount="", AICount="", AOCount="",
        IOSignals=[], SourceRecords=[],
    )

    persist_io_allocation_to_project(project)

    assert [(signal.slot, signal.channel) for signal in explicit_io_signals_from_project(project)] == [
        ("1", "0"), ("1", "1"),
    ]
