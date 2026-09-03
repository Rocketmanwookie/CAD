# SPDX-License-Identifier: MIT
"""Stable CEProject fact identifiers used across intake and traceability."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FactSpec:
    """Human-readable registry entry for one addressable project fact."""

    fact_id: str
    label: str
    category: str
    stakeholder: str
    property_name: str = ""


class FactIds:
    """Canonical fact ID constants for the currently supported project model."""

    PROJECT_ID = "project.id"
    PROJECT_NAME = "project.name"
    PROJECT_CUSTOMER = "project.customer"
    PROJECT_SITE_LOCATION = "project.siteLocation"
    SCHEMA_VERSION = "project.schemaVersion"
    CEPROJECT_IMPORTS = "ceproject.imports"
    DELIVERABLES = "intake.deliverables"
    CONTACTS = "contacts"
    SOURCE_RECORDS = "sourceRecords"
    INTAKE_QUESTIONS = "intake.questions"
    IO_SIGNALS = "signals.io"
    POWER_NOMINAL_VOLTAGE = "powerFeed.nominalVoltage"
    POWER_PHASE_COUNT = "powerFeed.phaseCount"
    POWER_CONFIGURATION = "powerFeed.configuration"
    CONTROLLED_LOADS = "powerFeed.controlledLoads"
    ESTIMATED_LOAD_AMPS = "powerFeed.estimatedLoadAmps"
    ENCLOSURE_RATING = "environment.enclosureRating"
    ENCLOSURE_RATINGS = "environment.enclosureRatings"
    PLC_MAKE = "controls.plcMake"
    PLC_LINE = "controls.plcLine"
    PLC_CPU = "controls.plcCpu"
    PLC_PLATFORM = "controls.plcPlatform"
    SENSOR_COUNT = "io.sensorCount"
    DI_COUNT = "io.diCount"
    DO_COUNT = "io.doCount"
    AI_COUNT = "io.aiCount"
    AO_COUNT = "io.aoCount"
    IO_ACCESSORIES = "io.accessories"
    ETHERNET_ADAPTER = "network.ethernetAdapter"
    EXPANSION_POWER_SUPPLY = "powerFeed.expansionPowerSupply"
    IO_EXPANSION_SUGGESTION = "io.expansionSuggestion"
    COMMUNICATION_PROTOCOLS = "network.communicationProtocols"
    PREFERRED_VENDORS = "purchasing.preferredVendors"
    BUDGET_STATUS = "costing.budgetStatus"
    POWER_FEED_STATUS = "powerFeed.status"
    ENCLOSURE_RATING_STATUS = "environment.enclosureRatingStatus"
    PLC_PLATFORM_STATUS = "controls.plcPlatformStatus"
    SENSOR_COUNT_STATUS = "io.sensorCountStatus"


FACT_SPECS: tuple[FactSpec, ...] = (
    FactSpec(FactIds.PROJECT_ID, "Project ID", "project", "Project manager", "ProjectId"),
    FactSpec(FactIds.PROJECT_NAME, "Project name", "project", "Project manager", "ProjectName"),
    FactSpec(FactIds.PROJECT_CUSTOMER, "Customer", "project", "Project manager", "Customer"),
    FactSpec(FactIds.PROJECT_SITE_LOCATION, "Site/location", "project", "Project manager", "SiteLocation"),
    FactSpec(FactIds.SCHEMA_VERSION, "Schema version", "project", "Project manager", "SchemaVersion"),
    FactSpec(FactIds.CEPROJECT_IMPORTS, "CEProject XML imports", "ceproject", "Project manager", "CEProjectImports"),
    FactSpec(FactIds.DELIVERABLES, "Deliverables", "intake", "Project manager", "Deliverables"),
    FactSpec(FactIds.CONTACTS, "Contacts", "contacts", "Project manager", "Contacts"),
    FactSpec(FactIds.SOURCE_RECORDS, "Source records", "sourceRecords", "Project manager", "SourceRecords"),
    FactSpec(FactIds.INTAKE_QUESTIONS, "Intake questions", "intake", "Project manager", "IntakeQuestions"),
    FactSpec(FactIds.IO_SIGNALS, "I/O signals", "signals", "Controls lead", "IOSignals"),
    FactSpec(FactIds.POWER_NOMINAL_VOLTAGE, "Nominal voltage", "powerFeed", "Electrical engineering", "NominalVoltage"),
    FactSpec(FactIds.POWER_PHASE_COUNT, "Phase count", "powerFeed", "Electrical engineering", "PhaseCount"),
    FactSpec(FactIds.POWER_CONFIGURATION, "Power configuration", "powerFeed", "Electrical engineering", "PowerConfiguration"),
    FactSpec(FactIds.CONTROLLED_LOADS, "Controlled loads", "powerFeed", "Electrical engineering", "ControlledLoads"),
    FactSpec(FactIds.ESTIMATED_LOAD_AMPS, "Estimated load amps", "powerFeed", "Electrical engineering", "EstimatedLoadAmps"),
    FactSpec(FactIds.ENCLOSURE_RATING, "Enclosure rating", "environment", "Operations / maintenance", "EnclosureRating"),
    FactSpec(FactIds.ENCLOSURE_RATINGS, "Enclosure ratings", "environment", "Operations / maintenance", "EnclosureRatings"),
    FactSpec(FactIds.PLC_MAKE, "PLC make", "controls", "Controls lead", "PlcMake"),
    FactSpec(FactIds.PLC_LINE, "PLC line", "controls", "Controls lead", "PlcLine"),
    FactSpec(FactIds.PLC_CPU, "PLC CPU", "controls", "Controls lead", "PlcCPU"),
    FactSpec(FactIds.PLC_PLATFORM, "PLC platform", "controls", "Controls lead", "PlcPlatform"),
    FactSpec(FactIds.SENSOR_COUNT, "Sensor count or estimate", "io", "Mechanical / materials handling", "SensorCount"),
    FactSpec(FactIds.DI_COUNT, "Digital input count", "io", "Controls lead", "DICount"),
    FactSpec(FactIds.DO_COUNT, "Digital output count", "io", "Controls lead", "DOCount"),
    FactSpec(FactIds.AI_COUNT, "Analog input count", "io", "Controls lead", "AICount"),
    FactSpec(FactIds.AO_COUNT, "Analog output count", "io", "Controls lead", "AOCount"),
    FactSpec(FactIds.IO_ACCESSORIES, "I/O accessories", "io", "Controls lead", "IOAccessories"),
    FactSpec(FactIds.ETHERNET_ADAPTER, "Ethernet adapter", "network", "Controls lead", "EthernetAdapter"),
    FactSpec(FactIds.EXPANSION_POWER_SUPPLY, "Expansion power supply", "powerFeed", "Controls lead", "ExpansionPowerSupply"),
    FactSpec(FactIds.IO_EXPANSION_SUGGESTION, "I/O expansion suggestion", "io", "Controls lead", "IOExpansionSuggestion"),
    FactSpec(FactIds.COMMUNICATION_PROTOCOLS, "Communication protocols", "network", "Controls lead", "CommunicationProtocols"),
    FactSpec(FactIds.PREFERRED_VENDORS, "Preferred vendors", "purchasing", "Purchasing"),
    FactSpec(FactIds.BUDGET_STATUS, "Budget or quote status", "costing", "Sales / estimator"),
    FactSpec(FactIds.POWER_FEED_STATUS, "Power feed intake status", "powerFeed", "Electrical engineering", "PowerFeedStatus"),
    FactSpec(FactIds.ENCLOSURE_RATING_STATUS, "Enclosure rating intake status", "environment", "Operations / maintenance", "EnclosureRatingStatus"),
    FactSpec(FactIds.PLC_PLATFORM_STATUS, "PLC platform intake status", "controls", "Controls lead", "PlcPlatformStatus"),
    FactSpec(FactIds.SENSOR_COUNT_STATUS, "Sensor count intake status", "io", "Mechanical / materials handling", "SensorCountStatus"),
)


_SPECS_BY_FACT_ID = {spec.fact_id: spec for spec in FACT_SPECS}
_FACT_IDS_BY_PROPERTY = {spec.property_name: spec.fact_id for spec in FACT_SPECS if spec.property_name}
_PROPERTIES_BY_FACT_ID = {spec.fact_id: spec.property_name for spec in FACT_SPECS if spec.property_name}


def known_fact_ids() -> tuple[str, ...]:
    """Return every currently registered fact ID in deterministic order."""
    return tuple(sorted(_SPECS_BY_FACT_ID))


def fact_spec(fact_id: str) -> FactSpec:
    """Return registry metadata for a fact ID."""
    try:
        return _SPECS_BY_FACT_ID[fact_id]
    except KeyError as exc:
        raise KeyError(f"Unknown CEProject fact ID: {fact_id}") from exc


def fact_id_for_property(property_name: str) -> str:
    """Return the canonical fact ID for a FreeCAD `CE_Project` property."""
    try:
        return _FACT_IDS_BY_PROPERTY[property_name]
    except KeyError as exc:
        raise KeyError(f"No CEProject fact ID registered for property: {property_name}") from exc


def property_for_fact_id(fact_id: str) -> str:
    """Return the FreeCAD `CE_Project` property name for a registered fact ID."""
    try:
        return _PROPERTIES_BY_FACT_ID[fact_id]
    except KeyError as exc:
        raise KeyError(f"No CE_Project property registered for fact ID: {fact_id}") from exc


def category_for_fact_id(fact_id: str) -> str:
    """Return the stable category used by missing-data and traceability output."""
    return fact_spec(fact_id).category


def question_id_for_fact_id(fact_id: str) -> str:
    """Return the deterministic starter intake question ID for a fact."""
    return f"Q-{fact_id.replace('.', '-').upper()}"


def missing_data_item_id_for_fact_id(fact_id: str) -> str:
    """Return the deterministic missing-data row ID for a fact."""
    return f"MD-{fact_id.replace('.', '-').upper()}"
