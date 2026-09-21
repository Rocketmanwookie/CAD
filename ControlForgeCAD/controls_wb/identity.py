# SPDX-License-Identifier: MIT
"""Stable CEProject identities and controlled semantic roles."""

from __future__ import annotations

from uuid import UUID, uuid4, uuid5


CEPROJECT_IDENTITY_NAMESPACE = UUID("cf96d3b8-720a-4acd-9fc6-39d4d4131778")


class CERoles:
    PROJECT = "project.root"
    PANEL = "panel.enclosure"
    MOUNTING_RAIL = "panel.mounting_rail"
    WIRE_DUCT = "panel.wire_duct"
    TERMINAL_STRIP = "electrical.terminal_strip"
    PLC_CONTROLLER = "plc.controller"
    PLC_CHANNEL_TERMINAL = "plc.channel_terminal"
    CABINET_TERMINAL = "electrical.cabinet_terminal"
    DEVICE_TERMINAL = "electrical.device_terminal"
    WIRE = "electrical.wire"
    SIGNAL = "electrical.signal"
    CONNECTION_PATH = "electrical.connection_path"
    FIELD_DEVICE = "electrical.field_device"


KNOWN_ROLES = frozenset(
    {
        CERoles.PROJECT,
        CERoles.PANEL,
        CERoles.MOUNTING_RAIL,
        CERoles.WIRE_DUCT,
        CERoles.TERMINAL_STRIP,
        CERoles.PLC_CONTROLLER,
        CERoles.PLC_CHANNEL_TERMINAL,
        CERoles.CABINET_TERMINAL,
        CERoles.DEVICE_TERMINAL,
        CERoles.WIRE,
        CERoles.SIGNAL,
        CERoles.CONNECTION_PATH,
        CERoles.FIELD_DEVICE,
    }
)


def new_ce_identity() -> str:
    """Return an opaque identity for a newly placed CEProject entity."""

    return uuid4().urn


def imported_ce_identity(source_system: str, source_identity: str) -> str:
    """Return a repeatable identity when an imported source has no CE identity."""

    source_key = f"{str(source_system).strip()}:{str(source_identity).strip()}"
    return uuid5(CEPROJECT_IDENTITY_NAMESPACE, source_key).urn


def is_ce_identity(value: object) -> bool:
    text = str(value)
    if not text.startswith("urn:uuid:"):
        return False
    try:
        return str(UUID(text.removeprefix("urn:uuid:"))) == text.removeprefix("urn:uuid:")
    except (TypeError, ValueError):
        return False


def validate_ce_role(role: str) -> str:
    normalized = str(role).strip()
    if normalized not in KNOWN_ROLES:
        raise ValueError(f"Unsupported CEProject role: {normalized}")
    return normalized


def ensure_object_identity(obj, role: str, identity: str | None = None) -> str:
    """Assign identity and role once, preserving identities already on an object."""

    normalized_role = validate_ce_role(role)
    existing_properties = set(getattr(obj, "PropertiesList", []) or [])
    if "CEIdentity" not in existing_properties:
        obj.addProperty(
            "App::PropertyString",
            "CEIdentity",
            "CEProject Identity",
            "Immutable identity shared by logical, 2D, 3D, export, and runtime representations",
        )
    if "CERole" not in existing_properties:
        obj.addProperty(
            "App::PropertyString",
            "CERole",
            "CEProject Identity",
            "Controlled semantic role assigned when the object enters CEProject",
        )

    current_identity = str(getattr(obj, "CEIdentity", "") or "").strip()
    if not current_identity:
        candidate = identity or new_ce_identity()
        if not is_ce_identity(candidate):
            raise ValueError(f"Invalid CEProject identity: {candidate}")
        obj.CEIdentity = candidate
        current_identity = candidate

    current_role = str(getattr(obj, "CERole", "") or "").strip()
    if current_role and current_role != normalized_role:
        raise ValueError(
            f"CEProject role is already {current_role}; cannot silently change it to {normalized_role}."
        )
    if not current_role:
        obj.CERole = normalized_role

    set_editor_mode = getattr(obj, "setEditorMode", None)
    if callable(set_editor_mode):
        set_editor_mode("CEIdentity", 1)
        set_editor_mode("CERole", 1)
    return current_identity
