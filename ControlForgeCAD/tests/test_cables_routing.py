# SPDX-License-Identifier: MIT

import json

import pytest

from controls_wb.cables_routing import (
    CABLES_ROUTE_BACKLINK_PROPERTY,
    cables_available,
    create_or_update_cables_route,
    route_link_is_identity_safe,
    route_points_from_cables,
    route_points_from_ce_wire,
)
from controls_wb.electrical_path import RoutePoint
from controls_wb.identity import CERoles


class Vector:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z


class Route:
    def __init__(self, points=()):
        self.Points = list(points)
        self.PropertiesList = []
        self.Label = ""

    def addProperty(self, _type, name, _group, _description):
        self.PropertiesList.append(name)


class Wire:
    CERole = CERoles.WIRE
    CEIdentity = "urn:uuid:11111111-1111-4111-8111-111111111111"
    WireTag = "W-101"
    CablesRouteObject = None
    RoutePoints = [
        json.dumps({"sequence": 0, "xMm": 0, "yMm": 0, "zMm": 0}),
        json.dumps({"sequence": 1, "xMm": 100, "yMm": 20, "zMm": 0}),
    ]


class CablesModule:
    def __init__(self):
        self.created = []

    def make_wireflex_from_vectors(self, vectors):
        route = Route(vectors)
        self.created.append(route)
        return route


def test_cables_availability_is_optional_and_import_safe():
    assert cables_available(lambda _name: CablesModule()) is True

    def missing(_name):
        raise ModuleNotFoundError

    assert cables_available(missing) is False


def test_create_and_update_cables_wireflex_uses_identity_safe_two_sided_link():
    wire = Wire()
    cables = CablesModule()
    route = (RoutePoint(0, 0, 0), RoutePoint(25, 50, 0))

    created = create_or_update_cables_route(wire, route, module_loader=lambda _name: cables, vector_factory=Vector)

    assert wire.CablesRouteObject is created
    assert getattr(created, CABLES_ROUTE_BACKLINK_PROPERTY) == wire.CEIdentity
    assert created.Label == "Cables route — W-101"
    assert route_link_is_identity_safe(wire)
    assert route_points_from_cables(created) == route

    updated = create_or_update_cables_route(wire, (RoutePoint(1, 2, 3), RoutePoint(4, 5, 6)), module_loader=lambda _name: cables, vector_factory=Vector)
    assert updated is created
    assert len(cables.created) == 1
    assert route_points_from_cables(updated) == (RoutePoint(1, 2, 3), RoutePoint(4, 5, 6))


def test_cables_route_rejects_foreign_or_tampered_link():
    wire = Wire()
    wire.CablesRouteObject = Route()
    wire.CablesRouteObject.CEWireIdentity = "urn:uuid:22222222-2222-4222-8222-222222222222"

    with pytest.raises(ValueError, match="mismatched"):
        create_or_update_cables_route(wire, (RoutePoint(0, 0, 0), RoutePoint(1, 0, 0)), module_loader=lambda _name: CablesModule(), vector_factory=Vector)


def test_initial_cables_route_reads_the_existing_part_polyline_contract():
    assert route_points_from_ce_wire(Wire()) == (RoutePoint(0, 0, 0), RoutePoint(100, 20, 0))
