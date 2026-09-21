# SPDX-License-Identifier: MIT
"""Small, import-safe adapter for the optional FreeCAD Cables workbench.

The Cables workbench is deliberately loaded only from the functions which need
it.  This keeps schedule/export code usable in Python and makes a missing
optional workbench a normal fallback case rather than an import failure.
"""

from __future__ import annotations

import importlib
import json

from controls_wb.electrical_path import RoutePoint
from controls_wb.identity import CERoles, is_ce_identity


CABLES_ROUTE_LINK_PROPERTY = "CablesRouteObject"
CABLES_ROUTE_BACKLINK_PROPERTY = "CEWireIdentity"


def cables_available(module_loader=importlib.import_module) -> bool:
    """Return whether the installed Cables workbench exposes WireFlex."""

    try:
        return callable(getattr(module_loader("freecad.cables.wireFlex"), "make_wireflex_from_vectors", None))
    except (ImportError, ModuleNotFoundError):
        return False


def route_points_from_cables(route_object) -> tuple[RoutePoint, ...]:
    """Read Cables' local ``Points`` into the canonical CE route contract."""

    return tuple(
        RoutePoint(float(point.x), float(point.y), float(point.z))
        for point in (getattr(route_object, "Points", []) or [])
    )


def route_points_from_ce_wire(wire_object) -> tuple[RoutePoint, ...]:
    """Read the CE wire's persisted fallback polyline for initial Cables routing."""

    records = []
    for record in getattr(wire_object, "RoutePoints", []) or []:
        payload = json.loads(record)
        records.append((int(payload["sequence"]), RoutePoint(float(payload["xMm"]), float(payload["yMm"]), float(payload["zMm"]))))
    records.sort(key=lambda item: item[0])
    if [sequence for sequence, _ in records] != list(range(len(records))):
        raise ValueError("Wire route point sequence must be contiguous from zero.")
    return tuple(point for _, point in records)


def route_link_is_identity_safe(wire_object, route_object=None) -> bool:
    """Check both the persisted link and Cables route's immutable CE backlink."""

    route_object = route_object or getattr(wire_object, CABLES_ROUTE_LINK_PROPERTY, None)
    wire_identity = str(getattr(wire_object, "CEIdentity", "") or "")
    return (
        getattr(wire_object, "CERole", "") == CERoles.WIRE
        and is_ce_identity(wire_identity)
        and route_object is not None
        and getattr(wire_object, CABLES_ROUTE_LINK_PROPERTY, None) is route_object
        and str(getattr(route_object, CABLES_ROUTE_BACKLINK_PROPERTY, "") or "") == wire_identity
    )


def _add_property_if_missing(obj, property_type: str, name: str, group: str, description: str) -> None:
    if name not in set(getattr(obj, "PropertiesList", []) or []):
        obj.addProperty(property_type, name, group, description)


def _vectors(route: tuple[RoutePoint, ...], vector_factory):
    return [vector_factory(point.x_mm, point.y_mm, point.z_mm) for point in route]


def create_or_update_cables_route(wire_object, route: tuple[RoutePoint, ...], *, module_loader=importlib.import_module, vector_factory=None):
    """Create or update the linked Cables ``WireFlex`` route for one CE wire.

    ``vector_factory`` is injectable so this integration boundary can be tested
    without FreeCAD.  The Cables module is only imported after all input checks.
    """

    if len(route) < 2:
        raise ValueError("A Cables route requires at least two route points.")
    wire_identity = str(getattr(wire_object, "CEIdentity", "") or "")
    if getattr(wire_object, "CERole", "") != CERoles.WIRE or not is_ce_identity(wire_identity):
        raise ValueError("Cables routing requires an identified typed CE_Wire.")
    cables = module_loader("freecad.cables.wireFlex")
    if vector_factory is None:
        app = module_loader("FreeCAD")
        vector_factory = app.Vector
    vectors = _vectors(route, vector_factory)
    existing = getattr(wire_object, CABLES_ROUTE_LINK_PROPERTY, None)
    if route_link_is_identity_safe(wire_object, existing):
        existing.Points = vectors
        return existing
    if existing is not None:
        raise ValueError("CE_Wire has a Cables route link with a mismatched CE wire identity.")
    route_object = cables.make_wireflex_from_vectors(vectors)
    if route_object is None:
        raise RuntimeError("Cables workbench did not create a WireFlex route.")
    _add_property_if_missing(route_object, "App::PropertyString", CABLES_ROUTE_BACKLINK_PROPERTY, "ControlForgeCAD", "Immutable CE wire identity owning this Cables route")
    route_object.CEWireIdentity = wire_identity
    route_object.Label = f"Cables route — {getattr(wire_object, 'WireTag', wire_identity)}"
    wire_object.CablesRouteObject = route_object
    return route_object
